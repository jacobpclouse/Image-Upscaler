# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# flask / general imports
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify, Response
import os
from os import path
import datetime

# upscaling imports
import cv2
from cv2 import dnn_superres
from werkzeug.utils import secure_filename

# email / sendgrid imports
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64

# colorize imports
# import numpy as np
# import argparse
from colorizers import *
import matplotlib.pyplot as plt


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
upscaledFilename = 'upscaled.'
desiredEmailFilename = 'JPC_Image_Upscaled.'

pathToUploads = "./UPLOADS/"
pathToOutbound = "./OUTBOUND/"
pathToModels = './TrainedModels/'
# email vars
sourceEmail = "mp3converterandencryptor@gmail.com"
subjectOfEmail = "Here is Your Upscaled Image"
contentOfEmail = "We appreciate you using our service! You will need to download the attachment and you should be all set."
# colorize vars


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print("Dedicated to Mary Ann Clouse, Carmen Liberticci, Peter Clouse, and Anna Libertucci")


# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime


# --- Function used to find ending type for file AND checking to make sure that it is an allowed type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Function used to find ending type for file only (for creating temp pic in UPLOADS)
def getExtension(inputFile):
    return '.' and inputFile.rsplit(".",1)[1].lower()


# --- Function used to upscale images
def uppyBoi(inputFile,containingFolder,outboundFolder,currentExtension,modelPath,upscaledFilename):
    print(f"Opening: {inputFile}")
    # Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()

    # Read image
    image = cv2.imread(f'{containingFolder}{inputFile}')

    # Read the desired model
    path = f"{modelPath}EDSR_x3.pb"
    sr.readModel(path)

    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel("edsr", 3)

    # Upscale the image
    result = sr.upsample(image)

    # Save the image
    cv2.imwrite(f"{outboundFolder}{upscaledFilename}{currentExtension}", result)


# --- Function to send email with attachment
def sendEmailFunc(sendFROMemail,sendTOemail,subjectLine,contentOfMessage,attachmentName,DesiredFilename,attachmentExtension,pathToAttachment):

    current_datetime = defang_datetime() #getting datetime for the name of the file

    # opening the file/decoding/saving it
    with open(f'{pathToAttachment}{attachmentName}{attachmentExtension}', 'rb') as f:
    # with open(f'./a.jpg', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()    

    # saving api key in the environment
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    from_email = Email(f"{sendFROMemail}")  # Change to your verified sender
    to_email = To(f"{sendTOemail}")  # Change to your recipient
    # subject = f"{subjectLine}!"
    # subject = "Here is your Upscaled Image!"
    
    html_content=Content('text/html', f'<h1>Thank you for using JPC Image Upscaler!</h1><p>{contentOfMessage}</p><p><b>Date Sent: {current_datetime}</b></p>')
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(f'{current_datetime}__{DesiredFilename}'),
        #FileName(f'{current_datetime}__upscaled'),
        FileType(attachmentExtension), 
        Disposition('attachment')
    )

    mail = Mail(from_email, to_email, subjectLine, html_content)
    mail.attachment = attachedFile  # tacking on the attachment

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


# --- Function to colorize image
# NOTE: this was made possible due to the wonderful colorizing library at: https://github.com/richzhang/colorization
def colorizeImage(origImage,pathToImg,extensionType):
    img_path = f"{pathToImg}{origImage}{extensionType}"
    print(f"Location of Target Image: {img_path}")

    # wantToUseGPU = False

    # load colorizers
    colorizer_eccv16 = eccv16(pretrained=True).eval()
    colorizer_siggraph17 = siggraph17(pretrained=True).eval()

    # default size to process images is 256x256
    # grab L channel in both original ("orig") and resized ("rs") resolutions
    img = load_img(img_path)
    (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))

    # colorizer outputs 256x256 ab map
    # resize and concatenate to original L channel
    img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
    out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
    out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

    # # plt.imsave(f'{origImage}_eccv16.{extensionType}', out_img_eccv16)
    # # plt.imsave(f'{origImage}_siggraph17.{extensionType}', out_img_siggraph17)
    # colorizedImageName1 = f'colorized_{origImage}1.{extensionType}'
    # colorizedImageName2 = f'colorized_{origImage}2.{extensionType}'
    plt.imsave(f"{pathToOutbound}colorizedImage1.png", out_img_eccv16)
    plt.imsave(f"{pathToOutbound}colorizedImage2.png", out_img_siggraph17)




# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Route to upscale
@app.route('/',methods=['GET', 'POST'])
@app.route('/upscale',methods=['GET', 'POST'])
def upscaleFunc():

    myLogo()

    uploaded_file = ''
    title = "Upload Image to Upscale"

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # GRABBING FORM INFO -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

            # getting input with email = userEmail in HTML form
            form_email = request.form.get("userEmail")
            # getting input with email = userEmail in HTML form
            form_phone = request.form.get("userPhone")
            # getting input with carrier = userCarrier in HTML form
            form_carrier = request.form.get("userCarrier")
            # getting input with colorize choice = colorized_choice in HTML form
            form_colorized_option = request.form.get("colorized_choice")
            # getting input with send out method = send_out_choice in HTML form
            form_send_out_option = request.form.get("send_out_choice")

            print(f"User's Email: {form_email}")
            print(f"User's Phone: {form_phone}")
            print(f"User's Phone Carrier: {form_carrier}")
            print(f"Want Colorized? : {form_colorized_option}") # Binary yes or no
            print(f"Want Send out? : {form_send_out_option}")
            # "email" or "sms" or "none" /\

            secureTheFile = secure_filename(file.filename)
            extensionType = getExtension(secureTheFile)
            print(f"Current Extension: {extensionType}")

            # Filename below - Important for functions 
            filename = "Temp_Pic_Upload." + extensionType
            file.save(f"{pathToUploads}{filename}")
            uploaded_file = secureTheFile

            # UPSCALE!!! - Careful, if image too big then it crashes!
            uppyBoi(filename,pathToUploads,pathToOutbound,extensionType,pathToModels,upscaledFilename)

            # COLORIZE?? - Checks to see if option set, if yes then colorizes and overwrites upscaled
            if form_colorized_option == 'yes':
                print('Colorizing!')


            # checking to see if we should send out email of file
            if form_send_out_option == 'email':
                print("Sending email")
                # sendEmailFunc(sendFROMemail,sendTOemail,subjectLine,contentOfMessage,attachmentName,DesiredFilename,attachmentExtension,pathToAttachment):
                sendEmailFunc(sourceEmail,form_email,subjectOfEmail,contentOfEmail,upscaledFilename,desiredEmailFilename,extensionType,pathToOutbound)
            
            if form_send_out_option == 'sms':
                print("Sending sms")




    return render_template('upscale.html',html_title = title)


# Route to colorize
@app.route('/colorize',methods=['GET', 'POST'])
def colorizeFunc():
    uploaded_file = ''
    title = "Upload Image to Colorize"
    
    return render_template('colorize.html',html_title = title)




# ----===--------===--------===--------===----
# main statement - used to set dev mode
# ----===--------===--------===--------===----
if __name__ == '__main__':
    app.run(debug=True)