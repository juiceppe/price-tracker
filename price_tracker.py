import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

def main():
    URL = input("Enter URL of the product you want to track: ")
    scrap(URL)

def scrap(URL):
    
    headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    c_price = price[0:]

    sheet(title, c_price)

def sheet(title, c_price):
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("price-tracker").sheet1  # Open the spreadhseet
    
    sheet.update_cell(2,1, title.strip())  #Update cell A2 with the name of the product
    sheet.update_cell(2,2, c_price)  # Update cell B2 with the price of the product
    #numRows = sheet.row_count  # Get the number of rows in the sheet


if __name__ == '__main__':
    main()