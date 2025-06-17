from twilio.rest import Client

def send_sms_alert(body, to):
    # Replace with your real credentials
    account_sid = 'AC6146d11240d328be994a679320bf5096'
    auth_token = '3ed0b0c20d7f597bce65f543d206a970'
    from_number = '+17754166423'
    
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to
    )

    print(f"SMS sent! SID: {message.sid}")
