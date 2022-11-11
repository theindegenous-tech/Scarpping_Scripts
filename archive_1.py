
from sqlite3 import Cursor
import psycopg2
import requests
from bs4 import BeautifulSoup
import uuid
import random



from boto3 import session
import boto3
from botocore.client import Config

ACCESS_ID = 'DO00DZN9YDVM4H4QKLPE'
SECRET_KEY = 'TJZGQgbfYS7aES8D9H/h5+/hDutOyn8BGwfhRmSdc1c'


def connectSQL(ID,title,url):
		try:
			connection = psycopg2.connect(user="admin",
										password="admin",
										host="127.0.0.1",
										port="5432",
										database="library")
			cursor = connection.cursor()
			postgres_insert_query = """INSERT INTO the_indegenous_backend_book (id,title,description,year,url) VALUES  (%s,%s,%s,%s,%s)"""
			record_to_insert = (ID,title,'desc',2022,url)
			cursor.execute(postgres_insert_query, record_to_insert)
			# cursor.execute(postgres_insert_query)

			connection.commit()
			count = cursor.rowcount
			print(count, "Record inserted successfully into mobile table")

		except (Exception, psycopg2.Error) as error:
			print("Failed to insert record into mobile table", error)
		
# connectSQL()
# connectSQL(111,"title","https://booksdatabaseepub.nyc3.digitaloceanspaces.com/{filename}")

# URL from which pdfs to be downloaded
url = "https://archive.org/details/cdl"

# Requests URL and get response object
response = requests.get(url,timeout=600) 

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hyperlinks present on webpage
links = soup.find_all(class_ = "item-ttl C C2")

i = 0

# From all links check for pdf link and
# if present download file
for link in links:
	
	# print(link)
	try:
		ans = link.find('a')['href']
		print("ans",ans)
		filename = ans.split('/')[-1]
		print("filename",filename)

		comp_url =( "https://archive.org/"+ans)

		# data_type =link.get('data-category')
		response_2 = requests.get(comp_url,timeout=600) 
			# Parse text obtained
		soup = BeautifulSoup(response_2.text, 'html.parser')
		# Find all hyperlinks present on webpage
		links_2 = soup.find_all(class_ = "format-summary download-pill")
		title = soup.find(class_ = "breaker-breaker").text
		print("title",title)
	# except:
	# 	break
		for hit in links_2:
    			
				i=i+1
				hit_detail = hit.text.strip()	
				if(hit_detail == "EPUB              download"):
						try:
							# print("yes inside",hit['href'])
							
							comp_url =( "https://archive.org"+hit['href'])
							print("comp_url",comp_url)
							response = requests.get(comp_url,timeout=600) 
							path = "books/"+filename+".epub"
							name_book = filename+".epub"
							
							idd = ''.join(str(random.randint(0,10)) for x in range(6))
							print("idd",idd)

							pdf = open("books/"+name_book, 'wb')
							# print("response.content",response.content)
							pdf.write(response.content)

							pdf.close()
							print("File ", i, " downloaded")

						# Initiate session
							try:
								session = session.Session()
								boto3.setup_default_session(session=session)
								client = session.client('s3',
														region_name='nyc3',
														endpoint_url='https://nyc3.digitaloceanspaces.com',
														aws_access_key_id=ACCESS_ID,
														aws_secret_access_key=SECRET_KEY)
														
								# client.upload_file(name)
								client.upload_file(path,  # Path to local file
								'booksdatabaseepub',  # Name of Space
								filename)  # Name for remote file
								connectSQL(idd,title,f'https://booksdatabaseepub.nyc3.digitaloceanspaces.com/{filename}')

								print("File ",filename , " uploaded")
							except Exception as ex:
								template = "An exception of type {0} occurred. Arguments:\n{1!r}"
								message = template.format(type(ex).__name__, ex.args)
								print (message)

							
						except Exception as ex:
							template = "An exception of type {0} occurred. Arguments:\n{1!r}"
							message = template.format(type(ex).__name__, ex.args)
							print (message)
							
	except Exception as ex:
		
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print (message)



	# print("All PDF files downloaded")




# print("All PDF files downloaded")
