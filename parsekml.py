#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
from xml.dom import minidom
from mechanize import Browser
from zipfile import ZipFile

__author__ = "Wenceslau Graus"
__copyright__ = "Copyright 2013-14"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "wgraus@gmail.com"

class Parse_kml:
    ''' Kml Parser
    '''
    def __init__(self):
        ''' Get original Kml
        '''
        self.WEB_GPS = 'http://www.gpsvisualizer.com/map_input?form=googleearth'
        self.abs_kmz_file = self.get_file()
        self.folder = self.get_folder(self.abs_kmz_file)
        self.tag = self.get_tag()
        self.abs_kml_file = self.get_abs_kml()

    def get_abs_kml(self):
        r = os.path.join(self.folder, '%s.kml' % self.tag)
        self.log('get: %s' % r)
        return r

    def get_file(self):
        ''' Get abspath
        '''
        r = os.path.abspath(sys.argv[1])
        self.log('get: %s' % r)
        return r

    def get_folder(self, path):
        r = os.path.dirname(path)
        self.log('get: %s' % r)
        return r

    def get_tag(self):
        ''' Get Tag
        '''
        r = sys.argv[2]
        self.log('get: %s' % r)
        return r

    def log(self, log):
        ''' Print log
        '''
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
        os.rename("%s/%s" % (self.folder, kml), self.abs_kml_file)

    def download_kml(self):
        ''' Download file
        '''
        self.log('Downloading from gpsvisualizer')

        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        br.open(self.WEB_GPS)
        br.select_form(name='main')
        br.set_value(['0'], name='googleearth_zip')
        br.set_value(['SRTM3'], name='add_elevation')
        self.log('Send file %s/%s.kml' % (self.folder, self.tag))
        br.add_file(open(self.abs_kml_file), 'text/plain', 'file.kml',
                    name='uploaded_file_1')
        self.log('Submit')
        br.submit()

        kml_file = None
        for l in br.links():
            siteMatch = re.compile('display/').search(l.url)
            if siteMatch:
                kml_file = br.follow_link(l)
                break

        self.kml_temp_data = kml_file.get_data()
        self.log('Downloaded')

    def get_coordinates(self):
        ''' Get coordinates
        '''
        self.log('Get coordinates')
        xmldoc = minidom.parseString(self.kml_temp_data)
        itemlist = xmldoc.getElementsByTagName('coordinates')
        self.coord = itemlist[-1].firstChild.nodeValue

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
        doc = minidom.parse(os.path.join(self.folder, '%s.kml' % self.tag))
        node = doc.getElementsByTagName('coordinates')[0]
        self.replaceText(node, self.coord)
        self.log('Generate File')
        with open(self.abs_kml_file, 'w') as f:
            f.write(doc.toxml())

    def run(self):
        ''' Run process
        '''
        self.extract()
        self.download_kml()
        self.get_coordinates()
        self.generate_kml()

def main ():
        ''' main
        '''
        pk = Parse_kml()
        pk.run()

if __name__ == '__main__':
    main()
