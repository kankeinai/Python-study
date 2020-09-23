import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path  # os.path


def notify(first_page, last_page):
    html = Template(Path('downloader.html').read_text())
    email = EmailMessage()
    email['from'] = 'Yummy'
    email['to'] = 'milka3341@gmail.com'
    email['subject'] = 'YummyDownloader'
    email.set_content(html.substitute(
        {'first_page': first_page, 'last_page': last_page}), 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('reiko.off@gmail.com', 'reikoisthebest_1')
        smtp.send_message(email)
