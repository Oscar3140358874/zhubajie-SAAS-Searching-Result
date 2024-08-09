import requests
from lxml import etree
import pandas as pd

url = "https://www.zbj.com/fw/?k=saas"
headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

resp = requests.get(url, headers=headers)

tree = etree.HTML(resp.text)
all_divs = tree.xpath('//*[@id="__layout"]/div/div[3]/div[1]/div[4]/div/div[2]/div/div[2]/div')
dic = {'Company_names': [], 'Price': [],  'Names': [], 'Sales': [], 'Evaluates': [], 'Links': []}

for divs in all_divs:
    price = divs.xpath("./div/div[3]/div[1]/span/text()")[0].strip('¥')
    dic['Price'].append(price)
    name = "saas".join(divs.xpath("./div/div[3]/div[2]/a/span/text()"))
    dic['Names'].append(name)
    company_name = divs.xpath('./div/div[5]/div/div/div/text()')[0]
    dic['Company_names'].append(company_name)
    sale = divs.xpath("./div/div[3]/div[3]/div[1]//text()")
    if len(sale) >= 2:
        sale = sale[1]
    else:
        sale = None
    dic['Sales'].append(sale)
    evaluate = divs.xpath("./div/div[3]/div[3]/div[2]//text()")
    if len(evaluate) >= 2:
        evaluate = evaluate[1]
    else:
        evaluate = None
    dic['Evaluates'].append(evaluate)
    link = divs.xpath("./div/div[3]/div[2]/a/@href")[0]
    dic['Links'].append(link)

pd.DataFrame(dic).to_excel('猪八戒saas搜索结果.xlsx', index=False)
