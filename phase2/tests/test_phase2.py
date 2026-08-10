import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import generate_profiles, generate_manifest, validate_manifest, sha256_text, validate_response
from chile_phase2.openrouter import request_payload, request_identity

class Phase2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study=json.loads((ROOT/'config/study.json').read_text())
        cls.models=json.loads((ROOT/'config/models.json').read_text())['models']
        cls.profiles=generate_profiles(cls.study['seed'],cls.study['profiles_per_domain'])
        cls.manifest=generate_manifest(ROOT,cls.profiles)
    def test_counts(self):
        self.assertEqual(len(self.profiles),192); self.assertEqual(len(self.manifest),1032); validate_manifest(self.manifest,self.profiles)
    def test_determinism(self):
        self.assertEqual(self.profiles,generate_profiles(self.study['seed'],48)); self.assertEqual(self.manifest,generate_manifest(ROOT,self.profiles))
    def test_counterfactual_main_cells(self):
        pid=self.profiles[0]['profile_id']; cells=[r for r in self.manifest if r['bank']=='decision_main' and r['base_profile_id']==pid]
        self.assertEqual({r['condition'] for r in cells},{'blind','elite','common'})
        self.assertEqual(len(cells),3)
    def test_prompt_hashes(self):
        self.assertTrue(all(r['prompt_sha256']==sha256_text(r['prompt_text']) for r in self.manifest))
    def test_model_pins(self):
        self.assertEqual(len(self.models),8); self.assertEqual(len({m['request_id'] for m in self.models}),8); self.assertTrue(all(m['provider'] for m in self.models))
    def test_provider_fallback_disabled(self):
        p=self.manifest[0]
        for m in self.models:
            payload=request_payload(m,p,self.study)
            self.assertFalse(payload['provider']['allow_fallbacks']); self.assertEqual(payload['provider']['order'],[m['provider']])
            self.assertIn('response_format',payload)
    def test_blind_cells_have_no_frozen_names(self):
        surnames=[x['surname'].lower() for x in __import__('chile_phase2.core',fromlist=['load_csv']).load_csv(ROOT/'data/frozen/surnames_v1.csv')]
        givens=[x['given_name'].lower() for x in __import__('chile_phase2.core',fromlist=['load_csv']).load_csv(ROOT/'data/frozen/given_names_v1.csv')]
        blind=[r for r in self.manifest if r['bank'].startswith('decision') and r['condition'].startswith('blind')]
        for r in blind:
            t=r['prompt_text'].lower()
            self.assertFalse(any(n in t for n in surnames))
            self.assertFalse(any(n in t for n in givens))
    def test_semantic_validation(self):
        assoc=next(r for r in self.manifest if r['bank']=='association' and r['instrument'].endswith('_forced'))
        cats=list(assoc['schema']['schema']['properties'])
        good={cats[0]:60,cats[1]:30,cats[2]:10}
        self.assertEqual(validate_response(assoc,good),(True,'ok'))
        bad={cats[0]:60,cats[1]:30,cats[2]:20}
        self.assertFalse(validate_response(assoc,bad)[0])
        dec=next(r for r in self.manifest if r['bank']=='decision_main')
        self.assertEqual(validate_response(dec,{'score':70,'recommendation':'advance','confidence':80}),(True,'ok'))
    def test_identity_stable(self):
        m=self.models[0]; p=self.manifest[0]; payload=request_payload(m,p,self.study)
        self.assertEqual(request_identity(self.study['study_id'],m,p,payload),request_identity(self.study['study_id'],m,p,payload))
if __name__=='__main__': unittest.main()
