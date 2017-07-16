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
    currentSourceSelection = 0
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
        #column 1 is invis
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
        self.sourceSelection['values'] = ('Mangafox', 'Mangalife')
        self.sourceSelection.current(self.currentSourceSelection)
        self.sourceSelection.bind("<<ComboboxSelected>>", self.changeSource)
        self.sourceSelection.pack(side=RIGHT, padx=5, pady=5)

    def refresh(self):
        webscraper = Scraper("http://mangafox.me/")
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
        self.value_of_sourceSelection = self.sourceSelection.get()
        print(self.value_of_sourceSelection)

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
        
    def getSeries(self, tree):
        if self.url == 'http://mangafox.me/':
            self.series = tree.xpath('//ul[@id="updates"]/li/div/h3/a/text()')

    def getTimes(self, tree):
        if self.url == 'http://mangafox.me/':
            self.times = tree.xpath('//ul[@id="updates"]/li/div/h3/em/text()')
        
    def getLinks(self, tree):
        if self.url == 'http://mangafox.me/':
            for count in range(0, len(self.series)):
                self.links.append(self.series[count].getparent().get('href'))
            
    def getNewChapters(self, tree):
        if self.url == 'http://mangafox.me/':
            self.newChapters = tree.xpath('//ul[@id="updates"]/li/div/dl/dt/span/a/text()')
                
def main():
    root = Tk()
    root.geometry("450x255+300+300")
    app = LatestChapters(root)
    root.mainloop()

if __name__ == '__main__':
    main()
