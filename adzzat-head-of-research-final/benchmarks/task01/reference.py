import json
TARGET='https://api.example.com/v2'
def solve(tools):
    if 'config/app.json' not in tools.list_files('.'): raise FileNotFoundError('config/app.json missing')
    original=tools.read_file('config/app.json')
    data=json.loads(original)
    if not isinstance(data,dict): raise ValueError('config root must be object')
    tools.copy_file('config/app.json','config/app.json.bak')
    data['api_endpoint']=TARGET
    tools.write_file('config/app.json',json.dumps(data,indent=2)+'\n')
    updated=tools.read_file('config/app.json')
    if json.loads(updated).get('api_endpoint') != TARGET: raise RuntimeError('read-back mismatch')
    if not tools.validate_json('config/app.json')['valid']: raise RuntimeError('invalid JSON')
    return {'status':'completed'}
