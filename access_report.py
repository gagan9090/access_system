import smtplib
from email.mime.text import MIMEText
import sqlite3
import datetime
import schedule
import time

import logging

# Configure logging
logging.basicConfig(
    filename="system_usage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

'''def send_email_report():
    logging.info("Starting send_email_report...")
    conn = sqlite3.connect('system_usage.db')
    cursor = conn.cursor()
    today = datetime.datetime.now().date()
    cursor.execute('SELECT * FROM usage WHERE date=?', (str(today),))
    data = cursor.fetchone()
    conn.close()

    if data:
        subject = f"System Usage Report for {today}"
        body = f"Date: {data[0]}\nBoot Time: {data[1]}\nShutdown Time: {data[2]}\nMost Used App: {data[3]}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'gagan.mspl@gmail.com'
        msg['To'] = 'gagan.mspl@gmail.com'

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('gagan.mspl@gmail.com', 'vrwnqqvwzmktpjgg')
            server.send_message(msg)
            server.quit()
            logging.info("Email sent successfully!")
        except Exception as e:
            logging.error(f"Error sending email: {e}")
    else:
        logging.warning("No data found for today.")
'''

def send_email_report():
    conn = sqlite3.connect('system_usage.db')
    cursor = conn.cursor()
    today = datetime.datetime.now().date()
    cursor.execute('SELECT * FROM usage WHERE date=?', (str(today),))
    data = cursor.fetchone()
    conn.close()

    # ✅ Ensure data exists and handle missing values
    if data:
        date = data[0]
        boot_time = data[1]
        shutdown_time = data[2] if data[2] else "Not Recorded"
        most_used_app = data[3] if data[3] else "Not Recorded"

        # ✅ Email Content
        subject = f"System Usage Report for {today}"
        body = f"""
        Date: {date}
        Boot Time: {boot_time}
        Shutdown Time: {shutdown_time}
        Most Used Application: {most_used_app}
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'gagan.mspl@gmail.com'
        msg['To'] = 'gagan.mspl@gmail.com'

        # ✅ Send the email
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('gagan.mspl@gmail.com', 'vrwnqqvwzmktpjgg')  # App Password
            server.send_message(msg)
            server.quit()
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Error sending email: {e}")
    else:
        print("❌ No data found for today.")
# Ensure the database and boot time are logged at startup
def init_db():
    conn = sqlite3.connect('system_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage (
            date TEXT,
            boot_time TEXT,
            shutdown_time TEXT,
            most_used_app TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_boot_time():
    conn = sqlite3.connect('system_usage.db')
    cursor = conn.cursor()
    boot_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.now().date()
    cursor.execute('INSERT INTO usage (date, boot_time) VALUES (?, ?)', (str(today), boot_time))
    conn.commit()
    conn.close()

def log_shutdown_time():
    conn = sqlite3.connect('system_usage.db')
    cursor = conn.cursor()
    shutdown_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE usage SET shutdown_time=? WHERE date=?', (shutdown_time, str(datetime.datetime.now().date())))
    conn.commit()
    conn.close()

# Initialize and schedule tasks
init_db()
log_boot_time()
#schedule.every().day.at("23:59").do(send_email_report)
send_email_report()
schedule.every().day.at("23:58").do(log_shutdown_time)

# Keep the script running continuously
while True:
    schedule.run_pending()
    time.sleep(60)
