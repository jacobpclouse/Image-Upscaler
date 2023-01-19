# Full Stack Image Upscaler
- __Upload any image and watch as it is upscaled with Python__
- __Lets you Colorize black and white images__
(will create app backend 1st then replace with react front end)

NOTE: Remember to enter 'source sendgrid.env' before running app.py (for sendgrid)

## Technologies Used: 
- Python/Flask (Backend)
- React/JavaScript (Frontend)
- Bootstrap
- Fontawesome (Icons)
- Sendgrid API (sending pictures via emails)
- MMS eText (sending pictures via SMS)


## Objectives / Goals:
- [x] Able to upload image (specify quality?)
- [x] Backend recieves it and upscales it
- ~~[ ] User redirected to display page~~
- [x] User can view image and send via email or MMS (NOTE: attachments blocked on phone, size too big?)
- [x] Route to Colorize B&W Image Page
- [x] Route to Resize Image Page


## Resources: 
- ** OpenCV image upscaling: https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066
- Colorizing Images with python:
- * Geeks for geeks colorizing: https://www.geeksforgeeks.org/black-and-white-image-colorization-with-opencv-and-deep-learning/
- * pyimagesearch: https://pyimagesearch.com/2019/02/25/black-and-white-image-colorization-with-opencv-and-deep-learning/
- Make pretty CSS: https://neumorphism.io/#e0e0e0
- __How to connect Flask to ReactJs__: https://dev.to/nagatodev/how-to-connect-flask-to-reactjs-1k8i
- Use sound library: https://www.npmjs.com/package/use-sound
- Resize images with opencv:
- * Tutorialkart: https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
- * Geeks for geeks: https://www.geeksforgeeks.org/image-resizing-using-opencv-python/
- sendgrid: free email templates and using email templates with the api:
- * https://sendgrid.com/blog/create-html-emails/
- * https://sendgrid.com/free-templates/
- Sendgrid API keys: https://docs.sendgrid.com/ui/account-and-settings/api-keys
- Gmail App Passwords (For Sendgrid): https://wpmailsmtp.com/gmail-less-secure-apps/#Option_2_Use_an_App_Password
- Gmail Docs: App passwords: https://support.google.com/accounts/answer/185833?hl=en
- Sendgrid 403 Error: https://stackoverflow.com/questions/59739152/getting-a-strange-error-403-forbidden-for-accessing-an-api-through-python
- Colorization github script by Richard Zhang, Phillip Isola, Alexei A. Efros. : 
- * https://github.com/richzhang/colorization/
- * https://github.com/richzhang/colorization/tree/caffe
- Send text messages for free with sms gateways: https://www.youtube.com/watch?v=4-ysecoraKo
- Python Image Resize With Pillow and OpenCV: https://cloudinary.com/guides/bulk-image-resize/python-image-resize-with-pillow-and-opencv
