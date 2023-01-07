from bs4 import BeautifulSoup
import requests
import shutil
import re

url = "https://marketlane.com.au/pages/coffee"
marketlane = "https://marketlane.com.au/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

list = []
filter_list = []


for link in doc.find_all('a'):
    if link.get('href') != None:
        list.append(link.get('href'))

for item in list:
    if 'filter-beans' in item and (item not in filter_list):
        filter_list.append(item)

all_beans = []
i = 0
while i < len(filter_list):
    coffee_dict = {
        'Name' : '',
        'Process' : '',
        'Variety' : '',
        'Origin' : '',
        'Producer' : '',
        'Relationship' : '',
        'Price': '',
        'Taste' : ''
    }
    print(filter_list[1])
    html = marketlane + filter_list[i]
    r = requests.get(html)
    soup = BeautifulSoup(r.text, "html.parser")
    s = str(soup)

    with open('/Users/paullee/Desktop/Coffee_emails/marketlane.html', 'w') as f:
        f.write(s)
        f.close()


    meta = soup.find_all("span", {'data-mce-fragment' : '1'})

    coffee_dict['Name'] = soup.title.string
    coffee_dict['Price'] = str(re.sub('\n', '', str(soup.find("span", {'itemprop' : 'price'}).string)).strip())
    coffee_dict['Taste'] = soup.find('div', {'class' : 'product-detail__header page__title'}).string.strip()



    coffee_info = ''
    for link in meta:
        coffee_info += (str(re.sub('<[^>]+>', '\n', str(link))))

    # print(coffee_info)
    coff = coffee_info.split()
    # print(coff)


    for k in range (0, len(coff)):

        if coff[k] == 'Origin:':
            coffee_dict['Origin'] = coff[k+1]
            j = k+2
            while True:
                if coff[j] == 'Variety:':
                    break
                else:
                    coffee_dict['Origin'] += ' ' + coff[j]
                j += 1
        elif coff[k] == 'Variety:':
            coffee_dict['Variety'] = coff[k+1]
            j = k+2
            while True:
                if coff[j] == 'Process:':
                    break
                else:
                    coffee_dict['Variety'] += ' ' + coff[j]
                j += 1
        elif coff[k] == 'Process:':
            coffee_dict['Process'] = coff[k+1]
            j = k+2
            while True:
                if coff[j] == 'Producer:':
                    break
                else:
                    coffee_dict['Process'] += ' ' + coff[j]
                j += 1
        elif coff[k] == 'Producer:':
            coffee_dict['Producer'] = coff[k+1]
            j = k+2
            while True:
                if 'Relationship' in coff[j]:
                    break
                else:
                    coffee_dict['Producer'] += ' ' + coff[j]
                j += 1
        elif 'Relationship' in coff[k] and (coff[k+1] == 'length:' or coff[k+1] == 'Length:'):
            coffee_dict['Relationship'] = coff[k+2]
            j = k+3
            while True:
                if len(coff) == j:
                    break
                else:
                    coffee_dict['Relationship'] += ' ' + coff[j]
                j += 1
        k += 1
    all_beans.append(coffee_dict)   
    i += 1         
    
for beans in all_beans:
    print(beans['Name'])
    print(beans['Variety'])
    print(beans['Origin'])
    print(beans['Producer'])
    print(beans['Relationship'])
    print(beans['Process'])
    print(beans['Price'])
    print(beans['Taste'])
    print('\n')

    
    
# bag = "https:" + soup.find('img', {'class' : 'product-detail__media--image lazyload crop-image'})['data-src']

    







def save_bag(bag):
    res = requests.get(bag, stream=True)
    if res.status_code == 200:
        with open((coffee_dict['Name']+'.png'), 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print("Image successfully downloaded: ", (coffee_dict['Name']+'.jpg'))
        # print(bag)
    else:
        print("Image couldn''t be retrieved\n")

### Shipping ###

# for links in soup.find_all("p"):
#     if links.string != None:
#         print(links.string)



# for links in filter_list:
#     r = requests.get(links)
#     soup = BeautifulSoup(r.text, "html.parser")
#     print(soup.)