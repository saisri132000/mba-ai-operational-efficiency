"""Reproducible exploratory analysis of the public 2025 Stack Overflow archive.

Run with --data and --schema; never combines OECD aggregates with survey records.
"""
from pathlib import Path
import argparse
import hashlib
import json
import warnings
import platform
import numpy as np
import pandas as pd
import scipy
from scipy.stats import rankdata, norm
import statsmodels.api as sm
import statsmodels
from statsmodels.stats.multitest import multipletests

DATA_HASH = '2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa'
SCHEMA_HASH = '1d24951e04eab46c6f9fecef6ce8e6b32a0a14a3f0eecdcf62f70833a74b3ff8'
BASE_URL = 'https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/'
TOOL = {'Yes, I use AI tools monthly or infrequently': 'Monthly or infrequent',
        'Yes, I use AI tools weekly': 'Weekly', 'Yes, I use AI tools daily': 'Daily'}
AGENT = {'Yes, I use AI agents at work monthly or infrequently': 'Monthly or infrequent',
         'Yes, I use AI agents at work weekly': 'Weekly', 'Yes, I use AI agents at work daily': 'Daily'}
NO_AI = ["No, and I don't plan to", 'No, but I plan to soon']
TRUST = {'Highly trust': 1, 'Somewhat trust': 1, 'Neither trust nor distrust': 0,
         'Somewhat distrust': 0, 'Highly distrust': 0}
COMPLEX = {'Very well at handling complex tasks': 1, 'Good, but not great at handling complex tasks': 1,
           'Neither good or bad at handling complex tasks': 0, 'Bad at handling complex tasks': 0,
           'Very poor at handling complex tasks': 0}
ORG = {'Less than 20 employees': 'Under 100', '20 to 99 employees': 'Under 100',
       '100 to 499 employees': '100 to 999', '500 to 999 employees': '100 to 999',
       '1,000 to 4,999 employees': '1000 or more', '5,000 to 9,999 employees': '1000 or more',
       '10,000 or more employees': '1000 or more'}
COUNTRIES = ['United States of America', 'Germany', 'India',
             'United Kingdom of Great Britain and Northern Ireland', 'France']
IMPACT = 'AI agents have increased my productivity.'
LEVELS = ['Strongly disagree', 'Somewhat disagree', 'Neutral', 'Somewhat agree', 'Strongly agree']
DEBUG = 'Debugging AI-generated code is more time-consuming'
NONE = 'I haven’t encountered any problems'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tokens(value):
    return set() if pd.isna(value) else {s.strip() for s in str(value).split(';') if s.strip()}


def decode_impact(frame, item=IMPACT):
    hits = pd.DataFrame({level: frame['AIAgentImpact' + level].map(lambda v: item in tokens(v))
                         for level in LEVELS}, index=frame.index)
    count = hits.sum(axis=1)
    rating = pd.Series(np.nan, index=frame.index, dtype=float)
    for i, level in enumerate(LEVELS):
        rating.loc[hits[level] & count.eq(1)] = i + 1
    return rating, count


def design(frame, frequency=None):
    x = pd.DataFrame({'Intercept': 1.0}, index=frame.index)
    groups = [('experience', ['Under 5', '5 to 9', '10 to 19', '20 or more']),
              ('org_group', ['Under 100', '100 to 999', '1000 or more']),
              ('country_group', COUNTRIES + ['Other countries'])]
    if frequency:
        groups.insert(0, (frequency, ['Monthly or infrequent', 'Weekly', 'Daily']))
    for col, cats in groups:
        for category in cats[1:]:
            x[col + ': ' + category] = frame[col].eq(category).astype(float)
    return x


def auc(y, pred):
    pos = int(y.sum())
    return float((rankdata(pred)[y == 1].sum() - pos * (pos + 1) / 2) / (pos * (len(y) - pos)))


