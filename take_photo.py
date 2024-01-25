from picamera import PiCamera
import time

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1280, 720)
time.sleep(2)

file_name = '/home/pi/Pictures/image.jpg'
camera.capture(file_name)

print("Picture done")

file_name = '/home/pi/Pictures/video.h264'
camera.start_recording(file_name)
camera.wait_recording(5)
camera.stop_recording()

print("Video done")