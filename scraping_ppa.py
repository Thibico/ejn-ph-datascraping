# from playwright.sync_api import sync_playwright, Page, expect
import pandas as pd
import requests
from bs4 import BeautifulSoup


def cols_number_df(df):
    return df.shape[1]

def get_table_df(table):
    cols = []
    for th in table.find('tr').find_all('th'):
        cols.append(th.get_text(strip=True))

    data = []
    for row in table.find_all('tr')[1:]:
        rowData = []
        for td in row.find_all('td'):
            check = td.find('a')
            if check:
                url = check.get('href')
                rowData.append(url)
            else:
                text = td.get_text(strip=True)
                rowData.append(text)
        data.append(rowData)

    df = pd.DataFrame(data, columns= cols)
    return df
            
correct_dfs = []
error_dfs = []
all_data = pd.DataFrame()
for page_number in range(0,170):
    page_url = f"https://www.ppa.com.ph/projects?page={page_number}"

    resp = requests.get(page_url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('table', {'class': 'views-table'})
        table_df = get_table_df(table)
        if cols_number_df(table_df) == 10:
            print(f"Correct DF for page:{page_number}")
            correct_dfs.append(table_df)
        else:
            print(f"Wrong shape {table_df.shape} for page:{page_number}")
            error_dfs.append(table_df)        
    else:
        print("Can't access to Page")
    print(f"-----xPage:{page_number} done!x-----")

all_data = pd.concat(correct_dfs, ignore_index=True)
all_data.to_csv('result_data/ppa_data.csv',encoding='utf-8')

print(all_data.shape)
print(all_data.columns)
  
        
    








'''
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page_index = 1
    page.goto(f"https://www.ppa.com.ph/projects?page={page_index}")
    print(page.title())
    
    tables = pd.read_html(page.content())
    print(f"Total : {len(tables)}")
    df = tables[0]
    print(df.head())
    print(df.shape)
    browser.close()
'''
    