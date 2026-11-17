#!/usr/bin/env python3
"""Real Calendar QML, isolated PIM/config, all supported UI languages and sizes.
Usage: run-typography-review.py BUILD [OUTPUT_DIRECTORY] [language ...]
Without OUTPUT_DIRECTORY, results use a temporary directory cleaned on exit.
A supplied directory retains results; its language subdirectories must not exist.
"""
from pathlib import Path
import os,sys,subprocess,shutil,json,tempfile
repo=Path(__file__).resolve().parents[3]
build=Path(sys.argv[1]).resolve()
output = sys.argv[2] if len(sys.argv)>2 else os.environ.get('KOS_TEST_OUTPUT_DIR')
temporary = tempfile.TemporaryDirectory(prefix='calendar-typography-') if not output else None
scratch=Path(temporary.name if temporary else output).resolve()
scratch.mkdir(parents=True,exist_ok=True)
bus_config=scratch/'session-bus.conf'
# Test services are launched explicitly. Avoid leaving autoactivated desktop portals behind.
bus_config.write_text('<busconfig><type>session</type><listen>unix:tmpdir=/tmp</listen><auth>EXTERNAL</auth><policy context="default"><allow own="*"/><allow send_destination="*"/><allow receive_sender="*"/></policy></busconfig>')
langs=sys.argv[3:] or ['zh_CN','en_US','pt_BR']
assert all(lang in ('zh_CN','en_US','pt_BR') for lang in langs)
results=[]
for lang in langs:
 work=scratch/lang;work.mkdir()  # Refuse to overwrite a prior test or user profile.
 qml=work/'qml';qml.mkdir(exist_ok=True)
 for p in (repo/'apps/org.nextks.calendar/qml').iterdir():
  if p.suffix in ('.qml','.js'):shutil.copy2(p,qml/p.name)
 text=(qml/'Main.qml').read_text().replace('import QtQuick\n','import QtQuick\nimport QtTest\n',1)
 fixture=Path(__file__).with_name('TypographyReview.qml.inc').read_text().replace('@OUT@',str(work).replace('\\','\\\\').replace('"','\\"'))
 (qml/'Main.qml').write_text(text.replace('    neutralTypography: true',fixture+'\n    neutralTypography: true',1))
 env=dict(os.environ,QT_QPA_PLATFORM=os.environ.get('KOS_TEST_QPA','offscreen'),QT_QUICK_BACKEND=os.environ.get('KOS_TEST_BACKEND','software'),QT_QUICK_CONTROLS_STYLE='Basic',QT_IM_MODULE='',LANG=lang+'.UTF-8',LC_ALL=lang+'.UTF-8',LANGUAGE=lang,QT_SCALE_FACTOR=os.environ.get('KOS_TEST_SCALE','1'),KOS_PIM_STORAGE_DIR=str(work/'pim'))
 for key in ['XDG_CONFIG_HOME','XDG_DATA_HOME','XDG_CACHE_HOME','XDG_STATE_HOME']:
  p=work/key.lower();p.mkdir(exist_ok=True);env[key]=str(p)
 if env['QT_QPA_PLATFORM']=='offscreen':
  run=work/'runtime';run.mkdir(mode=0o700,exist_ok=True);env['XDG_RUNTIME_DIR']=str(run)
 with (work/'session.py').open('w') as f:
  f.write('import subprocess,sys\nservice=subprocess.Popen('+repr([str(build/'services/pim-service/kos-pim-service')])+',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\ntry:\n result=subprocess.run('+repr([str(build/'apps/org.nextks.calendar/kos-calendar'),'--watch-qml',str(qml)])+',timeout=65)\n sys.exit(result.returncode)\nfinally:\n service.terminate()\n service.wait(timeout=5)\n')
 with (work/'review.log').open('w') as log:
  result=subprocess.run(['dbus-run-session','--config-file='+str(bus_config),'--',sys.executable,str(work/'session.py')],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=75)
 text=(work/'review.log').read_text();passed=result.returncode==0 and 'CALENDAR_TYPOGRAPHY_PASSED' in text and 'FAIL!' not in text and not any(e in text for e in ['ReferenceError','TypeError','is not a type','failed to load component','Binding loop'])
 results.append(dict(language=lang,passed=passed,returncode=result.returncode))
 print(lang,passed,flush=True)
 if not passed:print(text[-6000:],flush=True)
(scratch/'typography-results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
