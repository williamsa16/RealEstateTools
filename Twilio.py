import pandas as pd
import twilio
from twilio.rest import Client

# Twilio API credentials
account_sid = "AC2b8848610ca5596a4f608f08b7e0e003"
auth_token = "dbb9bc2ecdebfe54e5f586dbb9f48074"
twilio_phone_number = "18884771675"

# Read phone numbers and message bodies from Excel file
data = pd.read_excel("/Users/austinwilliams/Real Estate Analysis/ContactList.xlsx")  # Replace with your Excel/CSV file path
phone_numbers = data["Phone Number "].tolist()
message_bodies = data["Message Body"].tolist()
names = data["Names"].tolist()
addresses = data["Addresses"].tolist()

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Iterate over phone numbers and send personalized SMS messages
for phone_number, message_body, name, address in zip(phone_numbers, message_bodies, names, addresses):
    # Send an SMS
    message = client.messages.create(
        body='Hi ' + name+',' + " I got your number from city records. Any thought to sell " + address+"? If so, give me a text/call at 904-571-7199 or visit us online at Stratmgt.co "+ message_body,
        from_=twilio_phone_number,
        to='1'+(str(phone_number))
    )

    # Print the message SID
    print("Message SID:", message.sid)

