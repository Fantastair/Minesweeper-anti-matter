import sys
import os
import deta
import pickle
import subprocess
from tempfile import NamedTemporaryFile
def dump(data):
	return b'1' + pickle.dumps(data)[::-1] + b'1'
def load(file):
	d = pickle.loads(file.read()[-2:0:-1])
	file.close()
	return d
os.environ['DETA_PROJECT_KEY'] = 'c0s5rmynt5a_S8QgPj2cgftLoy63dp79k2rW7x3ngsFm'
d = deta.Deta()
drive = d.Drive('Data')
drive.put('sweepmine/updater.dict', data=dump({}))
argv = sys.argv
try:
	if len(argv) == 1:
		sys.exit()
	else:
		import os
		import deta
		import pickle
		import subprocess
		from tempfile import NamedTemporaryFile
		def load(file):
			d = pickle.loads(file.read()[-2:0:-1])
			file.close()
			return d
		os.environ['DETA_PROJECT_KEY'] = 'c0s5rmynt5a_S8QgPj2cgftLoy63dp79k2rW7x3ngsFm'
		d = deta.Deta()
		drive = d.Drive('Data')
		path = load(drive.get('sweepmine/updater.dict')).get(argv[1])
		if path is not None:
			f = NamedTemporaryFile(delete=False)
			f_ = drive.get(f'sweepmine/{path}')
			f.write(f_.read())
			f_.close()
			f.close()
			subprocess.check_output([f.name])
except:
	import time
	import traceback
	with open('_internal/hsarc.txt', 'a+') as f:
		print('==========', time.asctime(), '==========\n', traceback.format_exc(), file=f)
