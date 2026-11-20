from pathlib import Path
from benchmarks.task02.pipeline import clean_transactions
from benchmarks.task02.grader import grade
from run_all import FIXTURE

def test_pipeline_and_grader(tmp_path):
    inp=tmp_path/'input.csv'; inp.write_text(FIXTURE,encoding='utf-8'); original=inp.read_bytes(); c=tmp_path/'clean.csv'; r=tmp_path/'rejects.csv'; clean_transactions(inp,c,r); report=grade(c,r,inp,original); assert report['status']=='PASS',report

def test_empty_input_produces_header_only(tmp_path):
    inp=tmp_path/'input.csv'; inp.write_text('transaction_id,account_id,amount,currency,timestamp,status\n',encoding='utf-8'); c=tmp_path/'c.csv'; r=tmp_path/'r.csv'; clean_transactions(inp,c,r); assert len(c.read_text().splitlines())==1 and len(r.read_text().splitlines())==1

def test_invalid_header_rejected(tmp_path):
    inp=tmp_path/'input.csv'; inp.write_text('id,amount\n1,2\n',encoding='utf-8')
    try: clean_transactions(inp,tmp_path/'c.csv',tmp_path/'r.csv')
    except ValueError: pass
    else: raise AssertionError('invalid header must raise ValueError')


def test_duplicate_tie_keeps_first_and_timezone_normalizes(tmp_path):
    content=('transaction_id,account_id,amount,currency,timestamp,status\n'
             'X,A,1.00,usd,2026-01-01T12:00:00+02:00,settled\n'
             'X,A,9.00,usd,2026-01-01T10:00:00Z,settled\n')
    inp=tmp_path/'input.csv'; inp.write_text(content,encoding='utf-8'); c=tmp_path/'c.csv'; r=tmp_path/'r.csv'
    clean_transactions(inp,c,r)
    assert '1' in c.read_text(encoding='utf-8')
    assert '9' not in c.read_text(encoding='utf-8')

def test_naive_timestamp_is_rejected(tmp_path):
    content=('transaction_id,account_id,amount,currency,timestamp,status\n'
             'X,A,1,usd,2026-01-01T10:00:00,settled\n')
    inp=tmp_path/'input.csv'; inp.write_text(content,encoding='utf-8'); c=tmp_path/'c.csv'; r=tmp_path/'r.csv'
    clean_transactions(inp,c,r)
    assert 'invalid_timestamp' in r.read_text(encoding='utf-8')
