# Import libraries
import requests
from bs4 import BeautifulSoup

# URL from which pdfs to be downloaded
url = "https://universitypress.whiterose.ac.uk/site/books/"

# Requests URL and get response object
response = requests.get(url)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hyperlinks present on webpage
links = soup.find_all('a')

i = 0
timer = 3

# From all links check for pdf link and
# if present download file
for link in links:
	if ('/site/books/10.22599/' in link.get('href', [])):
		i += 1

		print("link",link)
		timer -= 1
		
		
		print("Downloading file: ", i)
		print("href",link.get('href'))
		comp_url =( "https://universitypress.whiterose.ac.uk"+link.get('href'))
		data_type =link.get('data-category')
		if(data_type):
			cate = data_type.split(' ')[0]
			print("cate",cate)
		
		print("comp_url",comp_url)
		# print("data_type",cate)
		# Get response object for link
		response = requests.get(comp_url)

		# Write content in pdf file
		if(data_type):
			pdf = open("pdf"+str(i)+"."+cate, 'wb')
			# print("response.content",response.content)
			pdf.write(response.content)

			pdf.close()
			print("File ", i, " downloaded")

print("All PDF files downloaded")
