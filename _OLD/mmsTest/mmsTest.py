import email, smtplib, ssl
from providers import PROVIDERS

# used for MMS
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os.path import basename




# used to construct text message and send it out via email gateway (from guide: https://www.alfredosequeida.com/blog/how-to-send-text-messages-for-free-using-python-use-python-to-send-text-messages-via-email/)
def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "JPC Upscaler Results",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"
    print(email_message)

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

# MAIN SMS SENDER - NEED TO USE THIS ONE 
def actualSendOutSMS(number,message,carrier,senderEmail,applicationKey,filepath,mimeMainBoi,mimeSubBoi):
    newTel = ''
    for x in number:
        # stripping out the dashes in order to send sms
        if x != '-':
            newTel = newTel + x

    number = f"{newTel}"

    sender_credentials = (f"{senderEmail}", f"{applicationKey}")
    print(f"Sending Text message to to: {number}, {message}, {carrier}, {sender_credentials}")
    # send_sms_via_email(number, message, provider, sender_credentials)
    send_mms_via_email(number,message,filepath,mimeMainBoi,mimeSubBoi,carrier,sender_credentials)



''' MMS SENDING '''

def send_mms_via_email(
    number: str,
    message: str,
    file_path: str,
    mime_maintype: str,
    mime_subtype: str,
    provider: str,
    sender_email,
    email_password,
    subject: str = "JPC Upscaler Results",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
# ---

    newTel = ''
    for x in number:
        # stripping out the dashes in order to send sms
        if x != '-':
            newTel = newTel + x

    number = f"{newTel}"
    print(f"Sending Text message to to: {number}, {message}, {provider}")
    
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message=MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email

    email_message.attach(MIMEText(message, "plain"))

    with open(file_path, "rb") as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={basename(file_path)}",
        )

        email_message.attach(part)

    text = email_message.as_string()

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, text)



####
myNumber = '----'
myMMSMessage = 'Here are the files you requested: '
theFilepath = './b.png'
mineMain = "application"
mineSub= 'zip'
myCarrier = 'Verizon'
mmsSenderEmail = "mp3converterandencryptor@gmail.com"
mmsAppKey = ""



    # send_mms_via_email(number,message,filepath,mimeMainBoi,mimeSubBoi,carrier,sender_credentials)
send_mms_via_email(myNumber,myMMSMessage,theFilepath,mineMain,mineSub,myCarrier,mmsSenderEmail,mmsAppKey)


'''
def send_mms_via_email(
    number: str,
    message: str,
    file_path: str,
    mime_maintype: str,
    mime_subtype: str,
    provider: str,
    senderEmail,
    applicationKey,
    # sender_credentials: tuple,
    subject: str = "JPC Upscaler Results",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
'''