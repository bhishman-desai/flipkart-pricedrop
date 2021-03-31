import smtplib
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

def initt():
    global URL_list
    global price_check
    global headers
    """ Add products and prices in respective arrays """
    URL_list = [
        'https://www.flipkart.com/hp-omen-ryzen-5-hexa-core-4600h-8-gb-512-gb-ssd-windows-10-home-6-graphics-nvidia-geforce-gtx-1660-ti-15-en0002ax-gaming-laptop/p/itm8837de99c3094?pid=COMFSTFFCG7CQW52&lid=LSTCOMFSTFFCG7CQW52SKMQBE&marketplace=FLIPKART&fm=neo%2Fmerchandising&iid=M_9d38bbbc-8bf9-42a0-8457-5b1886462f3d_6_PFK4M0QPCBD3_MC.COMFSTFFCG7CQW52&ppt=clp&ppn=gaming-laptops-store&ssid=r97gc6koy80000001597905111895&otracker=clp_pmu_v2_HP%2BGaming%2BLaptops_2_6.productCard.PMU_V2_HP%2BGaming%2BLaptops_gaming-laptops-store_COMFSTFFCG7CQW52_neo%2Fmerchandising_1&otracker1=clp_pmu_v2_PINNED_neo%2Fmerchandising_HP%2BGaming%2BLaptops_LIST_productCard_cc_2_NA_view-all&cid=COMFSTFFCG7CQW52',
        'https://www.flipkart.com/mivi-mfi-certified-6ft-long-nylon-braided-original-tough-2-m-lightning-cable/p/itmeguz74zdhaxrz?pid=ACCEGUZ7ZEUBBDPB&lid=LSTACCEGUZ7ZEUBBDPBXQ2JKA&marketplace=FLIPKART&spotlightTagId=BestsellerId_tyy%2F4mr%2F3nu&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&fm=SEARCH&iid=77bce695-4fbf-4893-8d9b-12c0d8a6e16e.ACCEGUZ7ZEUBBDPB.SEARCH&ppt=sp&ppn=sp&ssid=jwcdkj12jk0000001601649096382&qH=801895e1b7efeefc'
    ]
    price_check = [60000.0, 5000.0]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.130 Safari/537.36'}


def check_price():
    initt()
    page_list = []
    soup_list = []
    title_list = []
    price_list = []
    for x in URL_list:
        page_list.append(requests.get(x, headers=headers))
    for x in page_list:
        soup_list.append(BeautifulSoup(x.content, 'html.parser'))
    for x in soup_list:
        title_list.append(x.find("span", {"class": "B_NuCI"}).get_text())
        price_list.append(float(x.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text()[1:].replace(',', '')))

    for x in range(len(title_list)):
        print(title_list[x] + '-->', price_list[x])
        print()
        title_list[x] = ''.join(char for char in title_list[x] if ord(char) < 128)

    for x in range(len(price_list)):
        if price_list[x] < price_check[x]:
            sendmail(title_list[x], price_list[x], URL_list[x])
            sendsms(title_list[x], price_list[x], URL_list[x])

    return title_list, price_list


def sendmail(t, p, URL):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('cadbpd@gmail.com', 'sai30541')

    subject = 'Hey! Price fall for ' + t
    body = 'Current price for ' + t + ' is :' + str(p) + '\n\nCheck the link :' + URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('sender_email@gmail.com', 'desaibhishman1@gmail.com', msg)

    print('Email Sent')

    server.quit()


def sendsms(t, p, URL):
    account_sid = 'ACc6e8959843a234f62cf75ea7a608d348'
    auth_token = 'ff78440a3fe4bcaf711638923ba93e56'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body='Current price for ' + t + ' is :' + str(p) + '\n\nCheck the link :' + URL,
        from_='+14155944862',
        to='+919429474388'
    )
    if message.sid:
        print('SMS Sent')
