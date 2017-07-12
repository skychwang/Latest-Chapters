from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style


class MainGUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
      
        self.parent.title("Latest Chapters")
        self.style = Style()
        #self.style.theme_use("default")
        
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        
        self.pack(fill=BOTH, expand=True)
        
        closeButton = Button(self, text="Close", command=self.master.destroy)
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        refreshButton = Button(self, text="Refresh Now", command=self.refresh)
        refreshButton.pack(side=RIGHT)

    def refresh(self):
        print("Refresh")
        #refresh func here
              

def main():
  
    root = Tk()
    root.geometry("300x200+300+300")
    app = MainGUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
