#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
parsemaps.py.

Is a simple script that extracts the coordinates of a kmz file,
add them elevation information and generates a kml file.
"""
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import argparse
import os
import re
from xml.dom import minidom
from zipfile import ZipFile
from logger import logger
import requests
import time

__author__ = 'Wenceslau Graus'
__copyright__ = '2014, Wenceslau Graus <wgraus at gmail.com>'
__license__ = 'GPL v3'
__version__ = '1.0'
__email__ = 'wgraus@gmail.com'
__docformat__ = 'restructuredtext en'


class ParseKml:
    """Kml Parser."""

    def __init__(self):
        """Get original Kml."""
        self.args = self.load_args()
        if self.args.verbose:
            logger.verbose = True
        self.ELEVATION_API = 'https://maps.googleapis.com/maps/api/elevation' \
                             '/json?locations='
        self.abs_kmz_file = self.get_file()
        self.folder = self.get_folder(self.abs_kmz_file)
        self.tag = self.get_tag()
        self.abs_kml_file = self.get_abs_kml()

    def load_args(self):
        """Load args."""
        parser = argparse.ArgumentParser(description="KMZ parse coordinates")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("kmz_file", help="the .kmz file")
        parser.add_argument("kml_tag", help="the .kml tag file")
        return parser.parse_args()

    def get_abs_kml(self):
        r = os.path.join(self.folder, '%s.kml' % self.tag)
        logger('get: %s' % r)
        return r

    def get_file(self):
        """Get abspath."""
        r = os.path.abspath(self.args.kmz_file)
        logger('get: %s' % r)
        return r

    def get_folder(self, path):
        r = os.path.dirname(path)
        logger('get: %s' % r)
        return r

    def get_tag(self):
        """Get Tag."""
        r = self.args.kml_tag
        logger('get: %s' % r)
        return r

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

    def get_elevation(self, url):
        return [x['elevation'] for x in self.get_json_dic(url)]

    def get_coord_with_elev(self, coords):
        """Get coordinates with elevation info."""
        list_elevations = []
        llista_coords = coords.split()
        for tros in list(self.chunks(llista_coords, 25)):
            e = ['%f,%f' % (float(c.split(',')[1]), float(c.split(',')[0])) for c in tros]
            url = self.ELEVATION_API + '|'.join(e)
            elev = self.get_elevation(url)
            list_elevations.extend(elev)
        coords_elev = ''
        for e, c in enumerate(llista_coords):
            coords_elev = '%s%s,%s,%s\n' % (coords_elev,
                                            c.split(',')[0],
                                            c.split(',')[1],
                                            str(list_elevations[e]))
        return coords_elev

    def get_json_dic(self, url):
        """Get dictionary from json."""
        r = requests.get(url)
        return r.json()['results']

    def get_point_with_elev(self, c):
        """Get coordinates with elevation info."""
        l = c.split(',')
        url = self.ELEVATION_API + '%s,%s' % (l[1], l[0])
        dic_coords = self.get_json_dic(url)
        return '%s,%s,%s\n' % (l[0], l[1], str(dic_coords[0]['elevation']))

    def extract(self):
        """Extract kml from kmz."""
        logger('Extract kml from kmz')
        kmz = ZipFile(self.abs_kmz_file, 'r')

        kml = None
        for l in kmz.namelist():
            site_match = re.compile('\.kml').search(l)
            if site_match:
                kml = l
                break
        kmz.extract(kml, self.folder)
        os.rename("%s/%s" % (self.folder, kml), self.abs_kml_file)

    def replace_text(self, node, new_text):
        """Replace coordinates node."""
        if node.firstChild.nodeType != node.TEXT_NODE:
            raise Exception('node does not contain text')
        node.firstChild.replaceWholeText(new_text)

    def generate_kml(self):
        """Replace original Kml."""
        logger('Generate Kml')
        doc = minidom.parse(os.path.join(self.folder, '%s.kml' % self.tag))
        for i in doc.getElementsByTagName('coordinates'):
            valor = i.firstChild.nodeValue
            if len(valor.split()) > 10:
                self.replace_text(i, self.get_coord_with_elev(valor))
            else:
                self.replace_text(i, self.get_point_with_elev(valor))
        logger('Generate File')
        with open(self.abs_kml_file, 'w') as f:
            f.write(doc.toxml())
        s = os.path.join(self.folder, '%s.kml' % self.tag)
        t = os.path.join('/var/www/html/box/kml/', '%s.kml' % self.tag)
        os.rename(s, t)

    def save_kmz(self):
        """Save KMZ."""
        s = self.abs_kmz_file
        t = os.path.join('/var/www/html/box/kmz/', os.path.basename(self.abs_kmz_file))
        os.rename(s, t)

    def run(self):
        """Run process."""
        self.load_args()
        self.extract()
        self.generate_kml()
        self.save_kmz()


def main():
    """Main."""
    pk = ParseKml()
    pk.run()


if __name__ == '__main__':
    main()
