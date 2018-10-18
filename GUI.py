
# GUI for a Multithreaded Download Manager. 

# Import Statements
import tkinter				# Python GUI Library - For building GUI
from tkinter import ttk		# Overrides tk themed widgets - Progressbar is in this library
from tkinter import filedialog
import threading			# Python Threading Library - Start multiple downloads in threaded fashion
import urllib.request		# Python url parse library - Used to Download urls
import os

# Global Constants
fileGUIRowNumber = 2		# 0 and 1 are GUI elements. The first download can be inserted at 2
threadJobList = []

# =================================
# Initialize GUI
# =================================
appName = 'Multithreaded Downloader'
window = tkinter.Tk()
window.title(appName)
window.geometry('1000x600')
# Setting up a five column grid, Not fixed, just some number.
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_columnconfigure(4, weight=0)

locationFile = open('location.txt', 'r')
downloadLocation = locationFile.read()
print(downloadLocation)
locationFile.close()
# exit()
def changeLocation():
	global downloadLocation
	returnedDownloadLocation = filedialog.askdirectory(initialdir=downloadLocation)
	if returnedDownloadLocation:
		downloadLocation = returnedDownloadLocation
		locationFile = open('location.txt', 'w+')
		locationFile.truncate()
		locationFile.write(returnedDownloadLocation)
	downloadLocationButton.config(text='Download Location : '+ downloadLocation.split('/')[-1])

def terminateThread(thread, f, fileNameLabel, progressBar, cancelButton):
	f.close()
	fileNameLabel.grid_forget()
	progressBar.grid_forget()
	cancelButton.grid_forget()
	print(threadJobList)
	thread.exit(1)

def downloadOnAThread(url):
	# It is ensured that the 'url' obtained here is downloadable
	# This function creates a thread, pushes the coressponding filename and the progress onto the GUI and manages it
	# When the download finishes, the corresponding row is removed (opt. and all others are moved up?)
	u = urllib.request.urlopen(url)										# Open the File
	fileNameStr = url.split('/')[-1]
	downloadPath = os.path.join(os.path.expanduser(downloadLocation),url.split('/')[-1])
	fileName = tkinter.StringVar(window,value=fileNameStr)		# Get the file name to write to
	totalFileSize = int(u.getheader("Content-Length"))					# Get the total file size
	print(downloadPath)
	# print(totalFileSize, url)
	
	# Set up the GUI
	
	downloadingFileName = tkinter.Label(window, textvariable=fileName)
	downloadingFileName.grid(row=fileGUIRowNumber, column=0, columnspan=2, sticky=tkinter.E+tkinter.W)
	
	threadProgressBar = tkinter.ttk.Progressbar(window, orient=tkinter.HORIZONTAL, mode='determinate')
	threadProgressBar.grid(row=fileGUIRowNumber, column=2, columnspan=2, sticky=tkinter.E+tkinter.W)
	threadProgressBar['value']=0
	threadProgressBar['maximum']=totalFileSize

	cancelButton = tkinter.Button(window, text="Cancel", command= lambda : terminateThread(threading.current_thread(), f, downloadingFileName, threadProgressBar, cancelButton))
	cancelButton.grid(row=fileGUIRowNumber, column=4, columnspan=1, sticky=tkinter.E+tkinter.W)
	# Begin downloading the Url

	f = open(downloadPath, 'wb')
	downloadedFileSize = 0
	blockSize = 2**10 # 1024
	while True:
		buffer = u.read(blockSize)
		if not buffer:
			break
		downloadedFileSize += len(buffer)
		f.write(buffer)
		threadProgressBar['value'] = downloadedFileSize
	f.close()
	downloadingFileName.grid_forget()
	threadProgressBar.grid_forget()
	cancelButton.grid_forget()
	# print("url finished downloading")

def createThread():
	global threadJobList
	global fileGUIRowNumber
	## !!! Caution !!! Using because the url is already verified
	url = textBoxContents.get()
	t = threading.Thread(target=downloadOnAThread, args=(url,))
	fileGUIRowNumber+=1
	threadJobList.append(t)
	t.start()
	t.join(1)
	pass

