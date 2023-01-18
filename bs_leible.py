from bs4 import BeautifulSoup
import requests




def leible():
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

    return all_beans
    
def writeMessage(coffInfo):
    bagList = []
    message = "Dear ${PERSON_NAME},\n\nThis is a subscription newsletter from paul_over_coffee!\nBelow are the coffees that are being offered at Leible\n\n"
    for coffee in coffInfo:
        message += "Name: " + coffee['Name'] + '\n'
        message += "Price: $" + coffee['Price'] + '\n'
        bagList.append(coffee['Photo'])
    
    message += "Have a good day!\npaul_over_coffee"
    with open('/Users/paullee/Desktop/Coffee_Emails/message.txt', mode='w') as f:
        f.write(message)
        f.close()
    return bagList
