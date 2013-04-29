#!/usr/bin/env python
from optparse import OptionParser
import requests
import json
import sys

#option required none
def option_none(option, opt, value, parser):
	if parser.rargs and not parser.rargs[0].startswith('-'):
		print "Option arg error"
		print opt, " option should be empty"
		sys.exit(2)
	setattr(parser.values, option.dest, True)
		
def check_ops_per_second(result):
	# basic bucket stats  from json
	result = result[0]
	basicStats = result['basicStats']
	print "opsPerSec:",  basicStats['opsPerSec']

def check_mem_usage(result):
	result = result[0]
	basicStats = result['basicStats']
	nodes = result['nodes']
	print "memUsed: ", basicStats['memUsed']
	nodes = dict(nodes[0])
	print "nodes"
	print "memoryFree: ", nodes['memoryFree']
	print "memoryTotal: ", nodes['memoryTotal']
	interestingStats = nodes['interestingStats']	
	print "interestingStats MemUsed: ", interestingStats['mem_used']

def check_disk_read(result):
	result = result[0]
	basicStats = result['basicStats']
	print "diskFetches: ", basicStats['diskFetches']

parser = OptionParser()
parser.disable_interspersed_args()
arg = False

#options
parser.add_option('-I', dest='ip')
parser.add_option('-u', dest='username')
parser.add_option('-p', dest='password')
parser.add_option('-b', dest='bucket')
parser.add_option('--OPS', action='callback', callback=option_none, dest='operations_per_second')
parser.add_option('--mem', action='callback', callback=option_none, dest='memoryUsage')
parser.add_option('--disk-read', action='callback', callback=option_none, dest='disk_read')
options, args = parser.parse_args()

try:
	url = ''.join(['http://', options.ip, '/pools/', options.bucket, '/buckets/'])
	r = requests.get(url, auth=(options.username, options.password))
	result = r.json()
	if options.operations_per_second:
		check_ops_per_second(result)
		arg = True
	if options.memoryUsage:
		check_mem_usage(result)
		arg = True
	if options.disk_read:
		check_disk_read(result)
		arg = True
	if not arg:
		result = json.dumps(result)
		print result

except Exception:
    print "Invalid option combination"
    print "Try '--help' for more information "
