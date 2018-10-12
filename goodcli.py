import tkinter

AppName = 'Multithreaded Downloader'
window = tkinter.Tk()
window.title(AppName)
window.geometry('450x450')

#List to store the passed urls
storeUrlsToDownload = list()

def addButtonPressed():
	#Check for the url validity before adding or trace it before 
	print(EnteredURL.get() + " -> the url will be added after validity checking")
	storeUrlsToDownload.append(EnteredURL.get())

def checkForExistenceOfUrl(*args):
	if(EnteredURL.get()):
		addButton.config(state=tkinter.NORMAL)
	else:
		addButton.config(state=tkinter.DISABLED)
		
def pressedKey(event):
	print("Return was pressed, same as add button pressed")
	addButtonPressed()

#TITLE LABEL
label = tkinter.Label(window, text=AppName)
# label.pack()
label.grid(row=0, column=0, columnspan=5)

# URL: Label on the left of the text box
urlLabel = tkinter.Label(window, text='URL:')
# urlLabel.pack(after=label, side=tkinter.LEFT, anchor='nw')
urlLabel.grid(row=1, column=0, rowspan=2, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
#URL TextBox and the Add button

EnteredURL = tkinter.StringVar(window, value='')
EnteredURL.trace('w', checkForExistenceOfUrl)

urlTextBox = tkinter.Entry(window, exportselection=0, textvariable=EnteredURL)
addButton = tkinter.Button(window,text='Add', command=addButtonPressed, state=tkinter.DISABLED)
# urlTextBox.pack(after=urlLabel,side=tkinter.LEFT,expand=True, anchor='nw', fill=tkinter.X)
urlTextBox.grid(row=1, column=1, rowspan=2, columnspan=2,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
urlTextBox.bind('<Return>', pressedKey)
# addButton.pack(after=urlTextBox,side=tkinter.RIGHT, expand=False, anchor='nw')
addButton.grid(row=1, column=3, rowspan=2, columnspan=2)
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=0)
window.grid_columnconfigure(4, weight=0)
window.mainloop()
