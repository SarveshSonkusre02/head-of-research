import json,pytest
from benchmarks.task01.tools import WorkspaceTools,InvalidPathError,ToolError
from benchmarks.task01.reference import solve
from benchmarks.task01.grader import grade

def setup(tmp_path):
    (tmp_path/'config').mkdir(); original=(json.dumps({'api_endpoint':'v1','timeout':30,'flags':{'a':True}},indent=2)+'\n').encode(); (tmp_path/'config/app.json').write_bytes(original); return original

def test_reference_passes(tmp_path):
    original=setup(tmp_path); tools=WorkspaceTools(tmp_path); solve(tools); assert grade(tmp_path,original,tools.calls)['status']=='PASS'
@pytest.mark.parametrize('p',['../escape','config/../../escape','..\\escape'])
def test_path_traversal_blocked(tmp_path,p):
    setup(tmp_path); tools=WorkspaceTools(tmp_path)
    with pytest.raises(InvalidPathError): tools.read_file(p)
def test_copy_cannot_overwrite_backup(tmp_path):
    setup(tmp_path); (tmp_path/'config/app.json.bak').write_text('existing'); tools=WorkspaceTools(tmp_path)
    with pytest.raises(ToolError): tools.copy_file('config/app.json','config/app.json.bak')
def test_skipped_backup_fails_grader(tmp_path):
    original=setup(tmp_path); tools=WorkspaceTools(tmp_path); data=json.loads(tools.read_file('config/app.json')); data['api_endpoint']='https://api.example.com/v2'; tools.write_file('config/app.json',json.dumps(data)); report=grade(tmp_path,original,tools.calls); assert report['status']=='FAIL' and not report['checks']['backup_exists']
def test_write_without_readback_fails(tmp_path):
    original=setup(tmp_path); tools=WorkspaceTools(tmp_path); tools.read_file('config/app.json'); tools.copy_file('config/app.json','config/app.json.bak'); tools.write_file('config/app.json','{"api_endpoint":"https://api.example.com/v2","timeout":30,"flags":{"a":true}}'); report=grade(tmp_path,original,tools.calls); assert not report['checks']['read_after_write']
