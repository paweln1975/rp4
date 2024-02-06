# Raspberry PI 4
Raspberry PI 4 Computer edu python programs

## blink led
One LED blinking module

## tact led
LED enabled after pressing a tact button

## tact three leds
Three LEDs blinking alternately. Press the button longer to exit.

## pri read
Reading input from PIR HC-SR501 passive infrared sensor. Exit after pressing the tact button.

## send email
Sends an e-mail to g-mail.com account.

## gradient led
Changes the light intensity of the LED by changing the ratio of the duration of the high to low signal at a set frequency
 
## take photo
Takes a photo and a movie from a camera

# Final project

## move detector
Final project with move detection, photo, disk storage and mail sending

The first Python program:
- Monitor the PIR sensor. When some movement is detected and the movement is
detected for 3 consecutive seconds. To do that an infinite while loop is created.
The last PIR sensor state is kept into a variable and compared it with the
current state. As an additional visual indicator is also powered on an LED when the
PIR sensor detects some movement.
- At this point, a photo is taken and saved to the /home/pi/camera folder. A function
“take_photo()” is to take a photo and save it. The file name starts with “img_” and then has
a timestamp to make it unique. To get a timestamp the function “time.time()” is called.
- Then, the name of the photo (complete path + file name) is added into a log file named
photo_logs.txt (the append mode with “a” when opening the file). During the setup of
the program, check if folders camera and folder with current date exist, if not folders are created.
- Then,an email is saved to an e-mail with the photo as an attachment. Setup email (with
Yagmail) is in the setup section of the program. 
- Also, as an additional feature, more than one photo (+ write to log file and send email)
is created every 60 seconds. For that it is kept in a “last_time_photo_taken” variable with the time.

## server
Simple Flask server hosting a page where switching on a button is possible
With additional end points it is possible to browse photos taken by the move detector

Flask application with a default route “/” just returning simple page with buttons to operate on leds.
Another route “/movement/<date>” - when the function for this URL is called, the log file is read (photo_logs.txt 
created by the other Python program, using the read mode “r”). The table with all photos taken are rendered
using an img tag to render images in the browser. 

## utils
Common methods
