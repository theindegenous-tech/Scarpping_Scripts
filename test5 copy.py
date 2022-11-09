import requests
import json, boto3,os, sys, uuid
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')
from bs4 import BeautifulSoup 

def lambda_handler(event, context):
    bucket_name = "indegenous-epub-library"

    # URL from which pdfs to be downloaded
    url = "https://universitypress.whiterose.ac.uk/site/books/"
    
    # Requests URL and get response object
    response = requests.get(url)
    
    # Parse text obtained
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all hyperlinks present on webpage
    links = soup.find_all('a')
    
    i = 0
    
    # From all links check for pdf link and
    # if present download file
    for link in links:
    	if ('/site/books/10.22599/' in link.get('href', [])):

    		i += 1
    
    		print("link",link)
   
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
    # 		response = requests.get(comp_url)
    
    		response = requests.get(comp_url, stream=True)
    		# Write content in pdf file
    		if(data_type):
                
    		    file_name = "my_test_file.csv"
    		    
    		    lambda_path = "/tmp/" + file_name
                s3_path = "output/" + file_name
                os.system('echo testing... >'+lambda_path)
                s3 = boto3.resource("s3")
                s3.meta.client.upload_file(lambda_path, bucket_name, file_name)
    		    
                # s3url = 's3://' + bucket + '/' + key
                with smart_open(s3, 'wb') as fout:
                    fout.write(response.content)
                    		    
    			pdf = open("pdf"+str(i)+"."+cate, 'wb')
    			pdf.write(response.content)
    			pdf.close()
    			print("File ", i, " downloaded")
    
    print("All PDF files downloaded")