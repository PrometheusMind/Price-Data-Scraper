import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
import time

# User-defined variables
product_url = 'https://www.newegg.com/g-skill-64gb-288-pin-ddr4-sdram/p/N82E16820232990?quicklink=true' #URL of the product you want to track
target_price = 100.0
sender_email = 'example@gmail.com' #Sender email here
sender_password = 'Your Password Here' #Your password here
recipient_email = 'TO EMAIL HERE' # Recipient email here

# Function to scrape Amazon product page and extract product information


def scrape_amazon_product():
    page = requests.get(product_url, headers={'User-Agent': 'Mozilla/5.0'}) # Add headers to prevent 403 error
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content
    product_name = soup.title.get_text().strip() # Extract the product name from the page title

    price = float(soup.find('strong').get_text().replace('$', '')) # Extract the product price from the page. 'strong' is the HTML tag that contains the price

    return product_name, price

# Function to send email notifications


def send_email_notification():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com" # SMTP server for Gmail
    context = ssl.create_default_context() # Create a secure SSL context
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server: # Connect to the SMTP server and send the email
        server.login(sender_email, sender_password)
        message = 'Subject: Product Price Alert!\n\n' + \
                  f'The price of your product has dropped below {target_price}.\n' + \
                  f'Product URL: {product_url}'
        server.sendmail(sender_email, recipient_email, message)

# Function to check product price and send email notification if it drops to target price


def check_product_price():
    i = 0
    while True: # Run the loop until the price drops below the target price
        i += 1
        product_name, price = scrape_amazon_product()
        print(f'{product_name}: {price}: {i}')
        if price <= target_price:
            send_email_notification()
            break
        time.sleep(60)  #  Wait for 1 minute before checking again


# Run the program
check_product_price()
