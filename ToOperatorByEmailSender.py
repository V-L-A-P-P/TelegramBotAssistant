import smtplib
import os
import myFileWorker
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import logging
logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')


class ToOperatorByEmailSender:

    @staticmethod
    def send_to_operator(text, operator_data, photos):
        """Sends a message to the operator via email."""

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(operator_data["email"], operator_data["password"])
            msg = MIMEMultipart()
            body = MIMEText(text)
            msg.attach(body)
            msg["subject"] = "Уведомление"
            if photos is not None:
                for photo in photos:
                    basename = os.path.basename(photo['name'])
                    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
                    img = myFileWorker.load_image(photo['name'])
                    part_file.set_payload(img)
                    encoders.encode_base64(part_file)
                    msg.attach(part_file)

            server.sendmail(operator_data["email"], operator_data["email"], msg.as_string())
            print("Сообщение оператору через почту успешно доставлено")
        except Exception as _ex:
            print(f"Exception in sending to the operator via mail:\n{_ex}")
            logging.exception(f"Exception in sending to the operator via mail:\n{_ex}")