import base64
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup


def get_html_from_email(msg):
    html_content = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition and "text/html" in content_type:
                body = part.get_payload(decode=True)
                html_content = body.decode("utf-8")
    else:
        html_content = msg.get_payload(decode=True).decode("utf-8")
    return html_content


def mail_getting(email_name, password):

    email_address = email_name
    password = password

    mail = imaplib.IMAP4_SSL("mail.your-server.de", port=993)
    mail.login(email_address, password)
    print(mail.list())
    try:
        mail.select("INBOX.spambucket")

        status, messages = mail.uid("SEARCH", None, "ALL")
        message_ids = messages[0].split()

        for mail_id in message_ids[::-1]:
            # Получение заголовков письма
            _, msg_data = mail.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Извлечение информации из заголовков
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_ = msg.get("From")

            if from_ == "UEFA <no-reply@uefa.com>":
                html_content = get_html_from_email(msg)
                soup = BeautifulSoup(html_content, 'lxml')
                main_body_text = soup.find("html").text
                code = [i for i in main_body_text.split("\n") if i.isdigit()]
                mail.logout()
                return code[0]
    except:
        mail.select("INBOX")

        status, messages = mail.uid("SEARCH", None, "ALL")
        message_ids = messages[0].split()

        for mail_id in message_ids[::-1]:
            # Получение заголовков письма
            _, msg_data = mail.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Извлечение информации из заголовков
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_ = msg.get("From")

            if from_ == "UEFA <no-reply@uefa.com>":
                html_content = get_html_from_email(msg)
                soup = BeautifulSoup(html_content, 'lxml')
                main_body_text = soup.find("html").text
                code = [i for i in main_body_text.split("\n") if i.isdigit()]
                mail.logout()
                return code[0]
