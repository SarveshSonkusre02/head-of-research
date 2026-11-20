import json
TARGET='https://api.example.com/v2'
def grade(root, original_bytes, calls):
    from pathlib import Path
    root=Path(root).resolve(); cfg=root/'config/app.json'; bak=root/'config/app.json.bak'
    checks={'config_exists':cfg.is_file(),'backup_exists':bak.is_file()}
    parsed=None
    try: parsed=json.loads(cfg.read_text(encoding='utf-8')); checks['valid_json']=True
    except (OSError,ValueError,UnicodeDecodeError): checks['valid_json']=False
    checks['backup_exact']=bak.is_file() and bak.read_bytes()==original_bytes
    if isinstance(parsed,dict):
        try: old=json.loads(original_bytes.decode('utf-8'))
        except Exception: old={}
        checks['endpoint_correct']=parsed.get('api_endpoint')==TARGET
        checks['other_fields_preserved']={k:v for k,v in parsed.items() if k!='api_endpoint'}=={k:v for k,v in old.items() if k!='api_endpoint'}
    else: checks['endpoint_correct']=checks['other_fields_preserved']=False
    names=[c.get('tool') for c in calls]
    def idx(name): return names.index(name) if name in names else -1
    ci,wi=idx('copy_file'),idx('write_file')
    checks['read_before_copy']=idx('read_file')>=0 and idx('read_file')<ci
    checks['copy_before_write']=ci>=0 and wi>ci
    copy_call=next((c for c in calls if c.get('tool')=='copy_file'),{})
    write_call=next((c for c in calls if c.get('tool')=='write_file'),{})
    checks['copied_exact_backup_path']=copy_call.get('args',{}).get('source')=='config/app.json' and copy_call.get('args',{}).get('destination')=='config/app.json.bak'
    checks['wrote_exact_config_path']=write_call.get('args',{}).get('path')=='config/app.json'
    checks['read_after_write']=wi>=0 and any(n=='read_file' and calls[j].get('args',{}).get('path')=='config/app.json' for j,n in enumerate(names) if j>wi)
    checks['json_validation_called']='validate_json' in names
    checks['within_call_budget']=len(calls)<=20
    from pathlib import PurePosixPath
    path_values=[]
    for call in calls:
        args=call.get('args',{})
        path_values.extend(v for k,v in args.items() if k in {'path','source','destination'} and isinstance(v,str))
    checks['no_observed_out_of_workspace_path']=all(not PurePosixPath(v.replace('\\','/')).is_absolute() and '..' not in PurePosixPath(v.replace('\\','/')).parts for v in path_values)
    passed=sum(checks.values()); total=len(checks)
    return {'status':'PASS' if passed==total else 'FAIL','passed':passed,'total':total,'score_percent':round(100*passed/total,1),'checks':checks,'tool_calls':len(calls)}
