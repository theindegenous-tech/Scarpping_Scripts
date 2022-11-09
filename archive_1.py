
import requests
from bs4 import BeautifulSoup


# URL from which pdfs to be downloaded
url = "https://archive.org/details/cdl"

# Requests URL and get response object
response = requests.get(url)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hyperlinks present on webpage
links = soup.find_all(class_ = "item-ttl C C2")

i = 0

# From all links check for pdf link and
# if present download file
for link in links:

	# print(link)
	ans = link.find('a')['href']
	print("ans",ans)

	comp_url =( "https://archive.org/"+ans)
	# data_type =link.get('data-category')
	response_2 = requests.get(comp_url)

		# Parse text obtained
	soup = BeautifulSoup(response_2.text, 'html.parser')

	# Find all hyperlinks present on webpage
	links_2 = soup.find_all(class_ = "format-summary download-pill")

	list = ["other str", 2, 56]
	for hit in links_2:
			i=i+1
			hit_detail = hit.text.strip()	
			if(hit_detail == "PDF              download"):
					try:
						# print("yes inside",hit['href'])
						
						comp_url =( "https://archive.org"+hit['href'])
						print("comp_url",comp_url)
						response = requests.get(comp_url)

						pdf = open("pdf"+str(i)+".pdf", 'wb')
						# print("response.content",response.content)
						pdf.write(response.content)

						pdf.close()
						print("File ", i, " downloaded")
					except:
						pass

	# print("All PDF files downloaded")




# print("All PDF files downloaded")
