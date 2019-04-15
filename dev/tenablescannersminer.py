import requests
import pandas as pd
from bs4 import BeautifulSoup

url = requests.get('https://docs.tenable.com/cloud/Content/Scans/Scanners.htm')

html_soup = BeautifulSoup(url.content,'lxml')
table = html_soup.find_all('table')[0]
print(type(table))
df = pd.read_html(str(table))[0]
#print df
result = df[df.columns[1]].tolist()
print(result)