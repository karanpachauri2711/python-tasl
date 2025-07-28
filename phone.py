from twilio.rest import Client

# Your credentials from Twilio dashboard
account_sid = 'AC0aa0d93e8bdba04e37655203a005dcf6'
auth_token = 'b5285fa54f77e95e43615a4216a823fc'
twilio_number = '+1 618 328 4965'  # Your Twilio phone number
target_number = '+919079384343'  # The number you want to call

client = Client(account_sid, auth_token)

# Make the call
call = client.calls.create(
    to=target_number,
    from_=twilio_number,
    url='http://demo.twilio.com/docs/voice.xml'  # TwiML instructions
)

print(f"Call initiated. SID: {call.sid}")
