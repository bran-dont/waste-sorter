# python -m pip install --upgrade pip

# CHOOSE ONE
# pip install lobe[all]
# pip install lobe[tf]
# pip install lobe[tflite]
# pip install lobe[onnx]

# pip install opencv-python

#import Pi GPIO library button class
from gpiozero import Button, LED, PWMLED
import cv2
from time import sleep

from lobe import ImageModel

model = ImageModel.load('./waste-sorter-TFLite')

#Create input, output, and camera objects
button = Button(2)

yellow_led = LED(17) #garbage
blue_led = LED(27) #recycle
green_led = LED(22) #compost
red_led1 = LED(5) #garbage capacity
red_led2 = LED(6) #recycle capacity
red_led3 = LED(23) #compost capacity
white_led = PWMLED(24) #Status light and retake photo

#camera = PiCamera()

# Take Photo
def take_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('image.jpg', frame)
    else:
        print("Error capturing frame")
    cap.release()

# Identify prediction and turn on appropriate LED
def led_select(label):
    # print(label)
    if label == "cardboard":
        yellow_led.on()
        print("cardboard")
        sleep(5)

    elif label == "glass":
        yellow_led.on()
        print("glass")
        sleep(5)
        
    elif label == "metal":
        yellow_led.on()
        print("metal")
        sleep(5)

    elif label == "plastic":
        yellow_led.on()
        print("metal")
        sleep(5)

    elif label == "paper":
        yellow_led.on()
        print("paper")
        sleep(5)

    elif label == "compost":
        blue_led.on()
        print("compost")
        sleep(5)

    elif label == "not trash":
        print("not trash")
        white_led.on()

    else:
        yellow_led.off()
        blue_led.off()
        green_led.off()

#take_photo()
#result = model.predict_from_file('./image.jpg')
#print(result.prediction)

# Main Function
while True:
    if button.is_pressed:
        take_photo()
        # Run photo through Lobe TF model
        result = model.predict_from_file('/home/pi/Pictures/image.jpg')
        # --> Change image path
        led_select(result.prediction)
    else:
        # Pulse status light
        white_led.pulse(2,1)
    sleep(1)