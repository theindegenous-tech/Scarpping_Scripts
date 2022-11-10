
from sqlite3 import Cursor
import psycopg2
import requests
from bs4 import BeautifulSoup


from boto3 import session
from botocore.client import Config

ACCESS_ID = 'DO00DZN9YDVM4H4QKLPE'
SECRET_KEY = 'TJZGQgbfYS7aES8D9H/h5+/hDutOyn8BGwfhRmSdc1c'

# # Initiate session
# session = session.Session()
# client = session.client('s3',
#                         region_name='nyc3',
#                         endpoint_url='https://nyc3.digitaloceanspaces.com',
#                         aws_access_key_id=ACCESS_ID,
#                         aws_secret_access_key=SECRET_KEY)
						
# client.upload_file('books/pdf5.pdf',  # Path to local file

#                    'booksdatabaseepub',  # Name of Space
#                    'pdf5.pdf')  # Name for remote file


def connectSQL():
		try:
			connection = psycopg2.connect(user="admin",
										password="admin",
										host="127.0.0.1",
										port="5432",
										database="library")
			cursor = connection.cursor()
			postgres_insert_query = "INSERT INTO the_indegenous_backend_book (id,title,description,year,url) VALUES  (4,'Test','desc',2022,'url')"
			cursor.execute(postgres_insert_query)

			connection.commit()
			count = cursor.rowcount
			print(count, "Record inserted successfully into mobile table")

		except (Exception, psycopg2.Error) as error:
			print("Failed to insert record into mobile table", error)
		
connectSQL()
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
	try:
	# print(link)
		ans = link.find('a')['href']
		print("ans",ans)

		comp_url =( "https://archive.org/"+ans)
		# data_type =link.get('data-category')
		response_2 = requests.get(comp_url,timeout=15) 

			# Parse text obtained
		soup = BeautifulSoup(response_2.text, 'html.parser')

		# Find all hyperlinks present on webpage
		links_2 = soup.find_all(class_ = "format-summary download-pill")

		for hit in links_2:
				i=i+1
				hit_detail = hit.text.strip()	
				if(hit_detail == "PDF              download"):
						try:
							# print("yes inside",hit['href'])
							
							comp_url =( "https://archive.org"+hit['href'])
							print("comp_url",comp_url)
							response = requests.get(comp_url)
							path = "books/pdf"+str(i)+".pdf"
							name_book = "pdf"+str(i)+".pdf"
							pdf = open("books/pdf"+str(i)+".pdf", 'wb')
							# print("response.content",response.content)
							pdf.write(response.content)

							pdf.close()
							print("File ", i, " downloaded")

						# Initiate session
							session = session.Session()
							client = session.client('s3',
													region_name='nyc3',
													endpoint_url='https://nyc3.digitaloceanspaces.com',
													aws_access_key_id=ACCESS_ID,
													aws_secret_access_key=SECRET_KEY)
													
							# client.upload_file(name)
							client.upload_file(path,  # Path to local file
							'booksdatabaseepub',  # Name of Space
							name_book)  # Name for remote file
							print("File ",name_book , " uploaded")
							

							# title_list = article_list = author_list = list()

							# for title in soup.find_all('h1',class_='post-title'):
							# 	title_list.append(title)

							# for article in soup.find_all(class_='post-content'):
							# 	article_list.append(article)

							# for author in soup.find_all(class_='author-name'):
							# 	author_list.append(author)

							# for index in range(0, len(title_list)):
							# 	title = title_list[index]
							# 	article = article_list[index]
							# 	author = author_list[index]

							# 	postgres_insert_query = """ INSERT INTO library (title_list, article_list, author_list) VALUES (%s,%s,%s)"""
							# 	record_to_insert = (title,article,author)
							# 	Cursor.execute(postgres_insert_query, record_to_insert)
						except:
							pass
	except:
			pass

	# print("All PDF files downloaded")




# print("All PDF files downloaded")