def validateUrl(url):
	# This function ensures if the url passed to the function is a valid, downloadable url.
	# For example, webpages like https://www.google.com is rejected as it a webpage and not a file.
	# This function is called at every change of the textbox. So this validation is in realtime. 
	# Moreover, it handles the enabling and disabling of "Add Url" button properly
	# However this function works pretty slow.
	try:
		request = urllib.request.Request(url)
		request.get_method = lambda: 'HEAD'
	except ValueError:
		return False
	except urllib.request.URLError:
		return False
	try:
		try:
			u = urllib.request.urlopen(request)
			try:
				filelengthKB = int(u.getheader("Content-Length"))/(1024)
				filelengthMB = filelengthKB/1024
				filelengthGB = filelengthMB/1024
				fileName = url.split('/')[-1]
			except:
				return False
			# URL is valid from here
			addUrlButton.config(state=tkinter.NORMAL)		# Enable the button
			if(filelengthMB < 1):
				addUrlButton.config(text='Add ' + fileName + ', ' + str(round(filelengthKB,2)) + 'K')
			elif filelengthGB > 0.9:
				addUrlButton.config(text='Add ' + fileName + ', ' + str(round(filelengthGB,2)) + 'G')
			else:
				addUrlButton.config(text='Add ' + fileName + ', ' + str(round(filelengthMB,2)) + 'M')
			# URL is valid till here
			return True
		except urllib.request.URLError:
			return False
	except urllib.request.HTTPError:
		return False

def changeButtonState(*args):		# Take some dummy arguments
	urlValidState = validateUrl(textBoxContents.get())	# Either True or False
	if not urlValidState:
		addUrlButton.config(state=tkinter.DISABLED)
		addUrlButton.config(text='Check URL')
# Some Keyboard Handler functions for User-friendliness

def pressedKey(event):
	# print("Return was pressed, same as add button pressed")
	urlValidState = validateUrl(textBoxContents.get())
	if urlValidState:
		createThread()

def selectAll(event):
	urlEntryBox.selection_range(0,len(textBoxContents.get()))


# =================================
# Graphical User Interface building
# =================================
'''
	_____________________________________________
	|				< App Name >				|
	|	url: <Entry Field>		<Add Button>	|
	|	<File Name 1>			<Progress Bar>	|
	|	<File Name 1>			<Progress Bar>	|
	|											|
	..											..

'''
# Name of the app at the top
appNameLabel = tkinter.Label(window, text=appName)
appNameLabel.grid(row=0, column=0, columnspan=3)	# Span Across 3 columns

downloadLocationButton = tkinter.Button(window, text='Download Location : ' + downloadLocation.split('/')[-1], command=changeLocation)
downloadLocationButton.grid(row=0, column=3, columnspan=1, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

urlLabel = tkinter.Label(window, text='URL : ')
urlLabel.grid(row=1, column=0, columnspan=1)		# Next row, one column span

textBoxContents = tkinter.StringVar(window, value='')		# This variable will have all the contents of the Entry/Textbox
textBoxContents.trace("w", changeButtonState)						# At every change of the textbox contents, Check to see if you need to enable the button
urlEntryBox = tkinter.Entry(window, textvariable=textBoxContents)
urlEntryBox.bind('<Command-a>', selectAll)
urlEntryBox.bind('<Return>', pressedKey)
urlEntryBox.grid(row=1,column=1, columnspan=2, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)	# Make the text box fill the columns

addUrlButton = tkinter.Button(window, text='Add Url', state=tkinter.DISABLED, command=createThread)	# Initially the button is disabled
addUrlButton.grid(row=1, column=3, columnspan=2, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W) # We want a chonky button

ttk.Separator(window,orient=tkinter.HORIZONTAL).grid(row=2, columnspan=5, sticky=tkinter.E+tkinter.W)	# Some horizontal Line

# The downloads will be added by the thread function

window.mainloop()