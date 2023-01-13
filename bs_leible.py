from bs4 import BeautifulSoup
import requests


url = "https://leiblecoffee.com.au/collections/single-origin"
leible = "https://leiblecoffee.com.au/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# with open('/Users/paullee/Desktop/Coffee_emails/leible.html', 'w') as f:
#     d = str(doc)
#     f.write(d)
#     f.close()

# print(doc.find_all('a'))

filter_list = []  # <- Stores https links of all the single-origin coffee
info_list = []    # <- Stores https links of all the coffee information ()
all_beans = []    # <- Stores coffee dictionary for us to use later to write messages to the clients

 ## scraping single-origin information (Flavour, Region, Altitude, Variety, Process, Farm)
for link in doc.find_all('a'):
    if '/products' in link.get('href') and ((leible + link.get('href')) not in filter_list) and ('drip-bag' not in link.get('href')):
        filter_list.append(leible + link.get('href'))

i = 0
while i < len(filter_list):
    r = requests.get(filter_list[i])
    soup = BeautifulSoup(r.text, "html.parser")

    coffee_dict = {
        'Name'  : '',
        'Price' : '',
        'Photo' : ''
    }

    coffee_dict['Name'] = soup.title.string.strip()
    coffee_dict['Price'] = '$' + soup.find('meta', {'property' : 'product:price:amount'}).get('content')

    photo = soup.find('img', {'data-widths' : '[200,400,600,700,800,900,1000]'})

    if photo == None:
        x = soup.title.string.strip()
        y = x.split()
        for link in soup.find_all('img'):
            if (y[0] in link.get('alt')) and link.get('src') != None:
                if 'png' in link.get('src') and 'products' in link.get('src'):
                    photo = ("https:" + link.get('src'))
    else:
        photo = 'https:' + photo.get('data-original-src')
    
    coffee_dict['Photo'] = photo
    all_beans.append(coffee_dict)
    i += 1

for item in all_beans:
    print('Name: ' + item['Name'])
    print('Price: ' + item['Price'])
    print('Photo Link: ' + item['Photo'])
    print('\n\n')
    


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
    
