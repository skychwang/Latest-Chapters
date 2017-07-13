from tkinter import *
from tkinter.ttk import *
from lxml import html
import requests

class MainGUI(Frame):

    chapters = []
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

        self.listbox = Listbox(self, yscrollcommand=self.scrollbar.set)

        for newChapter in self.chapters:
            self.listbox.insert(END, newChapter)

        self.listbox.pack(side=TOP, fill=BOTH)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        
        self.pack(fill=BOTH, expand=True)
        
        self.closeButton = Button(self, text="Close", command=self.master.destroy)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        
        self.refreshButton = Button(self, text="Refresh Now", command=self.refresh)
        self.refreshButton.pack(side=RIGHT)

    def refresh(self):
        #
        updates = Scraper.scrape("http://mangafox.me/")#Add more sources
        self.chapters = []#empty previous updates for refresh
        for update in updates:
            self.chapters.append(update)
        #

        if self.firstInit != True:#two separate ifs because listbox won't exist on first init yet so runtime error would occur
            if self.listbox.winfo_exists() == 1:
                self.listbox.destroy()
                self.scrollbar.destroy()
                self.frame.destroy()
                self.closeButton.destroy()
                self.refreshButton.destroy()
                self.initUI()

class Scraper:
    def scrape(url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        updates = tree.xpath('//ul[@id="updates"]/li/div/h3/a/text()')#returns array of chapter names 
        #print(updates)#console error checking
        return updates
              
def main():
    root = Tk()
    root.geometry("300x207+300+300")
    app = MainGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()  
