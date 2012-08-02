import unittest
import argparse
import polutils
import os

class TestItemParser(unittest.TestCase):
    def setUp(self):
        self.file = 'en-items-weapons.xml'
        self.dirname = os.path.dirname(__file__)
        
        if os.path.isfile(self.file):
            self.path = self.file
        elif os.path.isfile(self.dirname + "/" + self.file):
            self.path = self.dirname + "/" + self.file
        else:
            sys.exit('File not found.')
        
    def read_file(self, file):
        f = open(file, 'r')
        xml = f.read()
        f.close()
        return xml
    
    def test_parse(self):
        p = polutils.ItemParser(files=[self.path])
        items = p.parse()
        assert len(items) == 5120
        
    def test_parse_file(self):
        p = polutils.ItemParser()
        items = p.parse_file(self.path)
        assert len(items) == 5120
        
    def test_parse_xml(self):
        p = polutils.ItemParser()
        
        xml = self.read_file(self.path)
        assert xml
        
        items = p.parse_xml(xml, 'en')
        assert len(items) == 5120
        
if __name__ == '__main__':
    unittest.main()