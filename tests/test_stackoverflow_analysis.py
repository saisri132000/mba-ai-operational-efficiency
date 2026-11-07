"""Critical coding checks and independent checks against genuine public records."""
import json
from pathlib import Path
import unittest
try:
    import numpy as np
    import pandas as pd
    from stackoverflow_analysis import decode_impact, tokens, LEVELS, IMPACT, DATA_HASH, sha
except ModuleNotFoundError as exc:
    raise unittest.SkipTest('Install requirements-stackoverflow.txt to run regression checks') from exc

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/stackoverflow2025'


class CodingTests(unittest.TestCase):
    def test_blank_is_not_negative(self):
        # Synthetic unit fixture only; never included in empirical results.
        fixture=pd.DataFrame({('AIAgentImpact'+level):[np.nan] for level in LEVELS})
        rating,count=decode_impact(fixture)
        self.assertTrue(rating.isna().all());self.assertEqual(count.iloc[0],0)

    def test_exact_item_and_ambiguity(self):
        fixture=pd.DataFrame({('AIAgentImpact'+level):[np.nan]*3 for level in LEVELS}, dtype=object)
        fixture.loc[0,'AIAgentImpactNeutral']=IMPACT
        fixture.loc[1,'AIAgentImpactSomewhat agree']=IMPACT
        fixture.loc[1,'AIAgentImpactStrongly agree']=IMPACT
        fixture.loc[2,'AIAgentImpactStrongly agree']=IMPACT+' extra'
        rating,count=decode_impact(fixture)
        self.assertEqual(rating.iloc[0],3)
        self.assertTrue(rating.iloc[1:].isna().all())
        self.assertEqual(count.iloc[1],2)

    def test_semicolon_selection(self):
        self.assertEqual(tokens('a; b'),{'a','b'})
        self.assertEqual(tokens(np.nan),set())


class GenuineOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ROOT/'work/stackoverflow_2025/results.csv').exists():
            raise unittest.SkipTest('Run scripts/download_stackoverflow.py to verify genuine source records')
        cls.result=json.loads((OUT/'analysis.json').read_text(encoding='utf-8'))
        cls.raw=pd.read_csv(ROOT/'work/stackoverflow_2025/results.csv',low_memory=False)

    def test_source_and_cohort_counts(self):
        self.assertEqual(sha(ROOT/'work/stackoverflow_2025/results.csv'),DATA_HASH)
        d=self.raw
        self.assertEqual(len(d),self.result['audit']['source_rows'])
        cohort=(d.MainBranch=='I am a developer by profession') & (d.Employment=='Employed')
        self.assertEqual(int(cohort.sum()),self.result['audit']['employed_professional_cohort'])
        self.assertFalse(d.ResponseId.duplicated().any())
        self.assertEqual(len(d)-49009,182)

    def test_model_rows_are_genuine_and_eligible(self):
        raw=self.raw.set_index('ResponseId')
        for model in self.result['models']:
            rows=pd.read_csv(OUT/(model['name']+'_model_rows.csv'))
            source=raw.loc[rows.ResponseId]
            self.assertEqual(len(rows),model['n'])
            self.assertEqual(int(rows.y.sum()),model['events'])
            self.assertTrue(source.MainBranch.eq('I am a developer by profession').all())
            self.assertTrue(source.Employment.eq('Employed').all())
            self.assertTrue(rows.predicted_probability.between(0,1).all())
            if model['name']!='M1_adoption':
                col='AIAgents' if model['name']=='M2_productivity' else 'AISelect'
                self.assertTrue(source[col].str.startswith('Yes,').all())
            if model['name']=='M1_adoption':
                np.testing.assert_array_equal(rows.y.to_numpy(),source.AISelect.str.startswith('Yes,').astype(int).to_numpy())
            if model['name']=='M3_debugging':
                expected=source.AIFrustration.str.split(';').map(lambda a:'Debugging AI-generated code is more time-consuming' in a).astype(int)
                np.testing.assert_array_equal(rows.y.to_numpy(),expected.to_numpy())

    def test_intervals_and_diagnostics(self):
        for m in self.result['models']:
            c=pd.read_csv(OUT/(m['name']+'_coefficients.csv'))
            np.testing.assert_allclose(c.odds_ratio,np.exp(c.beta),rtol=1e-10)
            np.testing.assert_allclose(c.ci_low,np.exp(c.beta-1.959963984540054*c.robust_se),rtol=1e-10)
            np.testing.assert_allclose(c.ci_high,np.exp(c.beta+1.959963984540054*c.robust_se),rtol=1e-10)
            self.assertTrue(m['converged']);self.assertLess(m['max_vif'],10)
            self.assertLess(m['glm_logit_max_difference'],1e-6)
            self.assertEqual(m['n']+m['covariate_excluded_n'],m['outcome_observed_n'])
            self.assertEqual(m['events']+m['nonevents'],m['n'])

    def test_holm_five_primary_contrasts(self):
        p=np.array([m['primary']['p_value'] for m in self.result['models']])
        order=np.argsort(p); adjusted=np.empty(5)
        adjusted[order]=np.minimum(1,np.maximum.accumulate(p[order]*np.arange(5,0,-1)))
        np.testing.assert_allclose(adjusted,[m['primary']['holm_p_five_primary_tests'] for m in self.result['models']],rtol=1e-12)

    def test_sensitivity_preserves_estimation_direction(self):
        sensitivity=self.result['sensitivity'];primary=self.result['models'][1]
        self.assertLess(sensitivity['n'],primary['n'])
        self.assertGreater(sensitivity['primary']['odds_ratio'],1)


if __name__=='__main__':unittest.main()
