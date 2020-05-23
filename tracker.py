import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_formatting as gsf 


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
worksheet = client.open("price-tracker").sheet1

def track():
    headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    URL= worksheet.col_values(3)[1:]
    f_price = []
    for i in URL:
        page = requests.get(i, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        price = soup.find(id="priceblock_ourprice").get_text()
        s_price = price.replace(',', '.')
        n_price = float(s_price[0:-2])
        f_price.append(n_price)
 
    compare(f_price)
                
def compare(f_price):

    prices = worksheet.col_values(2)[1:]
    rows = 1
    o_prices = list(map(lambda x: float(x.replace(",", ".")), prices))
     
    for a, b in zip(f_price, o_prices):
        rows += 1
        if a < b:
            worksheet.update_cell(rows, 2,a)
            fmt = gsf.CellFormat(backgroundColor=gsf.Color(0, 1, 0), textFormat=gsf.TextFormat(bold=True, foregroundColor=gsf.Color(0, 0, 0), fontSize=10)
            )
            gsf.format_cell_range(worksheet, 'B'+str(rows)+'', fmt)
            print('Product is now cheaper')
        elif a == b:
            print('Product price did not change')
        else:
            worksheet.update_cell(rows, 2, a)
            fmt = gsf.CellFormat(backgroundColor=gsf.Color(1, 0, 0), textFormat=gsf.TextFormat(bold=True, foregroundColor=gsf.Color(0, 0, 0), fontSize=10)
            )
            gsf.format_cell_range(worksheet, 'B'+str(rows)+'', fmt)
            print('Price has increased')
            
                        
track()