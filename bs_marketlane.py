from bs4 import BeautifulSoup
import requests
import re

def getInfo(coff): #coff is a list of strings that is scraped from the website with all the relevant information. The function returns a single dictionary
    coffee_dict = {
        'Name' : '',
        'Process' : '',
        'Variety' : '',
        'Origin' : '',
        'Producer' : '',
        'Relationship' : '',
        'Price': '',
        'Taste' : '',
        'Link' : '',
        'Bag' : ''
    }
    
    for k in range (0, len(coff)):
        if coff[k] == 'Origin:':
            coffee_dict['Origin'] = coff[k+1]
            j = k+2
            while True:
                if coff[j] == 'Variety:' or coff[j] == 'Varieties:':
                    break
                else:
                    coffee_dict['Origin'] += ' ' + coff[j]
                j += 1
        elif coff[k] == 'Variety:' or coff[k] == 'Varieties:':
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
                if coff[j] == 'Producer:' or coff[j] == 'Producers:':
                    break
                else:
                    coffee_dict['Process'] += ' ' + coff[j]
                j += 1
        elif coff[k] == 'Producer:' or coff[k] == 'Producers:':
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
    return coffee_dict
        
def marketlane():
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
        html = marketlane + filter_list[i]
        r = requests.get(html)
        soup = BeautifulSoup(r.text, "html.parser")
        s = str(soup)
        with open('/Users/paullee/Desktop/Coffee_emails/marketlane.html', 'w') as f:
            f.write(s)
            f.close()
        meta = soup.find_all("span", {'data-mce-fragment' : '1'})
        p = soup.find_all("p", {'data-mce-fragment' : '1'})
    
        coffee_info1 = ''
        coffee_info2 = ''
        for link in meta:
            coffee_info1 += (str(re.sub('<[^>]+>', '\n', str(link))))
        for link in p:
            coffee_info2 += (str(re.sub('<[^>]+>', '\n', str(link))))
    
        if coffee_info2 > coffee_info1:
            coffee_dict = getInfo(coffee_info2.split())
        else:
            coffee_dict = getInfo(coffee_info1.split())
    
        coffee_dict['Name'] = soup.title.string
        coffee_dict['Price'] = str(re.sub('\n', '', str(soup.find("span", {'itemprop' : 'price'}).string)).strip())
        coffee_dict['Taste'] = soup.find('div', {'class' : 'product-detail__header page__title'}).string.strip()
        coffee_dict['Link'] = marketlane + filter_list[i]
        coffee_dict['Bag'] = "https:" + soup.find('img', {'class' : 'product-detail__media--image lazyload crop-image'})['data-src']
    
        all_beans.append(coffee_dict)   
        i += 1
        
    return all_beans   
    

def writeMessage(coffInfo):
    bagList = []
    message = "Dear ${PERSON_NAME},\n\nThis is a subscription newsletter from paul_over_coffee!\nBelow are the coffees that are being offered at Leible, Marketlane and MadeofMany\n\n"
    for coffee in coffInfo:
        message += "Name: " + coffee['Name'] + '\n'
        message += "Process: " + coffee['Process'] + '\n'
        message += "Variety: " + coffee['Variety'] + '\n'
        message += "Origin: " + coffee['Origin'] + '\n'
        message += "Producer: " + coffee['Producer'] + '\n'
        message += "Relationship: " + coffee['Relationship'] + '\n'
        message += "Price: $" + coffee['Price'] + '\n'
        message += "Taste: " + coffee['Taste'] + '\n'
        message += coffee['Link'] + '\n\n'
        bagList.append(coffee['Bag'])
    
    message += "Have a good day!\npaul_over_coffee"
    with open('/Users/paullee/Desktop/Coffee_Emails/message.txt', mode='w') as f:
        f.write(message)
        f.close()
    return bagList

### Shipping ###    
# for links in soup.find_all("p"):
#     if links.string != None:
#         print(links.string)
