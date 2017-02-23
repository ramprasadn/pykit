#!/usr/bin/python
#
#
#Script to calculate md5sum recursively
#Usage: perl swap_notifications.py -t 30 -e emails.txt -s 3600 -m random@gmail.com
####emails.txt should contain one email id per line. For example,
#random@gmail.com
#random@yahoo.com
####
#Written by Ramprasad Neethiraj
#Developed: 23/02/2017
#Last modified: 23/02/2017

import subprocess,argparse,time,smtplib

parser = argparse.ArgumentParser()
parser.add_argument('-t','--threshold', dest='thresh', help='send a notification if usage exceeds this limit (GB)', required = True, type = int)
parser.add_argument('-e','--emails', dest='emails', help='a file containing a list of emails', required = True)
parser.add_argument('-s','--sleep_time', dest='sleeptime', help='time to wait until the next memory check after sending an warning email (in seconds)', required = True, type = int)
parser.add_argument('-m','--sender_mail', dest='sendermail', help='email id of the sender', required = True)
args = parser.parse_args()

eids = {}
with open(args.emails) as emailfile:
    for line in emailfile:
        eids[line.strip()]=""

while True:
    out, err = subprocess.Popen("free -g", shell = True, stdout = subprocess.PIPE).communicate()
    for line in out.split("\n"):
        l = line.strip().split()
        if l and l[0] == "total":
            ind = l.index("used")
        elif l and l[0] == "Swap:":
            used = l[ind+1]
    if int(used) < args.thresh:
        pass
    else:
        for j in eids:
            s = smtplib.SMTP('localhost')
            mess = 'Subject: {}\n\n{}'.format("Swap usage has exceeded "+str(args.thresh)+"G", "Swap usage has exceeded "+str(args.thresh)+"G")
            s.sendmail(args.sendermail,j,mess)
            s.quit()
        time.sleep(args.sleeptime)
