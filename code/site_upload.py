# Copyright (c) 2014, Martin P. Hellwig, All Rights Reserved.
"""
"""
import os
import site_generate

SOURCE='2wards2s-test-alpha'
SITE='towardsselfsufficiency'
SCOPES=['http://sites.google.com/feeds/', 'https://sites.google.com/feeds/']

if 'GOOGLE_SITE_USER' not in os.environ:
    raise(ValueError('Set GOOGLE_SITE_USER in environemt'))

elif 'GOOGLE_SITE_PASS' not in os.environ:
    raise(ValueError('Set GOOGLE_SITE_PASS in environemt'))

EMAIL=os.environ['GOOGLE_SITE_USER']
PASSWORD=os.environ['GOOGLE_SITE_PASS']

from gdata.sites import client 
CLIENT = client.SitesClient(source=SOURCE, site=SITE)
#CLIENT.http_client.debug = True
CLIENT.client_login(email=EMAIL, password=PASSWORD, source=SOURCE)



def delete_pages():
    print('# Deleting all existing pages')
    uri = CLIENT.MakeContentFeedUri() + '?kind=webpage'
    feed = CLIENT.get_content_feed(uri=uri)
        
    for entry in feed.entry:
        if entry.title.text != '-_cfg':
            print '- %s [%s]' % (entry.title.text, entry.Kind())
            CLIENT.delete(entry)
    print('# ! Done !')

def create_pages():    
    print('# Creating pages')
    
    paths = dict()
    sites = site_generate.generate()
    
    for path, title, html in sites:
        print(' - %s %s' % (path, title))
        if path == ['']:
            CLIENT.CreatePage('webpage', title, html=html)
        else:
            for index in range(1, len(path)+1):
                part = path[:index]
                if str(part) not in paths:
                    subtitle = part[-1]
                    
                    if index == 1:
                        entry = CLIENT.CreatePage('webpage', title=subtitle)
                        paths[str(part)] = entry
                    else:
                        parent = paths[str(part[:-1])]
                        entry = CLIENT.CreatePage('webpage', title=subtitle, parent=parent)
                        paths[str(part)] = entry
                                            
            parent = paths[str(path)]
            CLIENT.CreatePage('webpage', title, html=html, parent=parent)
    print('# ! Done !')
            

def main():
    delete_pages()
    create_pages()
    

if __name__ == '__main__':
    main()
