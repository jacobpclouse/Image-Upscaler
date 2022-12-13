# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify, Response
import os
from os import path
import datetime

import cv2
from cv2 import dnn_superres
from werkzeug.utils import secure_filename

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
pathToUploads = "./UPLOADS/"
pathToOutbound = "./OUTBOUND/"
pathToModels = './TrainedModels/'

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
def uppyBoi(inputFile,containingFolder,outboundFolder,currentExtension,modelPath):
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
    cv2.imwrite(f"{outboundFolder}upscaled.{currentExtension}", result)

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
            # getting input with send out method = send_out_choice in HTML form
            form_encryption = request.form.get("send_out_choice")

            print(f"User's Email: {form_email}")
            print(f"User's Phone: {form_phone}")
            print(f"User's Phone Carrier: {form_carrier}")
            print(f"Want Send out? : {form_encryption}")
            # "email" or "sms" or "none" /\

            secureTheFile = secure_filename(file.filename)
            extensionType = getExtension(secureTheFile)
            print(f"Current Extension: {extensionType}")

            # Filename below - Important for functions 
            filename = "Temp_Pic_Upload." + extensionType
            file.save(f"{pathToUploads}{filename}")
            uploaded_file = secureTheFile

            # UPSCALE!!!
            uppyBoi(filename,pathToUploads,pathToOutbound,extensionType,pathToModels)

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