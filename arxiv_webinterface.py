#Program to read data from an arxiv URL to easily import into jabref. Later this program will write directly into a given .bib file.


import urllib
import os



def get_page(url):
    '''
    downloads page, returns as string
    '''
    
    #check for url typos
    if url.count('arxiv')==0:
        return 'badurl'

    #open and read page
    arxiv_page = urllib.urlopen(str(url))
    arxiv_text = arxiv_page.read()
    arxiv_page.close()
    
    #check if its an arxiv page
    if arxiv_text.count('Bad paper identifier') !=0:
        return 'badurl'


    #return the text
    return arxiv_text

def get_title(text, length=200):
    '''
    finds the title
    '''

    # find keyword title, take string from that index +6 
    # to get rid of 'title>' 
    startindex = text.find('title')+6
    title_plus = text[startindex+6: startindex+length]

    #hack of the string at </title>
    endindex = title_plus.find('</title>')
    title_plus2 = title_plus[:endindex]

    # hack of additional starting crap
    startind = title_plus.find(']')+1
    title_plus3 = title_plus2[startind:]

    title = title_plus3.lstrip()

    #remove nextlines:
    while title.count('\n ') != 0:
        title_list = title.partition('\n')
        title = title_list[0]+title_list[2]

    return title


def get_authors(text):
    '''
    gets all authors, puts names in the right order
    '''
    
    authorno = text.count('citation_author')
    authorlist = ''
    startindex=0

    for i in range(authorno):
        #find 'citation_author', extract author, move 18 to the right, repeat
        startindex = text.find('"citation_author"',startindex)+18
        author = get_author(text, startindex)
        authorlist = authorlist + author + ' and '
        startindex += 18
        if i == 0:
            firstauthor = author
    
    return authorlist[:-5], firstauthor

def get_author(text, startindex, initials=True):
    ''' 
    find the author from some text.
    relies on the fact that author is sandwiched between "s
    '''
    textpiece = text[startindex:startindex+100]
    #get everything to the right of the first "
    partright = textpiece.partition('"')[2]
    #of whats left, take everything left of the next "
    author_long = partright.partition('"')[0]

    author, last_names = author_long.partition(',')[0]+',', author_long.partition(',')[2]
    
    if initials==True:
        #get initials from complete names
        authorsplit = last_names.split()
        for i in range(len(authorsplit)):
            authoradd = ' ' + authorsplit[i].lstrip()[0]+'.'
            author = author+authoradd
        
        return author

    return author_long


def get_journal(text):
    '''
    finds the arxiv subjournal
    '''
    index = text.find('"tablecell arxivid"')
    textpiece = text[index:index+100]
    journalno = textpiece.partition('/abs/')[2]
    journalno = journalno.partition('"')[0]
    journal = 'arXiv:'+journalno

    assert journal != '', "journal not found"

    return journal


def get_year(text):
    '''
    finds the year
    '''
    index = text.find('"citation_date"')
    textpiece = text[index+20:index+100]
    year = textpiece.partition('"')[2][0:4]

    return year

def get_all(url) :


    text = get_page(url)
    if text == 'badurl':
        return 'badurl'


    title = get_title(text)
    authorlist, firstauthor = get_authors(text)
    year = get_year(text)
    bibtexkey = firstauthor.split()[0][:-1]+year
    journal = get_journal(text)

    return title, authorlist, year, journal, bibtexkey

# NOW Coded in the INTERFACE
#def dl_pdf(url, path='Q://PaperArchive/indexed/', bibtexkey):
#    '''
#    gets the file
#    '''
#    filename = bibtexkey+'.pdf'
#    if os.path.isfile(path+filename) == True:
#        return 'file exists'
#    else :
#        pdfurl = 
#    # if it doesnt exist, create URL
    #DL pdf using urllib.urlretrieve
#def __main__():
#
#    url = raw_input('give arxiv url: ')
#    get_all(url)
#
#
