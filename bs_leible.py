from bs4 import BeautifulSoup
from bs_marketlane import getInfo

import requests
import re

url = "https://leiblecoffee.com.au/collections/single-origin"
leible = "https://leiblecoffee.com.au/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# with open('/Users/paullee/Desktop/Coffee_emails/leible.html', 'w') as f:
#     d = str(doc)
#     f.write(d)
#     f.close()



# print(doc.find_all('a'))

filter_list = []

for link in doc.find_all('a'):
    if '/products' in link.get('href') and ((leible + link.get('href')) not in filter_list) and ('drip-bag' not in link.get('href')):
        filter_list.append( leible + link.get('href'))
        # print(link.get('href'))  
r = requests.get(filter_list[0])
soup = BeautifulSoup(r.text, "html.parser")
# with open('/Users/paullee/Desktop/Coffee_emails/leible.html', 'w') as f:
#     f.write(str(soup))
#     f.close()
print(filter_list[0])
# print(soup.title.string.strip()) # Name
x = soup.title.string.strip()
y = x.split()
# print(y[0])

for link in soup.find_all('img'):
    if y[0] in link.get('alt'):
        print(link.get('src'))
# print(soup.find_all('img'))



all_beans = []
i = 0




# while i < len(filter_list):
# html = leible + filter_list[i]
# r = requests.get(html)
# soup = BeautifulSoup(r.text, "html.parser")
# s = str(soup)
# with open('/Users/paullee/Desktop/Coffee_emails/leible.html', 'w') as f:
#     f.write(s)
#     f.close()
        
    # meta = soup.find_all("span", {'data-mce-fragment' : '1'})
    # p = soup.find_all("p", {'data-mce-fragment' : '1'})

    # coffee_info1 = ''
    # coffee_info2 = ''
    # for link in meta:
    #     coffee_info1 += (str(re.sub('<[^>]+>', '\n', str(link))))
    # for link in p:
    #     coffee_info2 += (str(re.sub('<[^>]+>', '\n', str(link))))

    # if coffee_info2 > coffee_info1:
    #     coffee_dict = getInfo(coffee_info2.split())
    # else:
    #     coffee_dict = getInfo(coffee_info1.split())

    # coffee_dict['Name'] = soup.title.string
    # coffee_dict['Price'] = str(re.sub('\n', '', str(soup.find("span", {'itemprop' : 'price'}).string)).strip())
    # coffee_dict['Taste'] = soup.find('div', {'class' : 'product-detail__header page__title'}).string.strip()
    # coffee_dict['Link'] = leible + filter_list[i]
    # coffee_dict['Bag'] = "https:" + soup.find('img', {'class' : 'product-detail__media--image lazyload crop-image'})['data-src']

    # all_beans.append(coffee_dict)   
    # i += 1
    
