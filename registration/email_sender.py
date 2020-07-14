import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path  # os.path


def restore(mail, code):
    html = Template(Path('restore.html').read_text())
    email = EmailMessage()
    email['from'] = 'Registration'
    email['to'] = mail
    email['subject'] = 'Password recovery'
    email.set_content(html.substitute(
        {'login': mail.split("@")[0], 'garbage': code}), 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('reiko.off@gmail.com', 'reikoisthebest_1')
        smtp.send_message(email)


def confirm(mail, code):
    html = Template(Path('confirmation.html').read_text())
    email = EmailMessage()
    email['from'] = 'Registration'
    email['to'] = mail
    email['subject'] = 'Email confirmation'
    email.set_content(html.substitute(
        {'login': mail.split("@")[0], 'garbage': code}), 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('reiko.off@gmail.com', 'reikoisthebest_1')
        smtp.send_message(email)
