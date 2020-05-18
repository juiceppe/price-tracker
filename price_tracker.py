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
    c_price = price[0:-1]

    sheet(title, c_price, URL)

def sheet(title, c_price, URL):
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("price-tracker").sheet1  # Open the spreadhseet
    
    data = [title.strip(), c_price, URL]
    sheet.insert_row(data, 2)  # Populate always the second row, without overwriting the one before

    #sheet.update_cell(4,1, title.strip())  #Update cell A2 with the name of the product
    #sheet.update_cell(4,2, c_price)  # Update cell B2 with the price of the product
    #sheet.update_cell(4,3, URL) #Stores the value of the URL to check the price and update it
    

if __name__ == '__main__':
    main()