import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from data_processing_functions.data_check import create_pandas_table, make_timestamp_column, check_price
from data_processing_functions.config import config

smtp_server = "smtp.gmail.com"
sender_email = "yourpricefinder@gmail.com"  # Enter your address
receiver_email = "name.lastname@gmail.com"  # Enter receiver address
password = config("email")['password']

msg = MIMEMultipart()
msg["Subject"] = "Price Alert"
msg["From"] = sender_email
msg["To"] = receiver_email

preferred_price_monitor = 175  # Price for which willing to buy
prices = create_pandas_table("SELECT * FROM learning.item_prices;")
make_timestamp_column(prices, 'load_date')
filtered_prices = check_price(prices, 'Monitorius', preferred_price_monitor)

html1 = """
<p>Hello,</p>
<p>Here are the latest changes to the prices of your items:</p>
"""

html2 = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(filtered_prices.to_html(index=False, float_format="%.2f", justify="left"))

html3 = """
<p>Best regards,</p>
<p>Your Price Checker</p>
"""

part1 = MIMEText(html1, 'html')
msg.attach(part1)
part2 = MIMEText(html2, 'html')
msg.attach(part2)
part3 = MIMEText(html3, 'html')
msg.attach(part3)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, msg.as_string()
    )
