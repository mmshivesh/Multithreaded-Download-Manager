import urllib.request
import threading
import argparse

parser = argparse.ArgumentParser(description="Multithreaded file downloader. Pass it multiple files to download them in parallel.")
parser.add_argument("url_list", metavar='u', nargs='+', help="List of urls to be downloaded.")

args = parser.parse_args()
print_lock = threading.Lock()

def downloader(url):
	''' Downloads content from url ''' 
	file_name = url.split('/')[-1]
	u = urllib.request.urlopen(url)
	file_size = int(u.getheader("Content-Length"))
	# Check for html page or downloadable file
	print(u.getheader("Content-Length"), u.getheader('Content-Type'))
	exit()
	f = open(file_name, 'wb')
	with print_lock:	
		print("Downloading: %s Bytes: %s" % (file_name, file_size))
	print(file_size)
	file_size_dl = 0
	block_sz = 2**10
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break
		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		with print_lock:	    
			print(status)
	f.close()

threads = []

for url in args.url_list:
	t = threading.Thread(target=downloader, args=(url,)) 
	threads.append(t)	
	t.start()

for t in threads:
	t.join()

 
# https://speed.hetzner.de/100MB.bin http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf
