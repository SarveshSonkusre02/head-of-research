import csv
from pathlib import Path
from .pipeline import FIELDS,REJECT_FIELDS

def _rows(path):
    with open(path,'r',encoding='utf-8',newline='') as f: return list(csv.DictReader(f))

def grade(clean_path,rejects_path,input_path,original_bytes):
    c=Path(clean_path); r=Path(rejects_path); inp=Path(input_path)
    checks={'clean_file_exists':c.is_file(),'rejects_file_exists':r.is_file(),'input_unchanged':inp.read_bytes()==original_bytes}
    clean=_rows(c) if c.is_file() else []; rejects=_rows(r) if r.is_file() else []
    checks['clean_header_exact']=c.is_file() and list(clean[0].keys())==FIELDS if clean else c.is_file() and c.read_text(encoding='utf-8').splitlines()[0].split(',')==FIELDS
    checks['reject_header_exact']=r.is_file() and r.read_text(encoding='utf-8').splitlines()[0].split(',')==REJECT_FIELDS
    ids=[x['transaction_id'] for x in clean]
    checks['unique_transaction_ids']=len(ids)==len(set(ids))
    checks['sorted_by_transaction_id']=ids==sorted(ids)
    checks['valid_amounts']=all(float(x['amount'])>0 for x in clean)
    checks['currency_uppercase']=all(x['currency'].isalpha() and x['currency'].isupper() and len(x['currency'])==3 for x in clean)
    checks['allowed_statuses']=all(x['status'] in {'SETTLED','PENDING','REVERSED'} for x in clean)
    checks['reject_rows_have_reason']=all(bool(x['reason']) and x['source_row'].isdigit() for x in rejects)
    checks['fixture_accepted_ids']={x['transaction_id'] for x in clean}=={'T-100','T-200','T-400'}
    checks['fixture_rejected_source_rows']={x['source_row'] for x in rejects}=={'3','6'}
    checks['latest_duplicate_wins']=next((x['amount'] for x in clean if x['transaction_id']=='T-100'),None)=='12.5'
    checks['reject_reasons_exact']={x['source_row']:x['reason'] for x in rejects}=={'3':'missing_account_id','6':'invalid_amount'}
    checks['canonical_timestamp_utc']=all(x['timestamp'].endswith('Z') for x in clean)
    checks['clean_currency_values']={x['currency'] for x in clean}=={'USD','EUR','GBP'}
    passed=sum(checks.values()); total=len(checks)
    return {'status':'PASS' if passed==total else 'FAIL','passed':passed,'total':total,'score_percent':round(100*passed/total,1),'checks':checks}
