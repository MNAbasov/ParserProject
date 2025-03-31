import requests
from bs4 import BeautifulSoup as BS
import pandas as pd


def repin_parser(url = str, max_count = int):
    page = 1
    watched_pictures = 0
    
    global info_df
    info_df = {'Артикул':[],
               'Цена':[],
               'Размер':[]
               }
    while watched_pictures < max_count:
        response = requests.get(url)
        soup = BS(response.text, 'lxml')
        pictures = soup.find_all('div', class_ = 'loop-post loop-product')
        for picture in pictures:
            if watched_pictures>= max_count:
                break
            watched_pictures+=1    
            articule = picture.find('div', class_ = 'param-value').text
            info_df['Артикул'].append(articule)
            price = picture.find('span', 'price new').text
            new_price = price.replace(' ','')
            info_df['Цена'].append(new_price)
            x = picture.find('li', class_ = 'param param-size')
            size = x.find('div', class_ = 'param-value').text
            info_df['Размер'].append(size)

        create_excel()
        page+=1
    

def create_excel():
    with pd.ExcelWriter ('repin.xlsx', mode='w') as writer1:
        df1 = pd.DataFrame(info_df)
        df1.to_excel(writer1,sheet_name='Картины репина', index=False)

if __name__ == '__main__':  
    repin_parser(url = 'https://repin-print.ru/catalog/interernye-kartiny-interernye-kartiny/',max_count=160)
