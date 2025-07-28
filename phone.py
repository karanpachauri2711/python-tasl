from twilio.rest import Client

# Your credentials from Twilio dashboard
account_sid = input()
auth_token = input()
twilio_number = input(' Yor Twilio phone number')
target_number = input('The number you want to call')

client = Client(account_sid, auth_token)

# Make the call
call = client.calls.create(
    to=target_number,
    from_=twilio_number,
    url='http://demo.twilio.com/docs/voice.xml'  # TwiML instructions
)

print(f"Call initiated. SID: {call.sid}")
