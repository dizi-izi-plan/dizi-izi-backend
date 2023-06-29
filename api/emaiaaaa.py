import smtplib
import ssl
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path


def send_pdf_file(text=None):
    sender = 'dizi.izi.plan@gmail.com'
    receiver = '3antetsuken@mail.ru'
    password = 'tkttxsrnycqeijpw'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender, password)
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'План размещения мебели'
            if text:
                msg.attach(MIMEText(text))
            file = Path(__file__).parents[1].joinpath('test_storage/test_user/test_pdf_1.pdf')
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")
            filename = file.name
            with open(file, 'rb') as f:
                file = MIMEApplication(f.read(), subtype)
            file.add_header('content-disposition', 'attachment',
                            filename=filename)
            msg.attach(file)
            server.sendmail(sender, receiver, msg.as_string())
            return
        except Exception:
            return 'Не удалось отправить план на почту'


def main():
    text = 'Привет'
    print(send_pdf_file(text=text))


if __name__ == "__main__":
    main()
