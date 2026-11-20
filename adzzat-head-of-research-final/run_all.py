from pathlib import Path
from tempfile import TemporaryDirectory
import csv,json
from benchmarks.task01.tools import WorkspaceTools
from benchmarks.task01.reference import solve as solve1
from benchmarks.task01.grader import grade as grade1
from benchmarks.task02.pipeline import clean_transactions
from benchmarks.task02.grader import grade as grade2
from benchmarks.task03.grader import grade as grade3
from benchmarks.task03.solution import merge_intervals

FIXTURE="""transaction_id,account_id,amount,currency,timestamp,status
T-100,A-1,10.00,usd,2026-01-01T10:00:00+00:00,settled
T-200,A-2,7.25,eur,2026-01-02T11:00:00+00:00,pending
T-300,,5.00,USD,2026-01-03T10:00:00+00:00,settled
T-100,A-1,12.5,USD,2026-01-04T10:00:00+00:00,settled
T-400,A-4,2.00,gbp,2026-01-05T10:00:00+00:00,reversed
T-500,A-5,-1.00,USD,2026-01-06T10:00:00+00:00,settled
"""

def main():
    print('TASK 01 — TOOL EXECUTION RELIABILITY')
    with TemporaryDirectory() as td:
        root=Path(td); (root/'config').mkdir(); original=(json.dumps({'api_endpoint':'https://api.example.com/v1','timeout':30,'feature_flags':{'x':True}},indent=2)+'\n').encode(); (root/'config/app.json').write_bytes(original)
        tools=WorkspaceTools(root); solve1(tools); report=grade1(root,original,tools.calls); print(json.dumps(report,indent=2)); assert report['status']=='PASS'
    print('TASK 02 — TRANSACTION CSV PIPELINE')
    with TemporaryDirectory() as td:
        root=Path(td); inp=root/'input.csv'; inp.write_text(FIXTURE,encoding='utf-8'); original=inp.read_bytes(); clean=root/'clean.csv'; rejects=root/'rejects.csv'; clean_transactions(inp,clean,rejects); report=grade2(clean,rejects,inp,original); print(json.dumps(report,indent=2)); assert report['status']=='PASS'
    print('TASK 03 — INTERVAL MERGE (STRETCH)')
    report=grade3(merge_intervals); print(json.dumps(report,indent=2)); assert report['status']=='PASS'
    print('ALL REFERENCE BENCHMARKS PASSED')

if __name__=='__main__': main()
