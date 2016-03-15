#!/usr/bin/python
"""Track packages with USPS API."""
# import pyusps
from __future__ import with_statement
import os
import argparse
import urllib2
import urllib
import xml.etree.ElementTree as ET
import ConfigParser

parser = argparse.ArgumentParser(description='Track a package')
parser.add_argument('-t', '--tracking_id', metavar='TRACKING ID', type=str,
                    action='store', required=True,
                    help='Tracking id of a package.')

args = parser.parse_args()

config = ConfigParser.ConfigParser()
with open(os.environ['HOME']+'/.usps.conf') as config_h:
    config.readfp(config_h)
settings = dict(config.items('USPS'))


def get_tracking_info(tracking_id):
    """Query USPS API for tracking info."""
    base_uri = 'https://secure.shippingapis.com/ShippingAPI.dll'
    xml_string = ('<TrackRequest USERID="{}"><TrackID ID="{}"></TrackID>'
                  '</TrackRequest>'.format(settings['username'], tracking_id))
    # print xml_string
    query_form = {
        'API': 'TrackV2',
        'XML': xml_string
    }
    response = urllib2.urlopen(base_uri, urllib.urlencode(query_form.items()))
    data = response.read()
    # print data
    root = ET.fromstring(data)
    return root


def main():
    """Main."""
    root = get_tracking_info(args.tracking_id)
    trackinfos = root.findall('TrackInfo')
    if trackinfos:
        for trackinfo in trackinfos:
            print 'Tracking ID #: {}'.format(trackinfo.attrib['ID'])
            tracksummaries = trackinfo.findall('TrackSummary')
            if tracksummaries:
                for tracksummary in tracksummaries:
                    print tracksummary.text
            trackdetails = trackinfo.findall('TrackDetail')
            if trackdetails:
                trackdetails.reverse()
                print
                print 'Details:'
                for trackdetail in trackdetails:
                    print trackdetail.text

if __name__ == '__main__':
    main()
