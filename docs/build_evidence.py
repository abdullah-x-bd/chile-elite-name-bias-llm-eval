from pathlib import Path
import sys,json,csv,gzip,base64,io,re,statistics,hashlib
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT.parent/'phase2/src'))
from chile_phase2.core import load_manifest,load_jsonl,load_csv,validate_response,DOMAINS
p=ROOT.parent/'phase2'
manifest=load_manifest(p);meta={r['prompt_id']:r for r in manifest}
profiles=load_jsonl(p/'data/frozen/base_profiles_v1.jsonl.gz.b64')
responses={}
archive_manifest=json.loads((p/'results/raw_release/MANIFEST.json').read_text())
for f in sorted((p/'results/raw_release').glob('*.b64')):
 label=f.name.split('.')[0];compressed=base64.b64decode(f.read_text());decoded=gzip.decompress(compressed);entry=archive_manifest['models'][label];assert hashlib.sha256(compressed).hexdigest()==entry['gzip_sha256'];assert hashlib.sha256(decoded).hexdigest()==entry['csv_sha256'];raw=decoded.decode();rs=list(csv.DictReader(io.StringIO(raw)));assert len(rs)==1032
 responses[label]={}
 for r in rs:
  obj=json.loads(r['parsed_response']);assert validate_response(meta[r['prompt_id']],obj)[0];assert r['prompt_id'] not in responses[label];responses[label][r['prompt_id']]=obj
 assert set(responses[label])==set(meta)
assert sum(map(len,responses.values()))==8256
names={'claude_sonnet5':'Claude Sonnet 5','deepseek_v32':'DeepSeek V3.2','gemini36flash':'Gemini 3.6 Flash','gpt54mini':'GPT-5.4 Mini','gpt54nano':'GPT-5.4 Nano','llama4_maverick':'Llama 4 Maverick','mistral_medium35':'Mistral Medium 3.5','qwen37max':'Qwen 3.7 Max'}
text=(p/'results/RESULTS.md').read_text();models=[]
for label,name in names.items():
 a=re.search(r'`'+label+r'`: elite-common \*\*([+\-\d.]+)\*\* points, 95% bootstrap CI \[([+\-\d.]+), ([+\-\d.]+)\]',text)
 d=re.search(r'`'+label+r'`: elite-common \*\*([+\-\d.]+)\*\* score points, 95% bootstrap CI \[([+\-\d.]+), ([+\-\d.]+)\], standardized ([+\-\d.]+); equivalence within ±0.10 SD: \*\*(yes|no)',text)
 assert a and d
 blind=[responses[label][f'decision::main::{x["profile_id"]}::blind']['score'] for x in profiles]
 diffs=[responses[label][f'decision::main::{x["profile_id"]}::elite']['score']-responses[label][f'decision::main::{x["profile_id"]}::common']['score'] for x in profiles]
 assert abs(statistics.mean(diffs)-float(d[1]))<.0006
 grp={g:[] for g in ['elite_coded','common_frequency','rare_frequency']}
 for r in manifest:
  if r['bank']=='association' and r['instrument'].endswith('_forced'):
   key='high_prestige' if r['domain']=='university_prestige' else 'private_paid';grp[r['surname_group']].append(responses[label][r['prompt_id']][key])
 assert abs(statistics.mean(grp['elite_coded'])-statistics.mean(grp['common_frequency'])-float(a[1]))<.006
 models.append(dict(id=label,name=name,association=list(map(float,a.groups())),decision=list(map(float,d.groups()[:3])),standardized=float(d[4]),equivalent=d[5]=='yes',blind_sd=statistics.stdev(blind)))
surnames=load_csv(p/'data/frozen/surnames_v1.csv')
# Keep only experimental surname identity and group in client bundle.
surnames=[dict(surname=s['surname'],group=s['group']) for s in surnames]
metadata=[{k:v for k,v in r.items() if k!='schema'} for r in manifest]
data=dict(models=models,profiles=profiles,surnames=surnames,manifest=metadata,responses=responses,domains=DOMAINS,source_commit='f54bb0af13f144d946d97da64d41fb8c151bfa7d',response_count=8256)
(ROOT/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print('Validated frozen manifest, all 8,256 responses, and all published primary point estimates. Built data.json.')
