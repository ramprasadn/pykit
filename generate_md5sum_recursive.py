#!/usr/bin/python
#
#
#Script to calculate md5sum recursively
#Usage: perl generate_md5sum_recursive.py -input /path/to/the/folder -output md5.txt -cpu 20 -extension fastq.gz -extension fq.gz -extension fastq
#Written by Ramprasad Neethiraj
#Developed: 17/02/2017
#Last modified: 17/02/2017

import sys,os,subprocess,argparse

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument('-i','--input', dest='input_dir', help='path to the parent/base directory', required = True)
parser.add_argument('-o','--output', dest='output_filename', help='output file name', required = True)
parser.add_argument('-c','--cpu', action='store', default="1", dest='cpu', help='maximum number of md5 instances to be run simultaneously', type=int, required = True)
parser.add_argument('-e','--extension', action='append', dest='ext', help='md5sum will be calculated for files that end with these extensions. Use this option multiple times to specify multiple file extensions', required = True)
args = parser.parse_args()

commands = []
procs = set()
out = open(args.output_filename,"w")
for root,dirnames,filenames in os.walk(args.input_dir):
    for filename in filenames:
        if any(filename.endswith(j) for j in args.ext):
	    commands.append("md5sum " + root+"/"+filename)

for command in commands:
    procs.add(subprocess.Popen(command, shell = True, stdout = out))
    if len(procs) >= args.cpu:
	os.wait()
	procs.difference_update([i for i in procs if i.poll() is not None])
out.close()
