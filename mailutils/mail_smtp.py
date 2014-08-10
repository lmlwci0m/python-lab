import os
from utils import encutils

__author__ = 'roberto'

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from utils.fileutils import readfile, read_binary_file


HEADER_NAME_CONTENT_DISPOSITION = 'Content-Disposition'
HEADER_VALUE_ATTACHMENT = 'attachment'

MIME_TYPE_TEXTPLAIN = "text/plain"


def add_text_file_attachment(location, filename):
    content = readfile(os.path.join(location, filename))
    attachment = MIMEText(content, MIME_TYPE_TEXTPLAIN)
    attachment.add_header(HEADER_NAME_CONTENT_DISPOSITION, HEADER_VALUE_ATTACHMENT, filename=filename)
    return attachment


def add_bin_file_attachment(location, filename, application_type):
    content = read_binary_file(os.path.join(location, filename))
    attachment = MIMEApplication(content, application_type)
    attachment.add_header(HEADER_NAME_CONTENT_DISPOSITION, HEADER_VALUE_ATTACHMENT, filename=filename)
    return attachment


def define_multipart_message(sender, recipient, subject, body):

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(add_text_file_attachment("directorypath", "text_file.txt"))

    msg.attach(add_bin_file_attachment("directorypath", "zip_file.zip", "zip"))

    part = MIMEText('text', "plain", encutils.DEFAULT_FILE_ENCODING)
    part.set_payload(body.encode(encutils.DEFAULT_FILE_ENCODING))  # !!! IMPORTANT FOR SENDING UTF-8 text
    msg.attach(part)

    return msg


def send_mail(msg, recipient, host, port, username, password):

    session = smtplib.SMTP(host, port)
    print(session.ehlo())
    print(session.starttls())
    print(session.ehlo)
    print(session.login(username, password))
    print(session.sendmail(username, recipient, msg))
    print(session.quit())


def main():

    sender = 'abc@xyz.com'
    recipient = 'abc@xyz.com'
    subject = "Test subject"
    body = "Test body"

    message = define_multipart_message(sender, recipient, subject, body)

    send_mail(message.as_string(), recipient)


if __name__ == '__main__':
    main()
