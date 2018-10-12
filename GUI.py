import tkinter
from tkinter import ttk
import urllib.request
import threading

AppName = 'Multithreaded Downloader'
window = tkinter.Tk()
window.title(AppName)
window.geometry('1000x600')

#List to store the passed urls
storeUrlsToDownload = list()

print_lock = threading.Lock()
file_size_dl = int()
file_name = tkinter.StringVar(window, value='')
def downloader(url):
	''' Downloads content from url ''' 
	file_name.set(url.split('/')[-1])
	u = urllib.request.urlopen(url)
	file_size = int(u.getheader("Content-Length"))
	# Check for html page or downloadable file
	# print(u.getheader("Content-Length"), u.getheader('Content-Type'))
	progress['value'] = 0
	progress["maximum"] = file_size
	f = open(file_name.get(), 'wb')
	# with print_lock:	
	# 	print(file_size)
	file_size_dl = 0
	block_sz = 2**10
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break
		file_size_dl += len(buffer)
		f.write(buffer)
		progress['value'] = file_size_dl
		# status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		# status = status + chr(8)*(len(status)+1)
		with print_lock:	    
			print(file_size_dl)
	f.close()

def DownloaderThreadCreator():
	threads = []

	for url in storeUrlsToDownload:
		t = threading.Thread(target=downloader, args=(url,)) 
		threads.append(t)	
		t.start()

	for t in threads:
		t.join()

def url_is_alive(url):
	try:
		request = urllib.request.Request(url)
		request.get_method = lambda: 'HEAD'
	except ValueError:
		return False
	except urllib.request.URLError:
		return False
	try:
		try:
			urllib.request.urlopen(request)
			# try:
			# 	file_size = int(u.getheader("Content-Length"))/(1024)
			# except AttributeError:
			# 	return False
			# addButton.config(state=tkinter.NORMAL)
			# addButton.config(text='Add, ' + str(file_size) + 'K')
		except urllib.request.URLError:
			return False
		return True
	except urllib.request.HTTPError:
		return False

def addButtonPressed():
	#Check for the url validity before adding or trace it before 
	print(EnteredURL.get() + " -> the url will be added after validity checking")
	if(checkForExistenceOfUrl()):
		print("VALID!")
		storeUrlsToDownload.append(EnteredURL.get())
	print(storeUrlsToDownload)
	DownloaderThreadCreator()

def checkForExistenceOfUrl(*args):
	if(EnteredURL.get()):
		if(not url_is_alive(EnteredURL.get())):
			addButton.config(state=tkinter.DISABLED)
			addButton.config(text='Check URL')
			return False
		else:
			addButton.config(state=tkinter.NORMAL)
			addButton.config(text='Add')
			return True
	else:
		addButton.config(state=tkinter.DISABLED)
		return False
		
def pressedKey(event):
	print("Return was pressed, same as add button pressed")
	addButtonPressed()

def selectAll(event):
	urlTextBox.selection_range(0,len(EnteredURL.get()))

#TITLE LABEL
label = tkinter.Label(window, text=AppName)
# label.pack()
label.grid(row=0, column=0, columnspan=5)

# URL: Label on the left of the text box
urlLabel = tkinter.Label(window, text='URL:')
# urlLabel.pack(after=label, side=tkinter.LEFT, anchor='nw')
urlLabel.grid(row=1, column=0, rowspan=1, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
#URL TextBox and the Add button

EnteredURL = tkinter.StringVar(window, value='')
EnteredURL.trace('w', checkForExistenceOfUrl)

urlTextBox = tkinter.Entry(window, exportselection=0, textvariable=EnteredURL)
addButton = tkinter.Button(window,text='Add', command=addButtonPressed, state=tkinter.DISABLED)
# urlTextBox.pack(after=urlLabel,side=tkinter.LEFT,expand=True, anchor='nw', fill=tkinter.X)
urlTextBox.grid(row=1, column=1, rowspan=1, columnspan=2,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
urlTextBox.bind('<Return>', pressedKey)
urlTextBox.bind('<Command-a>', selectAll)
# addButton.pack(after=urlTextBox,side=tkinter.RIGHT, expand=False, anchor='nw')
addButton.grid(row=1, column=3, rowspan=1, columnspan=1, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)

window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_columnconfigure(4, weight=0)

downloadUrlLabel = tkinter.Label(window, textvariable=file_name)
downloadUrlLabel.grid(row=2, column=0,columnspan=2, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)

progress = tkinter.ttk.Progressbar(window,orient="horizontal", length=200, mode="determinate")
progress.grid(row=2, column=2, columnspan=2, sticky=tkinter.W)
window.mainloop()
