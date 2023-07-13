from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import ssl

from rest_framework import status
from rest_framework.response import Response

from config.settings import PROJECT_NAME_BY_DEFAULT


def get_name(user):
    name = f'Проект{user.rooms.count()}'
    all_names = user.rooms.values_list('name', flat=True)
    if name in all_names:
        new_number = max(
            all_names,
            key=lambda value: int(value[len(PROJECT_NAME_BY_DEFAULT) :]),
        )
        return f'Проект{int(new_number[len(PROJECT_NAME_BY_DEFAULT) :]) + 1}'
    else:
        return name


def send_pdf_file(subj, email, file, text=None):
    sender = 'dizi.izi.plan@gmail.com'  # Позднее убрать в .env
    password = 'tkttxsrnycqeijpw'  # Позднее убрать в .env
    context = ssl.create_default_context()

    # Позднее убрать в .env
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        try:
            server.login(sender, password)
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = email
            msg['Subject'] = subj
            if text:
                msg.attach(MIMEText(text))
            file_type, subtype = file.content_type.split('/')
            filename = file.name
            file = MIMEApplication(file.read(), subtype)
            file.add_header('content-disposition', 'attachment',
                            filename=filename)
            msg.attach(file)
            server.sendmail(sender, email, msg.as_string())
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
