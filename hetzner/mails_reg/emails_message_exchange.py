import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hetzner.databases_manage.database_scripts import update_hetzner_acc_date,\
    update_hetzner_acc_addressee, update_hetzner_acc_last_msg


def message_exchange(accounts):
    for idx, acc in enumerate(accounts):
        try:
            subject = "Hi, John!"

            body = "Hope you're doing well. How's your day going?" \
                   " Let's catch up soon and have a chat." \
                   " I've got a couple of interesting stories to share." \
                   " Remember, always happy to hang out!"
            sender_email, sender_password, recipient_email = acc
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("mail.your-server.de", 587) as server:
                server.starttls()

                server.login(sender_email, sender_password)

                server.send_message(message)

            print(idx, "Сообщение успешно отправлено!")
            update_hetzner_acc_date(sender_email, str(datetime.datetime.date(datetime.datetime.now())))
            update_hetzner_acc_addressee(sender_email, recipient_email)
            update_hetzner_acc_last_msg(sender_email, body)
        except Exception as e:
            print(f"not sent:\n", e)
    print("Всё отправлено!")
