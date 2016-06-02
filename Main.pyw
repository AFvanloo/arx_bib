from arxiv_webinterface import *
import bibtex_handling as bibhan
from Tkinter import *
import urllib
import os
import time


class Interface(Frame):

    def __init__(self, parent):
        ''' 
        Initializing the window
        '''

        Frame.__init__(self, parent)
        self.parent = parent
        self.grid()

        #properties of the class are URL, title, authors, year, journal, bibpath
        self.url = ''
        self.title = ''
        self.authors = ''
        self.year = ''
        self.journal = ''
        self.bibpath = ''
        #self.pdfpath = 'Q://PaperArchive/indexed/'
        self.pdfpath = 'Q://PaperArchive/Indexed/'
        self.bibtexkey = ''
        self.owner = ''
        self.timestamp = ''
        
        
        #ENTER INSTALLATION PATH HERE
        self.cfgpath = os.getcwd()+'/arx_bib_config.txt'
        
        self.initUI()




    def initUI(self):

        '''
        creating widgets etc
        '''

        
        #for inputting the URL
        self.urllabel = Label(self, text=' input URL here: ').grid(row=0,column=1, sticky=E)
        self.urlentry = Entry(self, width=70)
        self.urlentry.grid(row=0,column = 2, sticky=W)
        
        # for inputting the bibfile
        self.bibblabel = Label(self, text=' input bibfile \n path here: ').grid(row=1,column=1, sticky=E)
        self.bibentry = Entry(self, width=70)
        self.bibentry.grid(row=1,column = 2, sticky=W)
        self.bibentry.insert(0,self.bibpath)
        
        #create the buttons
        self.quitbutton = Button(self, text='Quit', fg='red',
                command=self.close_window,width=15).grid(row=9,column=3)
        self.databutton = Button(self, text='get Data', fg='blue', command=self.getshow_data,width=15).grid(row=0,column=3)
        self.pdfbutton = Button(self, text='save pdf to path', fg='black', command=self.get_pdf,width=15).grid(row=8,column=3)
        self.bibbutton = Button(self, text='make bibtex entry', fg='black', command=self.make_bib_entry,width=15).grid(row=7,column=3)
        #self.bibsavebutton = Button(self, text='save bibfile path \n to config file', fg='black', command=self.save_bib_path,width=15).grid(row=1,column=3)
        
        #create labels
        self.titlelabel = Label(self, text='title: ').grid(row=3,column=1, sticky=E)
        self.authorslabel = Label(self, text='authors: ').grid(row=4,column=1, sticky=E)
        self.journallabel = Label(self, text='journal: ').grid(row=5,column=1, sticky=E)
        self.yearlabel = Label(self, text='year: ').grid(row=6,column=1, sticky=E)
        self.bibtexkeylabel = Label(self, text='bibtexkey: ').grid(row=7,column=1, sticky=E)
        self.textlabel = Label(self, text = 'Bibtex data taken from the arxiv URL').grid(row=2,column=2)
        self.infolabel = Label(self, text = 'pdfpath, bibtexpath  and owner are changeable in the config file', fg='red').grid(row=9, column=2, sticky=W)
        self.pdflabel = Label(self, text='pdf path: ').grid(row=8,column=1, sticky=E)

        
        #create empty entries
        self.titleentry = Entry(self, width=70)
        self.titleentry.grid(row=3, column=2, sticky=W)
        
        self.authorsentry = Entry(self, width=70)
        self.authorsentry.grid(row=4, column=2, sticky=W)
        
        self.journalentry = Entry(self, width=70)
        self.journalentry.grid(row=5, column=2, sticky=W)
        
        self.yearentry = Entry(self, width=70)
        self.yearentry.grid(row=6, column=2, sticky=W)
         
        self.bibtexkeyentry = Entry(self, width=70)
        self.bibtexkeyentry.grid(row=7, column=2, sticky=W)

        self.pdfpathlabel = Label(self, text = self.pdfpath+'...')
        self.pdfpathlabel.grid(row=8, column=2, sticky=W)


        #open the config file
        cfgfile = open(self.cfgpath)
        cfg = eval(cfgfile.read())

        self.bibpath = cfg.get('bibpath')
        self.pdfpath = cfg.get('pdfpath')
        self.owner = cfg.get('owner')
        
        cfgfile.close()
        
        
        #show config
        self.bibentry.insert(0, self.bibpath)

        # set window title
        self.parent.title('arXiv to bibtex, run by: ' + self.owner)
        
    def getshow_data(self):
        '''
        just calls the get and show functions
        '''
        self.get_data()
        self.show_data()

    def get_data(self):
        '''
		gets data from url, uses module arxiv_bibtex
		'''
        self.url = self.urlentry.get()
        self.timestamp = self.get_timestamp()
        # Check URL
        if self.url == '':
            self.text = Text(self, 'No URL Entered').grid(row=10,column=2)
            self.show_messg('no url entered')
        elif get_all(self.url) == 'badurl':
            self.show_messg('bad url')
            return '', '', '', '', '' 

        else : 
            self.title, self.authors, self.year, self.journal, self.bibtexkey = get_all(self.url)
            
            #check bibtex path
            self.check_bib_path()
            
            #Check pdf file
            self.check_pdf_path()

        return

        
    def get_timestamp(self):
        '''
        get time info
        '''

        #Get time info, add zeroes with zfill if necessary
        time_info = time.localtime()
        time_month = str(time_info.tm_mon).zfill(2)
        time_day = str(time_info.tm_mday).zfill(2)

        timestamp = str(time_info.tm_year)+'.'+time_month+'.'+time_day
        self.timestamp = timestamp
       
        return timestamp 
        
    def get_entries(self):
        '''
        gets all entries before making the bib entry
        '''
        self.title = self.titleentry.get()
        self.authors = self.authorsentry.get()
        self.journal = self.journalentry.get()
        self.year = self.yearentry.get()
        self.bibtexkey = self.bibtexkeyentry.get()
         

    def show_data(self):
        '''
        takes the data from get_data, shows it in the entry boxes
        '''
        if self.title == '':
            return
        else:
            #empty fields
            self.empty_all()

            self.titleentry.insert(0,self.title)
            self.authorsentry.insert(0,self.authors)
            self.journalentry.insert(0,self.journal)
            self.yearentry.insert(0,self.year)
            self.bibtexkeyentry.insert(0,self.bibtexkey)
            self.pdfpathlabel.config(text=self.pdfpath+self.bibtexkey+'.pdf')

    

    def show_messg(self, mstext):
        msswin = Toplevel()
        typotext = Button(msswin, text=mstext,
                   bg="blue", fg="yellow",
                   activebackground="red", activeforeground="white",
                   padx=msswin.winfo_screenwidth()/4,
                   pady=msswin.winfo_screenheight()/4,
                   command=msswin.destroy)
        typotext.grid(row=0,column=0)
    

    def show_messg2(self, mstext):
        '''
        second popup message
        '''
        msswin2 = Toplevel()
        typotext = Button(msswin2, text=mstext,
                   bg="blue", fg="yellow",
                   activebackground="red", activeforeground="white",
                   padx=msswin2.winfo_screenwidth()/4,
                   pady=msswin2.winfo_screenheight()/4,
                   command=msswin2.destroy)
        typotext.grid(row=0,column=0)

    def show_choice_window(self,ms1,c1,c2, key):
        '''
        shows explanation and 2 choices
        '''
        choicewin = Toplevel(self)
        explanation = Label(choicewin, text=ms1,fg='blue').grid(row=2,column=1,columnspan=3)
        choice1 = Button(choicewin,text=c1,fg='black',command=self.choose_yes)
        choice2 = Button(choicewin,text=c2,fg='black',command=choicewin.destroy)
        quitbutton2 = Button(choicewin,text='close window',fg='black',command=choicewin.destroy)
        
        choice1.grid(row=1,column=1)
        choice2.grid(row=1,column=2)
        quitbutton2.grid(row=1,column=3)

    
    def empty_all(self):
        self.titleentry.delete(0,200)
        self.authorsentry.delete(0,200)
        self.journalentry.delete(0,200)
        self.yearentry.delete(0,200)
        self.bibtexkeyentry.delete(0,200)
        
    def get_pdf(self):
        '''
        gets the file. The path it downloads to is hardcoded in the properties in __init__
        '''
        
        filename = self.bibtexkey+'.pdf'
        #check if filename is free
        if self.check_pdf_path():
            #get pdf
            filepath = self.pdfpath+filename
            pdfurl = 'http://arxiv.org/pdf/'+self.journal[5:]+'.pdf'
            urllib.urlretrieve(pdfurl, self.pdfpath+filename)


    def check_pdf_path(self):
        '''
        checks if pdf file already exists
        '''
        filename = self.bibtexkey+'.pdf'

        if os.path.isfile(self.pdfpath+filename) == True:
            self.show_messg2('pdf file already exists')
            return False
        else :
            return True

    def check_bib_path(self):
        '''
        checks if bib file already exists
        '''
        if os.path.isfile(self.bibpath) != True:
            self.show_messg('bibfile does not exist')
            return False
        else :
            return True
 
    def check_bib_key(self):
        '''
        checks:
        bibtexkey
        bibtexpath
        '''
    
        #check bibtexkey
        key = bibhan.check_key(self.bibpath, self.bibtexkey)

        if key ==  'False':
            self.show_messg('no  appropriate bibtexkey found \n check how many of the same name there are!')
            return 'nokey'
        elif key == self.bibtexkey:
            return 'key'
        else :
            message = 'a bibtex key '+self.bibtexkey+' exists. \n Check if its the same paper. \n If it isnt, we suggest :' + key
            
            #update key regardless whether its used or not
            self.bibtexkey = key
            self.show_data()

            self.show_choice_window(message, 'this is a different paper. \n I submit the suggested key', 'Cancel!', key)
            return key

    def save_bib_path(self):

        #read dict
        with open(self.cfgpath, 'r') as file:
            cfg = eval(file.read())

        #change dict
        self.bibpath = self.bibentry.get()
        cfg['bibpath'] = self.bibpath

        #write to file
        with open(self.cfgpath, 'w') as file:
            file.write(str(cfg))

    def choose_yes(self):
        '''
        sets choice to yes
        '''
        self.do_make_bib_entry()


    def make_bib_entry(self):
        '''
        Uses the functionality in module 'bibtex_handling'
        '''
        
        if self.check_bib_path == False:
            return
        
        output = self.check_bib_key()
        if output == 'nokey':
            return

        elif output == 'key':
            self.get_entries()
            try :
                bibhan.make_entry(self.title, self.url, self.authors, self.year, self.journal, self.bibtexkey, self.bibpath, self.owner, self.timestamp)
            except TypeError:
                self.show_messg('There is an Error.  \n \
                Probably a non-ascii sign in the title or authorlist. \n \
                Please rewrite in Latex and try again')
        else :
            return

       
    def do_make_bib_entry(self):
        '''
        button function to make entry without checks
        '''
        self.get_entries()
        try :
            bibhan.make_entry(self.title, self.url, self.authors, self.year, self.journal, self.bibtexkey, self.bibpath, self.owner, self.timestamp)
        except TypeError:
            self.show_messg('There is an Error.  \n Probably a non-ascii sign in the title,  authorlist, or bibtexkey \n Please rewrite in Latex and try again')

    def close_window(self):
        self.quit()
        self.master.destroy()

def main():
    root = Tk()
    root.title('arxiv to bibtex: work in progress')
    interface = Interface(root)
    root.mainloop()

if __name__ == '__main__':
   main()


   #TODO Known bugs: Sometimes a paper will not get added. When you use .pyw, it will also not give you an error. This is due to some sign in the title, probably an apostrophe.
   #TODO add module for unicode->latex
