# Copyright (c) 2014, Martin P. Hellwig, All Rights Reserved.
"""
"""
import os
import docutils.core
import BeautifulSoup
import datetime

SOURCE = "https://bitbucket.org/towards_self_sufficiency/data/src/default"
_FILE = os.path.abspath(__file__)
_CODE = os.path.dirname(_FILE)
FOLDER = os.path.dirname(_CODE)

SITE='site'

_REPLACERS = [['h7', 'h8'],
              ['h6', 'h7'],
              ['h8', 'h7'],
              ['h5', 'h6'],
              ['h4', 'h5'],
              ['h3', 'h4'],
              ['h2', 'h3'],
              ['h1', 'h2']]

def make_site_html(path):
    file_name = os.path.join(FOLDER, SITE, path) 
    with open(file_name, 'r') as file_open:
        source = ''.join(file_open.readlines())
        target = docutils.core.publish_string(source=source, writer_name='html')
    
    page = BeautifulSoup.BeautifulSoup(target)
    for find, replace in _REPLACERS:
        for found in page.findAll(find):
            found.name = replace
    
    text = list() 
    tmp = list()
    for entry in page.body:
        tmp.append(unicode(entry))
        
    part = ''.join(tmp)

    for line in part.split('\n'):
        if len(line.strip()) > 0:            
            if not 'class="title"' in line:
                text.append(line)
                    
    text.append('<br/><br/>')
    now =  datetime.datetime.utcnow()
    now = now.strftime('%d %B %Y at %H:%M UTC')
    source = '/'.join([SOURCE, SITE, path])
    link = '<i> Page generated on %s from <a href="%s"> %s</a> </i>' 
    link = link % (now, source, path)
    text.append(link)
    
    html = '\n'.join(text) 
    return(page.title.text, html)
    
    

if __name__ == '__main__':
    print(make_site_html('articles/risk_scenario.rst')[1])