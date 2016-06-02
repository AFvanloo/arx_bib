# This module is part of the program for interfacing arxiv URLs, getting relevant data, and writing it in a bibtex file
#written by arjan van loo <arjanvanloo@gmail.com>

#for debugging

def readfile(path):
    
    #raw text
    bibfile = open(path, 'r')
    bibtext = bibfile.read()
    bibfile.close()

    #3lines
    bibfile = open(path, 'r')
    biblines = bibfile.readlines()
    bibfile.close()
    return biblines, bibtext

def check_key(path, key):
    '''
    checks the bibtexkey, and tries alternatives
    '''
    textlines, text = readfile(path)
    #find key, suggest alternatives if not found
    
    if text.count(key) ==0 :
        return key

    #probing alternatives
    for i in range(97,123):
        if text.count(key+chr(i))==0:
            return key+chr(i)

    #In case nothing worked:
    return 'False'

def make_entry(title, url, authors, year, journal, bibtexkey, file, owner, timestamp):
    entry = build_entry(title, url, authors, year, journal, bibtexkey, file, owner, timestamp)
    add_entry(file, entry)


def build_entry(title, url, authors, year, journal, bibtexkey, file, owner, timestamp):
    '''
    builds an entry as a list of strings, to be used with writelines
    '''
    bibentry = []
    bibentry.append('@Article{'+bibtexkey+',\n')
    bibentry.append('  author = {'+authors+'},\n')
    bibentry.append('  title = {'+title+'},\n')
    bibentry.append('  journal = {'+journal+'},\n')
    bibentry.append('  year = {'+year+'},\n')
    bibentry.append('  url = {'+url+'},\n')
    bibentry.append('  file = {'+bibtexkey+'.pdf:indexed\\\\'+bibtexkey+'.pdf:PDF},\n')
    bibentry.append('  owner = {'+owner+'},\n')
    bibentry.append('  timestamp = {'+timestamp+'}\n')
    bibentry.append('}\n')
    bibentry.append('\n')

    print authors

    return bibentry

def add_entry(bibpath, entry):
    '''
    add the entry by appending it
    '''
    #open for appending
    bibfile = open(bibpath,'a')

    #writing
    bibfile.writelines(entry)

