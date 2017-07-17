from tkinter import *
from tkinter.ttk import *
from lxml import html
import requests
import webbrowser

class LatestChapters(Frame):

    series = []
    times = []
    links = []
    newChapters = []
    currentSourceSelection = 0#change this to change starting source; index corresponds to item in sourcesNames
    sourcesNames = ('Mangafox', 'Mangalife');
    sourcesURL = {"Mangafox":"http://mangafox.me/", "Mangalife":"http://mangalife.us/"}
    firstInit = True
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.refresh()
        self.initUI()
        self.firstInit = False
        
    def initUI(self):
        self.parent.title("Latest Chapters")
        self.style = Style()
        self.style.theme_use("default")
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.tree = Treeview(self, yscrollcommand=self.scrollbar.set)
        self.tree['columns'] = ('Link', 'newChapters', 'timeUpdated')
        self.tree.heading('#0', text='Series')
        self.tree.column("#0", minwidth=0, width=200)
        self.tree.heading('#1', text='Link')
        #column 1, links, is invis
        self.tree.heading('#2', text='newChapters')
        self.tree.column("#2", minwidth=0, width=100)
        self.tree.heading('#3', text='timeUpdated')
        self.tree.column("#3", minwidth=0, width=100)
        num = 0
        for oneSeries in range(0, len(self.series)):
            newChapterIDs = ''
            while num < len(self.newChapters) and self.series[oneSeries] in self.newChapters[num]:
                newChapterIDs += self.newChapters[num].replace(self.series[oneSeries], '')
                num += 1
            newChapterIDs = newChapterIDs.lstrip()
            self.tree.insert('', 'end', text=self.series[oneSeries], values=(self.links[oneSeries], newChapterIDs, self.times[oneSeries]))
        self.tree.bind('<Double-Button-1>' , self.openLink)
        self.tree["displaycolumns"]=('newChapters', 'timeUpdated')
        self.tree.pack(side=TOP, fill=BOTH)
        self.scrollbar.config(command=self.tree.yview)
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)
        self.closeButton = Button(self, text="Close", command=self.master.destroy)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.refreshButton = Button(self, text="Refresh Now", command=self.refresh)
        self.refreshButton.pack(side=RIGHT, padx=5, pady=5)
        self.sourceSelection_value = StringVar()
        self.sourceSelection = Combobox(self, textvariable=self.sourceSelection_value)
        self.sourceSelection['values'] = self.sourcesNames
        self.sourceSelection.current(self.currentSourceSelection)
        self.sourceSelection.bind("<<ComboboxSelected>>", self.changeSource)
        self.sourceSelection.pack(side=RIGHT, padx=5, pady=5)

    def refresh(self):
        if self.firstInit != True:
            webscraper = Scraper(self.sourcesURL[self.sourceSelection.get()])
        else:
            webscraper = Scraper(self.sourcesURL[self.sourcesNames[self.currentSourceSelection]])
        self.series = webscraper.series
        self.times = webscraper.times
        self.links = webscraper.links
        self.newChapters = webscraper.newChapters
        if self.firstInit != True:
            if self.tree.winfo_exists() == 1:
                self.tree.destroy()
                self.scrollbar.destroy()
                self.frame.destroy()
                self.closeButton.destroy()
                self.refreshButton.destroy()
                self.currentSourceSelection = self.sourceSelection.current()
                self.sourceSelection.destroy()
                self.initUI()

    def openLink(self, event):
        webbrowser.open(self.tree.item(self.tree.focus()).get('values')[0])

    def changeSource(self, event):
        #self.sourceSelection.get()
        self.refresh()

class Scraper:

    url = ''
    series = []
    times = []
    links = []
    newChapters = []
    
    def __init__(self, url):
        self.url = url
        page = requests.get(url)
        tree = html.fromstring(page.content)
        self.getSeries(tree)
        self.getTimes(tree)
        self.getLinks(tree)
        self.getNewChapters(tree)
        
    def getSeries(self, tree):#Format is in "<Series Name>"
        if self.url == 'http://mangafox.me/':
            self.series = tree.xpath('//ul[@id="updates"]/li/div/h3/a/text()')
        elif self.url == 'http://mangalife.us/':
            self.series = tree.xpath('//div/div/div/div/a/div/div/p/text()')
            for count in range(0, len(self.series)):
                self.series[count] = self.series[count].rstrip('1234567890').lstrip()

    def getTimes(self, tree):#Format follows website's chosen format
        if self.url == 'http://mangafox.me/':
            self.times = tree.xpath('//ul[@id="updates"]/li/div/h3/em/text()')
        elif self.url == 'http://mangalife.us/':
            self.times = tree.xpath('//div/div/div/div/a/div/div/time/text()')
        
    def getLinks(self, tree):#Format is the http:// link
        self.links = []
        if self.url == 'http://mangafox.me/':
            for count in range(0, len(self.series)):
                self.links.append(self.series[count].getparent().get('href'))
        elif self.url == 'http://mangalife.us/':
            for count in range(0, len(self.series)):
                if tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().get('href') is not None:
                    self.links.append('http://mangalife.us' + tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().get('href'))
                elif tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().getparent().get('href') is not None:
                    self.links.append('http://mangalife.us' + tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().getparent().get('href'))
            
    def getNewChapters(self, tree):#Format is "<Series Name> <Chapter>"
        if self.url == 'http://mangafox.me/':
            self.newChapters = tree.xpath('//ul[@id="updates"]/li/div/dl/dt/span/a/text()')
        elif self.url == 'http://mangalife.us/':
            self.newChapters = tree.xpath('//div/div/div/div/a/div/div/p/text()')
            
def main():
    root = Tk()
    root.geometry("450x255+300+300")
    app = LatestChapters(root)
    root.mainloop()

if __name__ == '__main__':
    main()
