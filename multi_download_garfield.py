# Downloads Garfield Comic

import requests, os, bs4, threading

print('\t\t---------Garfield Comic Download---------')

print('Enter the Year:')
year = input()

print("Enter the Month(1-12):")
month = input()

url = 'http://pt.jikos.cz/garfield/' + year + '/' + month
location = 'Garfield(' + month + '-' + year + ')'
os.makedirs(location, exist_ok=True)

def downloadGarfield(comicElem, startNum, endNum):
	# Download the images
	for i in range(startNum, endNum):
		comicUrl = comicElem[i].get('src')
		# Download the image.
		print('Downloading the image %s...' % (comicUrl))
		res = requests.get(comicUrl)
		res.raise_for_status()

		# Save the image to ./Garfield(month-year).
		imageFile = open(os.path.join(location, os.path.basename(comicUrl)), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

# Download the page.
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text,'lxml')

# Find the URL of the comic image.
comicElem = soup.select('table img')

downloadThreads = []
for i in range(0, len(comicElem), 2):
	downloadThread = threading.Thread(target = downloadGarfield, args=(comicElem, i, min(len(comicElem), i+2)))
	downloadThreads.append(downloadThread)
	downloadThread.start()

# Wait for all threads to end.
for downloadThread in downloadThreads:
	downloadThread.join()

print('Done')