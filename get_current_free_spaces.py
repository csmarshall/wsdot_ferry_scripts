#!/usr/bin/env python

# Script to pull the free spaces available at a given terminal
# Tested with *only* bainbridge and seattle

import simplejson
import sys
import urllib, urllib2

import argparse
from argparse import RawTextHelpFormatter
from collections import defaultdict

#def parse_trip_info(trip):
#    return [%s,%s] % ( trip['SpaceForArrivalTerminals'][0]['TerminalName'], trip['SpaceForArrivalTerminals'][0]['DriveUpSpaceCount'] )

def main():
    parser = argparse.ArgumentParser(description='Pull the number of open driveup spots at a given terminal given terminal # and wsdot API key', formatter_class=RawTextHelpFormatter, 
        epilog='TerminalIDs as of 2014-06-29\n\n'
                '#    Terminal\n'
                '=========================\n'
                '1    Anacortes\n'
                '3    Bainbridge Island\n'
                '4    Bremerton\n'
                '5    Clinton\n'
                '7    Seattle\n'
                '8    Edmonds\n'
                '9    Fauntleroy\n'
                '10    Friday Harbor\n'
                '11    Coupeville \n'
                '12    Kingston\n'
                '13    Lopez Island\n'
                '14    Mukilteo\n'
                '15    Orcas Island\n'
                '16    Point Defiance\n'
                '17    Port Townsend\n'
                '18    Shaw Island\n'
                '19    Sidney B.C.\n'
                '20    Southworth\n'
                '21    Tahlequah\n'
                '22    Vashon Island\n\n'
                'Current return codes\n'
                '-1 - WSDOT Api returned a non-2xx response\n'
                '-2 - Terminal Data returned does not match requested\n'
                '-3 - Destination given is not in requested terminal\n'
    )

    parser.add_argument('ferry_terminal', type=int, help='{TerminalID} referenced in API documentation here: http://www.wsdot.wa.gov/ferries/api/terminals/rest/help' )
    parser.add_argument('api_key', type=str, help='API Key requested from here: http://www.wsdot.wa.gov/traffic/api/')
    parser.add_argument("-d", "--destination", type=int, help="{TerminalID} of destination terminal, use for source terminals with multiple destinations eg: terminal 7, Seattle")

    args = parser.parse_args()

    base_url = 'http://www.wsdot.wa.gov/Ferries/API/Terminals/rest/terminalsailingspace/%s?apiaccesscode=%s' % (args.ferry_terminal, args.api_key)

    spaces = defaultdict(lambda: defaultdict())

    try:
        response = simplejson.loads(urllib2.urlopen(urllib2.Request(base_url)).read())

        if response['TerminalID'] != args.ferry_terminal:
            print -2
            sys.exit(1)
        else:
            for trip in response['DepartingSpaces']:
                if args.destination and (trip['SpaceForArrivalTerminals'][0]['TerminalID'] != args.destination):
                    next

                TerminalName = trip['SpaceForArrivalTerminals'][0]['TerminalName']
                DriveUpSpaceCount = trip['SpaceForArrivalTerminals'][0]['DriveUpSpaceCount']

                if not TerminalName in spaces:
                    spaces[TerminalName]['Spaces'] = DriveUpSpaceCount
                    spaces[TerminalName]['TerminalID'] = trip['SpaceForArrivalTerminals'][0]['TerminalID']
                else:
                    MaxSpaceCount = trip['SpaceForArrivalTerminals'][0]['MaxSpaceCount']
                    OverbookedSpaces = MaxSpaceCount - DriveUpSpaceCount
                    spaces[TerminalName]['Spaces'] = spaces[TerminalName]['Spaces'] - OverbookedSpaces
                    #print "%s %s" % (trip['SpaceForArrivalTerminals'][0]['TerminalName'], OverbookedSpaces)

        for TerminalName in spaces:
            if args.destination and args.destination != spaces[TerminalName]['TerminalID']:
                next
            else:
                print "\'%s\':%d" % (TerminalName,spaces[TerminalName]['Spaces']),
    except:
          print "'Closed':0"
          sys.exit(1)

if __name__ == "__main__":
    main()