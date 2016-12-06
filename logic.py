#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc

#鍵の番号
key_list = ["0114B405B6116944","01010114DD15E70D"]

#終了の際の処理
def exit_handler(signal, frame):
	print("\nExit")
	GPIO.cleanup()
	sys.exit(0)

#基本的なセッティング
signal.signal(signal.SIGINT, exit_handler)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
toggle = True

#タッチされたとき
def touched(tag):
    #変数のグローバル化
	global toggle
	global key_list
	#idの照合
	tag_id = tag.identifier.encode("hex").upper()
	print(tag_id)
	if tag_id not in key_list:
	    #データが正しいidと異なっていた場合
		print("No matching Key")
		return

	servo = GPIO.PWM(12, 50)
	if toggle:
        #鍵の解錠
		servo.start(7.7)
		print("Open")
		time.sleep(0.5)
		toggle = False
	else:
        #鍵の施錠
		servo.start(2.5)
		print("Close")
		time.sleep(0.5)
		toggle = True
	servo.stop()

clf = nfc.ContactlessFrontend('usb')

print("setting OK.")

#繰り返し
while True:
	clf.connect(rdwr={'on-connect': touched})
	time.sleep(3)
	print("relese")
