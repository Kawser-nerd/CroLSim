from initialization import *


class FrontEnd:

    def interface(self):
        window1 = Tk()
        window1.title("CroLSim Execution Interface")
        #window1.geometry('640x480')
        link = Label(window1, text="Local Folder Link", font=("Helvetica", 12))
        link.grid(column=1, row=1, padx=5, pady=5)
        link_entry = Entry(window1, width=30)
        link_entry.grid(column=2, row=1, padx=5, pady=5)

        def browser_clicked():
            folder_Link = tkFileDialog.askdirectory()
            link_entry.delete(0, END)
            link_entry.insert(0, folder_Link)

        floder_Browser = Button(window1, text="Browse", command=browser_clicked, font=("Helvetica", 12))
        floder_Browser.grid(column=3, row=1, padx=5, pady=5)

        languagelable = Label(window1, text="Programming Language", font=("Helvetica", 12))
        languagelable.grid(column=1, row=3,padx=5, pady=5)
        language = StringVar(window1)
        choices = {'Java', 'Python', 'C#'}
        language.set('Choose One')
        languageMenu = OptionMenu(window1, language, *choices)
        languageMenu.grid(column=2, row=3, padx=5, pady=5)

        def apiextraction_clicked():
            selectedlanguage = language.get()
            folder_Link = link_entry.get()
            CroLSim().extractAPI(folder_Link, selectedlanguage)

        apiExtraction = Button(window1, text="API Extraction", command=apiextraction_clicked, font=("Helvetica", 12))
        apiExtraction.grid(column=2, row=5, padx=5, pady=5)
        window1.mainloop()


class CroLSim:
    global currentFolder

    def extractAPI(self, folderLink, selectedLanguage):
        self.master = Tk()

        if not folderLink:
            w = Message(self.master, text="Please Enter valid local directory")
            w.pack()
        else:
            if selectedLanguage == 'C#':
                self.master.destroy()
                self.Csharp(folderLink)
            elif selectedLanguage == 'Java':
                self.master.destroy()
                self.Java(folderLink)
            elif selectedLanguage == 'Python':
                self.master.destroy()
                self.Python(folderLink)
            else:
                w = Message(self.master, text="Please Enter valid Language")
                w.pack()

    def Csharp(self, folderLink):
        dataFolder = os.path.join(currentFolder, 'data/Csharp')

        if not os.path.exists(dataFolder):
            print 'Folder Creation'
            os.mkdir(dataFolder)

        listofprojects = os.listdir(folderLink)
        '''
        for projectSelected in listofprojects:
            fileName = dataFolder + '/' + projectSelected + '.txt'
            with open(fileName, 'w+') as fileAPI:
        '''



    def Java(self, folderLink):
        wkDir = os.getcwd()
        dataFolder = os.path.join(wkDir, 'data/Java')

        if not os.path.exists(dataFolder):
            print 'Folder Creation'
            os.mkdir(dataFolder)

        listofprojects = os.listdir(folderLink)


    def Python(self, folderLink):
        print 'Python'


if  __name__ == '__main__':
    starter = FrontEnd()
    starter.interface()


    '''
    1. Load XML file of API documentation
    2. Create files/List of Projects
    3. Search API names and Replace
    4. Doc Replacement with API names 
    '''