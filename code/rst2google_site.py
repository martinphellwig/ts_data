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

def _reduce_headers(page):
    found = list()
    for number in range(1,7):
        header = 'h%s' % number
        if len(page.findAll(header)) > 0:
            found.append(header)
    
    found.sort()
    
    replacers = zip(found, range(2, 2+len(found)))
    replacers.sort(reverse=True)
    for find, replace in replacers:
        replace = 'h%s' % replace
        for fetched in page.findAll(find):
            fetched.name = replace

def make_site_html(path):
    file_name = os.path.join(FOLDER, SITE, path) 
    with open(file_name, 'r') as file_open:
        source = ''.join(file_open.readlines())
        target = docutils.core.publish_string(source=source, writer_name='html')
    
    page = BeautifulSoup.BeautifulSoup(target)
    _reduce_headers(page)
    
    text = list() 
    tmp = list()
    for upper_div in page.body:
        for entry in upper_div:
            unicode_entry = unicode(entry) 
            tmp.append(unicode_entry)
        
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
    rv = make_site_html('articles/risk_assessment.rst')[1]
    print(rv)
    