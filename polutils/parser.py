import sys
import re
from os.path import basename
from lxml import etree
from StringIO import StringIO

class TitleParser(object):
    
    things = {}
    
    def __init__(self, files=None, fields=None, rename_fields=None, 
                 detect_lang=False, lang_sep="_"):
        
         # Desired fields
        if fields is None:
            # All fields will be taken
            self.fields = []
        else:
            self.fields = fields
          
        # XML files to be parsed
        self.files = files

        self.lang_fields = ['string-1', 'string-2', 'string-3', 'string-4']
        self.rename_fields = rename_fields
        self.detect_lang = detect_lang
        self.lang_sep = lang_sep
        
        # Used for the self.titles dict key
        self.id_field = 'index'
        if rename_fields:
            self.fields.extend(rename_fields.keys())
            if rename_fields.get(self.id_field):
                self.id_field = rename_fields[self.id_field]
                
        self.fields = set(self.fields)
    
    def parse(self, lang=None):
        for file in self.files:
            self.parse_file(file, lang=lang)
        return self.things
    
    def parse_file(self, file, lang=None):
        if lang is None and self.detect_lang:
             # Determine lang by prefix of file
            m = re.match(r"^([a-z]+)[\-_\s\.].*", basename(file), re.IGNORECASE)
            if m:
                lang = m.group(1)
                if lang not in ('en', 'de', 'jp', 'fr'):
                    lang = None
        try:
            f = open(file, 'r')
        except IOError as e:
            sys.exit("Could not open file for reading: %s" % file)
            
        xml = f.read()
        f.close()
        return self.parse_xml(xml, lang)
    
    def parse_xml(self, xml, lang=None):
        tree = etree.parse(StringIO(xml))
        context = etree.iterparse(StringIO(xml), events=('start', 'end'))
        
        # The name fields are different for each lang, this maps them
        name_fields = { 'en': 'string-1', 'jp': 'string-1', 'fr': 'string-3', 'de': 'string-2'}
        things = self.things
        
        thing = {}
        
        for action, elem in context:
            if elem.tag == 'thing-list':
                continue
            
            # Begin new item
            if elem.tag == 'thing':
                if action == 'start':
                    thing = {}
                elif action == 'end':
                    if thing[self.id_field] in things:
                        things[thing[self.id_field]].update(thing)
                    else:
                        things[thing[self.id_field]] = thing
            
            name = elem.attrib.get('name')
            
            # Kind of a hack
            if lang and name_fields[lang] == name:
                name = 'string-1'
                
            if not name or (name not in self.fields and self.fields):
                continue
            
            if elem.text is None:
                text = ""
            else:
                text = elem.text
            
            if isinstance(text, str):
                text = text.strip()
                
            if self.rename_fields and name in self.rename_fields:
                newname = self.rename_fields[name]
            else:
                newname = name
                
            if lang and name in self.lang_fields:
                thing[lang + self.lang_sep + newname] = text
            else:
                thing[newname] = text
                
        self.things = things
        return self.things
    
class KeyItemParser(object):
    pass

class ItemParser(object):
    
    # Parsed items
    items = {}
    
    def __init__(self, files=None, fields=None, convert_hex=False, 
                 rename_fields=None, detect_lang=False, lang_sep="_"):
        # Desired fields
        if fields is None:
            # All fields will be taken
            self.fields = []
        else:
            self.fields = fields
          
        # XML files to be parsed
        self.files = files
        self.convert_hex = convert_hex
        self.hex_fields = ['type', 'resource-id', 'valid-targets', 'slots', 
                           'races', 'jobs', 'element', 'flags', 'skill']
    
        self.lang_fields = ['name', 'description', 'log-name-singular', 'log-name-plural']
        self.rename_fields = rename_fields
        self.detect_lang = detect_lang
        self.lang_sep = lang_sep
        
        # Used for the self.items dict key
        self.id_field = 'id'
        if rename_fields:
            self.fields.extend(rename_fields.keys())
            if rename_fields.get('id'):
                self.id_field = rename_fields['id']
                
            
        self.fields = set(self.fields)
            
        
    def parse(self, lang=None):
        for file in self.files:
            self.parse_file(file, lang=lang)
        return self.items
    
    def parse_file(self, file, lang=None):
        if lang is None and self.detect_lang:
             # Determine lang by prefix of file
            m = re.match(r"^([a-z]+)[\-_\s\.].*", basename(file), re.IGNORECASE)
            if m:
                lang = m.group(1)
                if lang not in ('en', 'de', 'jp', 'fr'):
                    lang = None
        try:
            f = open(file, 'r')
        except IOError as e:
            sys.exit("Could not open file for reading: %s" % file)
            
        xml = f.read()
        f.close()
        return self.parse_xml(xml, lang)
        
    def parse_xml(self, xml, lang=None):
        tree = etree.parse(StringIO(xml))
        context = etree.iterparse(StringIO(xml), events=('start', 'end'))
        
        items = self.items
        
        item = {}
        skip = True
        
        for action, elem in context:
            if elem.tag == 'thing-list':
                continue
            
            # Begin new item
            if elem.tag == 'thing' and elem.attrib.get('type') == 'Item':
                if action == 'start':
                    skip = False
                    item = {}
                elif action == 'end':
                    if item[self.id_field] in items:
                        items[item[self.id_field]].update(item)
                    else:
                        items[item[self.id_field]] = item
                
            # Skip until beginning of item
            if skip:
                continue
            
            # Reached graphic, which is the end
            if elem.tag == 'thing' and elem.attrib.get('type') == 'Graphic' and action == 'start':
                skip = True
                continue
            
            if elem.tag == 'field' and action == 'start':
                continue
            
            name = elem.attrib.get('name')
            
            if not name or (name not in self.fields and self.fields):
                continue
            
            if elem.text is None:
                text = ""
            else:
                text = elem.text
            
            if isinstance(text, str):
                text = text.strip()
                    
            if self.convert_hex and name in self.hex_fields:
                text = int(text, 16)
                
            if self.rename_fields and name in self.rename_fields:
                newname = self.rename_fields[name]
            else:
                newname = name
                
            if lang and name in self.lang_fields:
                item[lang + self.lang_sep + newname] = text
            else:
                item[newname] = text
                
        self.items = items
        return self.items
                                             