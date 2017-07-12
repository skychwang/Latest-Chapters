from tkinter import *
from tkinter.ttk import *


class MainGUI(Frame):

    chapters = []
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent

        #refresh function contents here
        self.chapters.append("hi")#temp
        #
        
        self.initUI()

        
    def initUI(self):
        self.parent.title("Latest Chapters")
        self.style = Style()
        #self.style.theme_use("default")

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
        self.chapters.append("hi")#temp
        
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.frame.destroy()
        self.closeButton.destroy()
        self.refreshButton.destroy()
        self.initUI()
              
def main():
    root = Tk()
    root.geometry("300x207+300+300")
    app = MainGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()  
