from __future__ import annotations
import json, shutil
from pathlib import Path

class ToolError(Exception): pass
class InvalidPathError(ToolError): pass
class ToolValidationError(ToolError): pass

class WorkspaceTools:
    def __init__(self, root, max_calls=20):
        self.__root = Path(root).resolve()
        self.__root.mkdir(parents=True, exist_ok=True)
        self.max_calls = max_calls
        self.calls = []
    def _record(self, name, args):
        if len(self.calls) >= self.max_calls: raise ToolError('tool-call budget exceeded')
        self.calls.append({'tool':name,'args':dict(args)})
    def _path(self, rel):
        if not isinstance(rel,str) or not rel.strip(): raise ToolValidationError('path must be non-empty')
        p=(self.__root / rel.replace('\\', '/')).resolve()
        try: p.relative_to(self.__root)
        except ValueError as e: raise InvalidPathError('path escapes workspace') from e
        return p
    def list_files(self, path='.'):
        self._record('list_files',{'path':path}); p=self._path(path)
        if not p.is_dir(): raise ToolError('directory does not exist')
        return sorted(x.relative_to(self.__root).as_posix() for x in p.rglob('*') if x.is_file())
    def read_file(self,path):
        self._record('read_file',{'path':path}); p=self._path(path)
        if not p.is_file(): raise ToolError('file does not exist')
        return p.read_text(encoding='utf-8')
    def write_file(self,path,content):
        self._record('write_file',{'path':path})
        if not isinstance(content,str): raise ToolValidationError('content must be text')
        p=self._path(path)
        if p.exists() and p.is_dir(): raise ToolError('cannot write to directory')
        p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8')
        return {'written':True}
    def copy_file(self,source,destination):
        self._record('copy_file',{'source':source,'destination':destination})
        s,d=self._path(source),self._path(destination)
        if not s.is_file(): raise ToolError('source file does not exist')
        if d.exists(): raise ToolError('destination already exists')
        d.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(s,d)
        return {'copied':True}
    def validate_json(self,path):
        self._record('validate_json',{'path':path}); p=self._path(path)
        try: json.loads(p.read_text(encoding='utf-8'))
        except (OSError,ValueError,UnicodeDecodeError) as e: return {'valid':False,'error':str(e)}
        return {'valid':True}
