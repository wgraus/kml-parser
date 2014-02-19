#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
reversekml.py is a simple script that rotates the coordinates of a route
passing a kmz file from google-earth
'''
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import argparse
import os
import re
from xml.dom import minidom
from zipfile import ZipFile

__author__ = 'Wenceslau Graus'
__copyright__ = '20014, Wenceslau Graus <wgraus at gmail.com>'
__license__ = 'GPL v3'
__version__ = '1.0'
__email__ = 'wgraus@gmail.com'
__docformat__ = 'restructuredtext en'


class Parse_kml:
    ''' KMZ reverse coordinates
    '''
    def __init__(self):
        ''' Get original Kml
        '''
        self.args = self.load_args()
        self.abs_kmz_file = self.get_file()
        self.folder = self.get_folder(self.abs_kmz_file)
        self.kml_temp = 'temp.kml'
        self.kml_doc = 'doc.kml'

    def load_args(self):
        parser = argparse.ArgumentParser(description="KMZ reverse coordinates")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("kmz_file", help="the .kmz file")
        return parser.parse_args()

    def get_file(self):
        ''' Get abspath
        '''
        r = os.path.abspath(self.args.kmz_file)
        self.log('get: %s' % r)
        return r

    def get_folder(self, path):
        r = os.path.dirname(path)
        self.log('get: %s' % r)
        return r

    def log(self, log):
        ''' Print log
        '''
        if self.args.verbose:
            print "%s ..." % log

    def extract(self):
        ''' Extract kml from kmz
        '''
        self.log('Extract kml from kmz')
        kmz = ZipFile(self.abs_kmz_file, 'r')

        kml = None
        for l in kmz.namelist():
            siteMatch = re.compile('\.kml').search(l)
            if siteMatch:
                kml = l
                break
        kmz.extract(kml, self.folder)
        os.rename(os.path.join(self.folder, kml), self.kml_temp)

    def get_coordinates(self):
        ''' Get coordinates
        '''
        self.log('Get coordinates')
        kml = os.path.join(self.folder, self.kml_temp)
        with open(kml) as f:
            xmldoc = minidom.parseString(f.read())
            itemlist = xmldoc.getElementsByTagName('coordinates')
            self.coord = itemlist[0].firstChild.nodeValue

    def replaceText(self, node, newText):
        ''' Replace coordinates node
        '''
        if node.firstChild.nodeType != node.TEXT_NODE:
            raise Exception('node does not contain text')
        node.firstChild.replaceWholeText(newText)

    def generate_kml(self):
        ''' Replace original Kml
        '''
        self.log('Generate Kml')
        doc = minidom.parse(os.path.join(self.folder, self.kml_temp))
        node = doc.getElementsByTagName('coordinates')[0]
        self.replaceText(node, self.coord)
        self.log('Generate File')
        with open(self.kml_doc, 'w') as f:
            f.write(doc.toxml())
        os.remove(self.kml_temp)

    def reverse(self):
        ''' Reverse coordinates
        '''
        self.log('Reverse coordinates')
        c = self.coord.split()
        c.reverse()
        self.coord = ' '.join(c)

    def zip_kmz(self):
        '''kml to kmz
        '''
        with ZipFile(self.abs_kmz_file, 'w') as myzip:
            myzip.write(self.kml_doc)
        os.remove(self.kml_doc)

    def run(self):
        ''' Run process
        '''
        self.load_args()
        self.extract()
        self.get_coordinates()
        self.reverse()
        self.generate_kml()
        self.zip_kmz()


def main():
    ''' main
    '''
    pk = Parse_kml()
    pk.run()

if __name__ == '__main__':
    main()
