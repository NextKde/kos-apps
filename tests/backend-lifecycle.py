from pathlib import Path
import os, subprocess, socket, json, time, hashlib, tempfile, sys
root=Path(__file__).resolve().parent.parent
exe=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'tmp/prefix/bin/kos-weather-backend'
(root/'tmp').mkdir(exist_ok=True)
workspace=tempfile.TemporaryDirectory(prefix='backend-',dir=root/'tmp')
base=Path(workspace.name)
# Make sentinel core data and explicitly expose its locations to the helper.
core=base/'core';core.mkdir(exist_ok=True)
(core/'state.json').write_text('{"sentinel":"do not change"}')
(core/'kos-data.sock').write_text('sentinel, not a real socket')
before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in core.iterdir()}
env=os.environ.copy();env.update(KOS_DATA_SOCKET=str(core/'kos-data.sock'),XDG_STATE_HOME=str(core))
state=base/'standalone-backend'; runtime=base/'runtime';runtime.mkdir(exist_ok=True); sock=runtime/'weather.sock'
args=[str(exe),'--socket',str(sock),'--state-dir',str(state)]
log=open(base/'helper.log','wb')
p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=log,stderr=log,env=env)
def connect():
 end=time.monotonic()+5
 while True:
  try:
   c=socket.socket(socket.AF_UNIX);c.settimeout(5);c.connect(str(sock));return c,c.makefile('rwb',buffering=0)
  except OSError:
   if time.monotonic()>end:raise
   time.sleep(.03)
def read(f):return json.loads(f.readline())
def request(f,op,payload={}):
 rid=str(time.monotonic_ns());f.write((json.dumps(dict(version=1,requestId=rid,operation=op,payload=payload))+'\n').encode())
 for _ in range(20):
  r=read(f)
  if r.get('requestId')==rid:return r
 raise AssertionError('response missing')
try:
 c,f=connect();c2,f2=connect()
 assert read(f)['event']=='weather.changed'
 assert read(f2)['event']=='weather.changed'
 r=request(f,'weather.snapshot');assert r['ok'] and r['result']['weather']['schemaVersion']==1
 assert not request(f,'metrics.snapshot')['ok']
 # A second app must not steal the socket or state lock.
 other=subprocess.run(args,stdin=subprocess.DEVNULL,capture_output=True,env=env,timeout=5)
 assert other.returncode!=0 and b'already active' in other.stderr
 # Removing final city must publish to every client without using network data.
 city=r['result']['weather']['location']['id']
 assert request(f,'weather.remove-location',{'id':city})['ok']
 assert read(f2)['event']=='weather.changed'
 assert request(f2,'weather.snapshot')['result']['weather']['locations']==[]
 p.stdin.close();assert p.wait(timeout=5)==0
 assert not sock.exists()
 f.close();f2.close();c.close();c2.close()
 saved=json.loads((state/'state.json').read_text());assert list(saved)==['weather'] and saved['weather']['locations']==[]
 # Parent crash closes the pipe without orderly helper termination.
 parent_script='''import subprocess,sys,time\np=subprocess.Popen(sys.argv[1:],stdin=subprocess.PIPE)\nprint(p.pid,flush=True)\ntime.sleep(30)'''
 parent=subprocess.Popen(['python3','-c',parent_script,*args],stdout=subprocess.PIPE,stderr=log,env=env)
 helper_pid=int(parent.stdout.readline());c,f=connect();read(f)
 parent.kill();parent.wait(timeout=5)
 end=time.monotonic()+5
 while sock.exists() and time.monotonic()<end:time.sleep(.03)
 assert not sock.exists(),'helper survived owner crash'
 f.close();c.close()
 for bad in [[],['--socket',str(core/'kos-data.sock'),'--state-dir',str(state)],['--socket',str(sock),'--state-dir',str(core)]]:
  r=subprocess.run([str(exe),*bad],capture_output=True,timeout=5,env=env);assert r.returncode!=0 and b'required' in r.stderr
 assert before=={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in core.iterdir()}
 print('PASS: weather protocol, all-client notifications, exclusive lock, EOF shutdown, parent-crash exit, saved empty city list, invalid paths, core sentinels unchanged')
finally:
 if p.poll() is None:p.kill();p.wait()
 log.close()
 workspace.cleanup()
