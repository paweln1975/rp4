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

## server
Simple Flask server hosting a page where switching on a button is possible
With additional end points it is possible to browse photos taken by the move detector

## take photo
Takes a photo and a movie from a camera

## move detector
Final project with move detection, photo, disk storage and mail sending

The first Python program:
- Monitor the PIR sensor. When some movement is detected, make sure the movement is
detected for 3 consecutive seconds. To do that you can create an infinite while loop.
You’ll have to keep the last PIR sensor state into a variable and compare it with the
current state. As an additional visual indicator you can also power on an LED when the
PIR sensor detects some movement.
- At this point, take a photo and save it to the /home/pi/camera folder. Create a function
“take_photo()” to take a photo and save it. The file name starts with “img_” and then has
a timestamp to make it unique. To get a timestamp you can call the function
“time.time()”. Then call this function in the appropriate place in your main while loop.
- Then, add the name of the photo (complete path + file name) into a log file named
photo_logs.txt (use the append mode with “a” when opening the file). During the setup of
the program, check if this file exists and remove it so it doesn’t contain data from
previous program runs.
- Then, send an email to yourself with the photo as an attachment. Setup email (with
Yagmail) in the setup section of the program. Create a “send_email_with_photo” function
to send the photo which was just taken by email.
- Also, as an additional feature, make sure you don’t take more than one photo (+ write to
log file and send email) every 60 seconds. For that you can also keep a
“last_time_photo_taken” variable with the time.
The second Python program will:
- Run a Flask application with a default route “/” just returning simple
- Add another route “/movement/<date>”
- When the function for this URL is called, read the log file (photo_logs.txt created by the
other Python program, using the read mode “r”). Count the number of lines in the file,
and get the last photo path (last line). You can use a “for line in f” loop to go through all
the lines in the file.
- Then, compare the line count with the previous line count (= the last time you called this
URL). For that you’ll need to use a global variable to keep track of the count.
- Return a string telling how many new photos have been taken since the last time the
URL was called, + give the path to the photo file.
- And finally, use an img tag inside the string you return to print the
image in the browser. To make things work you’ll also have to change the line “app =
Flask(__name__)” to become “app = Flask(__name__,
static_url_path=CAMERA_FOLDER_PATH, static_folder=CAMERA_FOLDER_PATH)”,
where CAMERA_FOLDER_PATH is "/home/pi/camera".

## utils
Common methods
