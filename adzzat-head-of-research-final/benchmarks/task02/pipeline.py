from __future__ import annotations
import csv, re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

FIELDS=['transaction_id','account_id','amount','currency','timestamp','status']
REJECT_FIELDS=['source_row','reason']+FIELDS
STATUSES={'SETTLED','PENDING','REVERSED'}

def _normalise(row):
    errors=[]; out={k:(row.get(k) or '').strip() for k in FIELDS}
    if not out['transaction_id']: errors.append('missing_transaction_id')
    if not out['account_id']: errors.append('missing_account_id')
    try:
        amount=Decimal(out['amount'])
        if not amount.is_finite() or amount<=0: raise InvalidOperation
        out['amount']=format(amount.normalize(),'f')
    except (InvalidOperation,ValueError): errors.append('invalid_amount')
    if not re.fullmatch(r'[A-Za-z]{3}',out['currency']): errors.append('invalid_currency')
    else: out['currency']=out['currency'].upper()
    try:
        ts=datetime.fromisoformat(out['timestamp'].replace('Z','+00:00'))
        if ts.tzinfo is None or ts.utcoffset() is None: raise ValueError
        out['timestamp']=ts.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError: errors.append('invalid_timestamp')
    out['status']=out['status'].upper()
    if out['status'] not in STATUSES: errors.append('invalid_status')
    return out,errors

def clean_transactions(input_csv,clean_csv,rejects_csv):
    accepted=[]; rejected=[]
    with open(input_csv,'r',encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames is None or set(reader.fieldnames)!=set(FIELDS):
            raise ValueError('input header must contain exactly the six required columns')
        for source_row,row in enumerate(reader,start=1):
            normalized,errors=_normalise(row)
            if errors:
                rejected.append({'source_row':source_row,'reason':'; '.join(errors),**{k:(row.get(k) or '') for k in FIELDS}})
            else:
                normalized['_source_row']=source_row
                accepted.append(normalized)
    # Latest timestamp wins; stable input order wins ties.
    by_id={}
    for row in accepted:
        key=row['transaction_id']; current=by_id.get(key)
        if current is None or row['timestamp']>current['timestamp']:
            by_id[key]=row
    final=[]
    for key in sorted(by_id):
        row=by_id[key]; final.append({k:row[k] for k in FIELDS})
    with open(clean_csv,'w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS); writer.writeheader(); writer.writerows(final)
    with open(rejects_csv,'w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=REJECT_FIELDS); writer.writeheader(); writer.writerows(rejected)
    return {'accepted':len(final),'rejected':len(rejected),'duplicates_removed':len(accepted)-len(final)}
