import unittest
import argparse
import polutils
import os
import sys

class TestTitleParser(unittest.TestCase):
    def setUp(self):
        self.files = ['en-titles.xml', 'fr-titles.xml']
        self.dirname = os.path.dirname(__file__)
        self.paths = []
        
        for file in self.files:
            if os.path.isfile(file):
                self.paths.append(file)
            elif os.path.isfile(self.dirname + "/" + file):
                self.paths.append(self.dirname + "/" + file)
            else:
                sys.exit('File not found.')
        
    def read_file(self, file):
        f = open(file, 'r')
        xml = f.read()
        f.close()
        return xml
    
    def test_parse(self):
        p = polutils.TitleParser(files=self.paths, rename_fields={'index': 'id', 'string-1': 'name'}, detect_lang=True)
        items = p.parse()
        assert len(items) == 836
        
    def test_parse_file(self):
        p = polutils.TitleParser()
        items = p.parse_file(self.paths[0])
        assert len(items) == 836
        
    def test_parse_xml(self):
        p = polutils.TitleParser()
        
        xml = self.read_file(self.paths[0])
        assert xml
        
        items = p.parse_xml(xml, 'en')
        assert len(items) == 836
        
if __name__ == '__main__':
    unittest.main()