def fit_model(name, eligible, outcome, frequency, primary, out):
    outcome = outcome.reindex(eligible.index)
    answered = eligible.loc[outcome.notna()].copy()
    answered['y'] = outcome.dropna().astype(int)
    complete = answered.dropna(subset=['experience', 'org_group', 'country_group'] + ([frequency] if frequency else []))
    x = design(complete, frequency)
    y = complete.y.to_numpy(dtype=float)
    if len(np.unique(y)) != 2 or np.linalg.matrix_rank(x.to_numpy()) != x.shape[1]:
        raise ValueError(f'{name}: non-identifiable design')
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        result = sm.GLM(y, x, family=sm.families.Binomial()).fit(cov_type='HC1', maxiter=150, tol=1e-10)
    if caught or not result.converged or not np.isfinite(result.params).all():
        raise ValueError(f'{name}: fitting warning or nonconvergence: {[str(w.message) for w in caught]}')
    # Independent optimizer and likelihood implementation cross-check.
    alternative = sm.Logit(y, x).fit(disp=False, maxiter=150)
    difference = float(np.max(np.abs(alternative.params - result.params)))
    if difference > 1e-6:
        raise ValueError(f'{name}: GLM/Logit disagreement {difference}')
    # Explicit HC1 sandwich: statsmodels 0.15 GLM's HC1 label uses HC0 here.
    # Calculate the n/(n-k) correction rather than relying on that label.
    pred = np.asarray(result.predict(x))
    values=x.to_numpy()
    bread=np.linalg.inv(values.T @ ((pred*(1-pred))[:,None]*values))
    scores=values*(y-pred)[:,None]
    hc0=bread @ (scores.T @ scores) @ bread
    if not np.allclose(result.cov_params(),hc0,rtol=1e-6,atol=1e-10):
        raise ValueError(f'{name}: library covariance changed; review HC1 implementation')
    hc1=hc0*len(y)/(len(y)-x.shape[1])
    robust_se=np.sqrt(np.diag(hc1))
    betas=result.params.to_numpy()
    z=norm.ppf(.975)
    coef = pd.DataFrame({'term': x.columns, 'beta': result.params.to_numpy(),
                         'robust_se': robust_se, 'odds_ratio': np.exp(betas),
                         'ci_low': np.exp(betas-z*robust_se), 'ci_high': np.exp(betas+z*robust_se),
                         'p_value': 2*norm.sf(np.abs(betas/robust_se))})
    coef.to_csv(out / f'{name}_coefficients.csv', index=False)
    complete.assign(predicted_probability=pred)[['ResponseId', 'y', 'predicted_probability']].to_csv(
        out / f'{name}_model_rows.csv', index=False)
    calibration = pd.DataFrame({'actual': y, 'predicted': pred})
    calibration['bin'] = pd.qcut(calibration.predicted, 10, duplicates='drop')
    calibration.groupby('bin', observed=True).agg(n=('actual','size'), observed=('actual','mean'),
          predicted=('predicted','mean')).to_csv(out / f'{name}_calibration.csv')
    nonconstant = x.iloc[:, 1:].to_numpy()
    vifs = np.diag(np.linalg.inv(np.corrcoef(nonconstant, rowvar=False)))
    event = int(y.sum())
    minority_ratio = min(event, len(y)-event) / x.shape[1]
    if minority_ratio < 10 or float(vifs.max()) >= 10:
        raise ValueError(f'{name}: sparse outcome or excessive collinearity')
    row = coef.loc[coef.term.eq(primary)].iloc[0].to_dict()
    info = {'name': name, 'eligible_n': len(eligible), 'outcome_observed_n': len(answered),
            'missing_or_invalid_outcome_n': len(eligible)-len(answered),
            'covariate_excluded_n': len(answered)-len(complete), 'n': len(y), 'events': event,
            'nonevents': len(y)-event, 'event_percent': 100*event/len(y), 'parameters': x.shape[1],
            'converged': bool(result.converged), 'max_vif': float(vifs.max()),
            'minority_per_parameter': minority_ratio, 'glm_logit_max_difference': difference,
            'in_sample_auc': auc(y, pred), 'in_sample_brier': float(np.mean((y-pred)**2)),
            'mcfadden_pseudo_r2': float(1-result.llf/result.llnull),
            'covariance': 'Explicit HC1 sandwich with n/(n-k) correction', 'primary': row,
            'missing_covariates_among_answered': {c:int(answered[c].isna().sum()) for c in
                ['experience','org_group','country_group'] + ([frequency] if frequency else [])}}
    return info


