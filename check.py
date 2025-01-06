from email.mime.text import MIMEText
import smtplib

def test_email():
    subject = "Test Email"
    body = "This is a test email from Python script."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'gagan.mspl@gmail.com'
    msg['To'] = 'gagan.mspl@gmail.com'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('gagan.mspl@gmail.com', 'vrwnqqvwzmktpjgg')
        server.send_message(msg)
        server.quit()
        print("Test Email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {e}")

test_email()
