from bs4 import BeautifulSoup
import requests
import shutil

url = "https://marketlane.com.au/pages/coffee"
marketlane = "https://marketlane.com.au/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

list = []
filter_list = []

coffee_dict = {
    'Name' : '',
    'Process' : '',
    'Variety' : '',
    'Origin' : '',
    'Producer' : '',
    'relationship' : '',
    'Price': ''
}




for link in doc.find_all('a'):
    if link.get('href') != None:
        list.append(link.get('href'))

for item in list:
    if 'filter-beans' in item and (item not in filter_list):
        filter_list.append(item)

# print(filter_list)
# print(filter_list[0])
r = requests.get(marketlane + filter_list[1])
soup = BeautifulSoup(r.text, "html.parser")
s = str(soup)

# with open('/Users/paullee/Desktop/marketlane.html', 'w') as f:
#     f.write(s)
#     f.close()

span = soup.find_all("span")
# print(span)

for links in soup.find_all("span"):
    l = links.string
    if l == None:
        continue
    if 'Variety' in l:
        coffee_dict['Variety'] = l
    elif 'Origin' in l:
        coffee_dict['Origin'] = l
    elif 'Producer' in l:
        coffee_dict['Producer'] = l
    elif 'Relationship' in l:
        coffee_dict['Relationship'] = l
    elif 'Process' in l:
        coffee_dict['Process'] = l
    elif '$' in l and l != '$':
        coffee_dict['Price'] = "Price: " + l.strip()

coffee_dict['Name'] = soup.title.string

# print(type(soup.find('img', {'class' : 'product-detail__media--image lazyload crop-image'})))

bag = "https:" + soup.find('img', {'class' : 'product-detail__media--image lazyload crop-image'})['data-src']




res = requests.get(bag, stream=True)

if res.status_code == 200:
    with open((coffee_dict['Name']+'.png'), 'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print("Image successfully downloaded: ", (coffee_dict['Name']+'.jpg'))
    # print(bag)
else:
    print("Image couldn''t be retrieved\n")




# print(soup.find_all('img').string)

### Shipping ###

# for links in soup.find_all("p"):
#     if links.string != None:
#         print(links.string)



# for links in filter_list:
#     r = requests.get(links)
#     soup = BeautifulSoup(r.text, "html.parser")
#     print(soup.)