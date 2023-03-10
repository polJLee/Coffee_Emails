import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from html2image import Html2Image

from bs_marketlane import marketlane
from bs_marketlane import writeMessage as marketlane_write

from bs_leible import leible
from bs_leible import writeMessage as leible_write


MY_ADDRESS = 'poljunhyeok@outlook.com'
PASSWORD = 'povcoffee58290'
contacts = '/Users/paullee/Desktop/Coffee_Emails/contacts.txt'
message_path = '/Users/paullee/Desktop/Coffee_Emails/message.txt'


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    # bagList = marketlane_write(marketlane())
    bagList = leible_write(leible())
    hti = Html2Image()
    names, emails = get_contacts(contacts)
    message_template = read_template(message_path)

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    
    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        message = message_template.substitute(PERSON_NAME=name.title())
        
        print(message)
        
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Coffee Newsletter"
        i = 0
        while i < len(bagList):
            bag = bagList[i]
            print(bag)
            hti.screenshot(url = bag)
            fp = open('screenshot.png', mode='rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msg.attach(msgImage)
            i += 1

        msg.attach(MIMEText(message,'plain'))

        s.send_message(msg)
        del msg
    s.quit()

if __name__ == '__main__':
    main()