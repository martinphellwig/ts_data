# Copyright (c) 2014, Martin P. Hellwig, All Rights Reserved.
"""
"""
import os
import rst2google_site

BASE = os.path.join(rst2google_site.FOLDER, rst2google_site.SITE)

def generate():
    tmp = list()
    for triple in os.walk(BASE):
        basis = triple[0]
        files = triple[2]
        basis = basis[len(BASE)+1:]
        for name in files:
            path = os.path.join(basis, name)
            hier = basis.split(os.path.sep)
            print('- %s' % name)
            title, content = rst2google_site.make_site_html(path)
            tmp.append((hier, title, content))
    return(tmp)

def main():
    from pprint import pprint
    pprint(generate())

if __name__ == '__main__':
    main()