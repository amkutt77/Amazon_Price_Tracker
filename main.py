from bs4 import BeautifulSoup
import requests
import smtplib
import time


PRODUCT_NAME = "Cole Haan Men's Grand Crosscourt Ii Sneaker"

PRODUCT_URL = "https://www.amazon.com/Cole-Haan-Grand-Crosscourt-Leather/dp/B07BN184VF/ref=sr_1_17?asc=1&keywords=white%2Bsneakers%2Bfor%2Bmen&qid=1645834644&refinements=p_n_size_browse-vebin%3A1285077011&rnid=1285068011&s=apparel&sprefix=white%2Bsn%2Caps%2C76&sr=1-17&th=1&psc=1"


headers = {

    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "YOUR USER AGENT HERE",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"

}

PRICE_TARGET = 105

BRUTE_FORCE_TRIES = 10

#this function will scrape the amazon web page given the url. Note that Amazon will try to detect robots and block them.
# In this case the select_one method from the beautiful soup class will return "None" instead of the correct price.
# to workaround this, I can brute force request Amazon. Keep requesting Amazon until they return the price instead of None.
# once a price is gotten, I can return it and use it to see if it's below our price target.
def scrape_amazon_data():
      
    brute_force = True
    counter = 0
    price = None # initialize price to None
    while brute_force:

        if not price is None: # if the price is found, exit the while loop
            brute_force = False
        elif counter >= BRUTE_FORCE_TRIES: # limit the number of times I request Amazon
            brute_force = False
        else: # keep trying to request Amazon until we get a price.
            response = requests.get(url = PRODUCT_URL, headers = headers)
            response_text = response.text
            soup = BeautifulSoup(response_text, "lxml")
            price = soup.select_one("span.a-offscreen")
            print(price)
            counter += 1
            time.sleep(3)
        
    price = price.getText().split("$") # returns $XX, so take out the $
    price = price[1]
    print(price)
    return float(price)


current_price = scrape_amazon_data()

def send_email_alert():
    my_email = "amkutt77@gmail.com"
    password = "XXX"
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls() 
        connection.login(user = my_email, password= password)
        message = f'''Subject: AMAZON PRICE ALERT!!
        \n\n{PRODUCT_NAME} is now less than ${PRICE_TARGET}!
          
        '''.encode('utf-8')
        

        connection.sendmail(from_addr= my_email, to_addrs="amkutt77@gmail.com", msg = message)



if current_price < PRICE_TARGET:
    print("sending email")
    send_email_alert()