def run(data, schema, output):
    output.mkdir(parents=True, exist_ok=True)
    if sha(data) != DATA_HASH or sha(schema) != SCHEMA_HASH:
        raise ValueError('Source checksum mismatch; review changed source before analysing.')
    frame = pd.read_csv(data, low_memory=False)
    if frame.ResponseId.isna().any() or frame.ResponseId.duplicated().any():
        raise ValueError('Missing or duplicate ResponseId; do not silently remove respondents.')
    for c, allowed in [('AISelect', set(TOOL) | set(NO_AI)), ('AIAcc', set(TRUST)),
                       ('AIComplex', set(COMPLEX) | {"I don't use AI tools for complex tasks / I don't know"})]:
        if not set(frame[c].dropna()).issubset(allowed):
            raise ValueError(f'Unreviewed categories in {c}')
    professional = frame.MainBranch.eq('I am a developer by profession')
    employed = professional & frame.Employment.eq('Employed')
    base = frame.loc[employed].copy()
    base['tool_frequency'] = base.AISelect.map(TOOL)
    base['agent_frequency'] = base.AIAgents.map(AGENT)
    exp = pd.to_numeric(base.WorkExp, errors='coerce').where(lambda s:s.between(1,60))
    base['experience'] = pd.cut(exp, [0,5,10,20,61], right=False,
                                labels=['Under 5','5 to 9','10 to 19','20 or more']).astype('object')
    base['org_group'] = base.OrgSize.map(ORG)
    base['country_group'] = base.Country.where(base.Country.isin(COUNTRIES), 'Other countries').where(base.Country.notna())
    users = base.loc[base.tool_frequency.notna()].copy()
    agents = base.loc[base.agent_frequency.notna()].copy()
    rating, hitcount = decode_impact(agents)
    productivity = rating.map({1:0,2:0,3:0,4:1,5:1})
    frustration_sets = users.AIFrustration.map(tokens)
    contradiction = frustration_sets.map(lambda v:NONE in v and len(v)>1)
    debug = users.AIFrustration.map(lambda v: np.nan if pd.isna(v) else int(DEBUG in tokens(v)))
    debug.loc[contradiction] = np.nan
    adoption = base.AISelect.map({**{v:1 for v in TOOL},**{v:0 for v in NO_AI}})
    definitions = [
        ('M1_adoption', base, adoption, None, 'experience: 20 or more'),
        ('M2_productivity', agents, productivity, 'agent_frequency', 'agent_frequency: Daily'),
        ('M3_debugging', users, debug, 'tool_frequency', 'tool_frequency: Daily'),
        ('M4_complex_tasks', users, users.AIComplex.map(COMPLEX), 'tool_frequency', 'tool_frequency: Daily'),
        ('M5_trust', users, users.AIAcc.map(TRUST), 'tool_frequency', 'tool_frequency: Daily')]
    models = [fit_model(*spec, output) for spec in definitions]
    adjusted = multipletests([m['primary']['p_value'] for m in models], method='holm')[1]
    for m, p in zip(models, adjusted):
        m['primary']['holm_p_five_primary_tests'] = float(p)
    sensitivity = fit_model('S1_productivity_exclude_neutral', agents,
        productivity.where(rating.ne(3)), 'agent_frequency', 'agent_frequency: Daily', output)
    audit = {'source_rows':len(frame), 'published_analysis_count':49009,
             'archive_minus_published_count':len(frame)-49009,
             'count_discrepancy':'Public archive differs from published headline count; reason not established. No rows removed merely to match the headline.',
             'professional_developers':int(professional.sum()), 'employed_professional_cohort':len(base),
             'current_tool_users_in_cohort':len(users), 'current_agent_users_in_cohort':len(agents),
             'experience_over_60_excluded_as_covariate':int(pd.to_numeric(base.WorkExp,errors='coerce').gt(60).sum()),
             'contradictory_productivity_ratings':int(hitcount.gt(1).sum()),
             'contradictory_no_frustration':int(contradiction.sum()), 'duplicate_response_ids':0,
             'source_sha256':DATA_HASH,'schema_sha256':SCHEMA_HASH,
             'source_url':BASE_URL+'results.csv','schema_url':BASE_URL+'schema.csv',
             'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
                         'scipy':scipy.__version__,'statsmodels':statsmodels.__version__}}
    # Counts are frequencies of genuine records, not weighted or reconstructed counts.
    descriptive = []
    for cohort_name, cohort in [('Employed professional developers',base),('Current AI tool users',users),('Current AI agent users',agents)]:
        for col in ['AISelect','AIAgents','AIAcc','AIComplex']:
            for value, n in cohort[col].fillna('Missing').value_counts().items():
                descriptive.append({'cohort':cohort_name,'question':col,'response':value,'n':int(n),
                                    'cohort_n':len(cohort),'percent_of_cohort':100*n/len(cohort)})
    pd.DataFrame(descriptive).to_csv(output/'descriptive_counts.csv',index=False)
    summary = {'audit':audit,'models':models,'sensitivity':sensitivity}
    (output/'analysis.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf-8')
    pd.DataFrame([{'model':m['name'],'n':m['n'],'events':m['events'],**m['primary']} for m in models]).to_csv(output/'primary_results.csv',index=False)
    schema_frame = pd.read_csv(schema)
    schema_frame[schema_frame.qname.isin(['MainBranch','Employment','WorkExp','OrgSize','Country','AISelect',
         'AIAgents','AIAcc','AIComplex','AIFrustration','AIAgentImpact'])].to_csv(output/'questionnaire_extract.csv',index=False)
    return summary


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=Path('work/stackoverflow_2025/results.csv'))
    parser.add_argument('--schema',type=Path,default=Path('work/stackoverflow_2025/schema.csv'))
    parser.add_argument('--output',type=Path,default=Path('outputs/stackoverflow2025'))
    args=parser.parse_args()
    result=run(args.data,args.schema,args.output)
    print(json.dumps({'audit':result['audit'],'primary_results':[
        {'model':m['name'],'n':m['n'],**m['primary']} for m in result['models']]},indent=2))
