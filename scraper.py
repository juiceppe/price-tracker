import requests
from bs4 import BeautifulSoup
import gspread
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
worksheet = client.open("price-tracker").sheet1

def main():
    URL = input("Enter URL of the product you want to track: ")
    scrap(URL)

def scrap(URL):
    
    headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    s_price = price.replace(',', '.')
    c_price = float(s_price[0:-2])
    sheet(title, c_price, URL)

def sheet(title, c_price, URL):  # Open the spreadhseet
    data = [title.strip(), c_price, URL]
    firstRow = worksheet.cell(2,3).value
       
    if firstRow == '':
        worksheet.insert_row(data, 2)
        print('Product inserted correctly')
    elif firstRow != URL:
        worksheet.insert_row(data, 2)
    else:
        print('Product is already tracked')
    

if __name__ == '__main__':
    main()