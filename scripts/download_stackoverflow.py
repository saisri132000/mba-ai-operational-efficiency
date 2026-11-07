"""Download the exact public archive used by this analysis; no credentials required."""
from pathlib import Path
import sys
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stackoverflow_analysis import BASE_URL, DATA_HASH, SCHEMA_HASH, sha

if __name__=='__main__':
    dest=Path(__file__).resolve().parents[1]/'work/stackoverflow_2025'
    dest.mkdir(parents=True,exist_ok=True)
    for name,expected in [('results.csv',DATA_HASH),('schema.csv',SCHEMA_HASH)]:
        target=dest/name
        if target.exists() and sha(target)==expected:
            print(name+': checksum verified');continue
        temporary=dest/(name+'.download')
        urllib.request.urlretrieve(BASE_URL+name,temporary)
        if sha(temporary)!=expected:
            raise ValueError(name+': source has changed; review before proceeding')
        temporary.replace(target)
        print(name+': downloaded and checksum verified')
