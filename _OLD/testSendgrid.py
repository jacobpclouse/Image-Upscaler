from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify, Response
import os
from os import path
import datetime

import cv2
from cv2 import dnn_superres
from werkzeug.utils import secure_filename

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64





sourceEmail = "mp3converterandencryptor@gmail.com"
toEmail = os.environ.get("TO_THIS_EMAIL")
subjectOfEmail = "Using Email Source Envir"
contentOfEmail = "We appreciate you using our service! You will need to download the attachment and you should be all set."
nameOfAttachment = 'a'
desiredAttachmentName = 'Desired'
attachmentExtension = '.jpg'
pathToAttachment = '../backend/OUTBOUND/'




# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime



# --- Function to send email with attachment
def sendEmailFunc(sendFROMemail,sendTOemail,subjectLine,contentOfMessage,attachmentName,DesiredFilename,attachmentExtension,pathToAttachment):

    current_datetime = defang_datetime() #getting datetime for the name of the file

    # opening the file/decoding/saving it
    with open(f'{pathToAttachment}{attachmentName}{attachmentExtension}', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()    

    # saving api key in the environment
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    from_email = Email(f"{sendFROMemail}")  # Change to your verified sender
    to_email = To(f"{sendTOemail}")  # Change to your recipient
    subject = f"{subjectLine}!"
    
    html_content=Content('text/html', f'<h1>, Thank you for using JPC Image Upscaler!</h1><p>{contentOfMessage}</p><p><b>Date Sent: {current_datetime}</b></p>')
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(f'{current_datetime}__{DesiredFilename}'),
        FileType(attachmentExtension), 
        Disposition('attachment')
    )

    mail = Mail(from_email, to_email, subject, html_content)
    mail.attachment = attachedFile  # tacking on the attachment

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


# --- 
sendEmailFunc(sourceEmail,toEmail,subjectOfEmail,contentOfEmail,nameOfAttachment,desiredAttachmentName,attachmentExtension,pathToAttachment)