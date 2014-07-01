#!/usr/bin/env python

# Script to pull the free spaces available at a given terminal
# Tested with *only* bainbridge and seattle

import simplejson
import sys
import urllib, urllib2

import argparse
from argparse import RawTextHelpFormatter


def main():
	parser = argparse.ArgumentParser(description='Pull the number of open driveup spots at a given terminal given terminal # and wsdot API key', formatter_class=RawTextHelpFormatter, 
		epilog='TerminalIDs as of 2014-06-29\n\n'
			   '# 	Terminal\n'
			   '=========================\n'
			   '1	Anacortes\n'
			   '3	Bainbridge Island\n'
			   '4	Bremerton\n'
			   '5	Clinton\n'
			   '7	Seattle\n'
			   '8	Edmonds\n'
			   '9	Fauntleroy\n'
			   '10	Friday Harbor\n'
			   '11	Coupeville \n'
			   '12	Kingston\n'
			   '13	Lopez Island\n'
			   '14	Mukilteo\n'
			   '15	Orcas Island\n'
			   '16	Point Defiance\n'
			   '17	Port Townsend\n'
			   '18	Shaw Island\n'
			   '19	Sidney B.C.\n'
			   '20	Southworth\n'
			   '21	Tahlequah\n'
			   '22	Vashon Island\n'
	)

	parser.add_argument('ferry_terminal', type=int, help='{TerminalID} referenced in API documentation here: http://www.wsdot.wa.gov/ferries/api/terminals/rest/help' )
	parser.add_argument('api_key', type=str, help='API Key requested from here: http://www.wsdot.wa.gov/traffic/api/')

	args = parser.parse_args()

	base_url = 'http://www.wsdot.wa.gov/Ferries/API/Terminals/rest/terminalsailingspace/%s?apiaccesscode=%s' % (args.ferry_terminal, args.api_key)

	try:
		response = urllib2.urlopen(urllib2.Request(base_url)).read()
		print simplejson.loads(response)['DepartingSpaces'][0]['SpaceForArrivalTerminals'][0]['DriveUpSpaceCount']
	except:
		print -1
		sys.exit(1)

	#print simplejson.loads((urllib2.urlopen(urllib2.Request(base_url))).read())['DepartingSpaces'][0]['SpaceForArrivalTerminals'][0]['DriveUpSpaceCount']

if __name__ == "__main__":
    main()