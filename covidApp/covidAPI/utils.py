from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
from background_task import background
import base64
from datetime import datetime
# from .covidApp.celery import *

@background(schedule=60)
def sendCovidData(toEmail, image):
    print("Send Covid Called")
    subject = 'COVID19 API Bar Chart dated ' + datetime.strftime(datetime.now(), '%d-%m-%Y')
    body = '<strong>Please Find below bar chart. Bar chart is being created using https://corona-api.com API.</strong>'
    fileName = 'covid19 ' + datetime.strftime(datetime.now(), '%d-%m-%Y') + '.png'
    sendEmail(toEmail, image, subject, body,fileName)


def sendEmail(toEmail, image, subject, body, fileName):
    send_grid = SendGridAPIClient(api_key="")
    message = None

    message = Mail(
        from_email='mohitmanglani2906@gmail.com',
        to_emails=toEmail,
        subject=subject,
        html_content=body)

    # encoded = base64.b64encode(image).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(image)
    attachment.file_type = FileType('image/png')
    attachment.file_name = FileName(fileName)
    message.attachment = attachment
    response = send_grid.send(message)

    print(response.status_code)