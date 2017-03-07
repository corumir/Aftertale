#------------------------------------
#--------import error check----------
import os
import sys
import shutil

error_list = []
try:
	import yara
except ImportError:
	error_list.append('Error on import yara: goto yara.readthedocs.io for installation instructions')
if len(error_list) > 0:
	print '\n'.join(error_list)
	exit()
#--------import error check----------
#------------------------------------

def file_driver(d):
	files = []
	for item in os.listdir(d):
		path = os.path.join(d, item)
		if os.path.isfile(path):
			files.append(os.path.abspath(path))
		else:
			files.extend(file_driver(path))			
	return files

yarafile = sys.argv[1]
input_path = sys.argv[2]

if os.path.isdir(input_path) == True:
	testfiles = file_driver(input_path)
elif os.path.isfile(input_path) == True:
	testfiles = [input_path]
else:
	print "ERROR: Data path does not exist"
	exit()

#create output directory if needed
try:
	os.makedirs('results')
except OSError:
	if not os.path.isdir('results'):
		raise

textout = []
files2move = []
rules = yara.compile(yarafile)

#test files against rules
for testfile in testfiles:
	if len(rules.match(testfile)) != 0:
		files2move.append(testfile)
		textout.append("%s: %s" % (os.path.basename(testfile), rules.match(testfile)))

#move matched files
for nextfile in files2move:
	shutil.copy(nextfile, 'results')
	
#results documentation
with open(os.path.join('results', 'results.txt'), 'w') as f:
	f.write('\n'.join(textout))
f.close()
