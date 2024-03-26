from firebase_admin import get_app, messaging

def send_notification(notify_list=[], title='title', body='body'):
    # Define message payload.
    message = messaging.MulticastMessage
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
            image="https://pawss.vercel.app/logo512.png"
        ),
        tokens=notify_list,
    )
    try:
        response = messaging.send_multicast(message)
        print('Successfully sent meassage to firebase.')
        # Print the response for each individual message
        for idx, resp in enumerate(response.responses):
            if resp.success:
                print(f"Message {idx} sent successfully")
            else:
                print(f"Message {idx} could not be sent: {resp.exception}")
    except Exception as e:
        print(f"Failed to send message: {e}")