#!/usr/bin/env python3
#define where the interpreter is located

import PySimpleGUI as sg
import numpy as np 
import cv2
import os
from pathlib import Path
from PIL import Image, ImageTk
import matplotlib.image as mpimg
def isImage(path) -> bool:
	supported_types = ['.png', '.jpg', '.jpeg', '.bmp']
	root, ext = os.path.splitext(path)

	return ext.lower() in supported_types

def get_img_data(filepath, maxsize=(400, 300), first=False):
	if not isImage(filepath):
		return None
	
	data = None
	try:
		image = Image.open(filepath)
		image.thumbnail(maxsize, Image.ANTIALIAS)
		data = ImageTk.PhotoImage(image)	
	
	except Exception as e:
		print(e)
		data = None
	
	finally:
		return data

def cv2_process_img_data(filepath, maxsize=(400, 300), values = None):
	#read image
	try:
		img = mpimg.imread(filepath)
		
		if values['_RGB_']:
			pass
			if values['_red_']:
				channel = img[:,:,0]
			elif values['_green_']:
				channel = img[:,:,1]
			elif values['_blue_']:
				channel = img[:,:,2]
		elif values['_HLS_']:
			HLS_img = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
			if values['_HLS_hue_']:
				channel = HLS_img[:,:,0]
			elif values['_HLS_light_']:
				channel = HLS_img[:,:,1]
			elif values['_HLS_sat_']:
				channel = HLS_img[:,:,2]

		elif values['_HSV_']:
			HSV_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
			if values['_HSV_hue_']:
				channel = HSV_img[:,:,0]
			elif values['_HSV_sat_']:
				channel = HSV_img[:,:,1]
			elif values['_HSV_val_']:
				channel = HSV_img[:,:,2]

		min_threshold = values['_MIN_THRES_']
		max_threshold = values['_MAX_THRES_']

		output_img = np.zeros_like(channel)

		output_img[(channel>=min_threshold) & (channel <= max_threshold)] = 1

		result = np.dstack((output_img, output_img, output_img)) * 255
		temp_img = Image.fromarray(result)
		temp_img.thumbnail(maxsize, Image.ANTIALIAS)
		return ImageTk.PhotoImage(image=temp_img)
	
	except Exception as e:
		print(e)
		print(output_img.shape)
		return None
	
if __name__ == "__main__":
	sg.change_look_and_feel('Black')	# Add a touch of color
	#
	# All the stuff inside your window.
	#
	channels = [[sg.Radio('RGB', 'Type', default=True, key='_RGB_', enable_events=True), 
				sg.Radio('HSV', 'Type', default=False, key='_HSV_', enable_events=True), 
				sg.Radio('HLS', 'Type', default=False, key='_HLS_', enable_events=True), 
				sg.Input(key='_filepath_', enable_events=True), sg.FileBrowse(enable_events=True)]]
	
	Color 	= [[sg.Radio('Red', 'Color', default=True, key='_red_', enable_events=True), 
				sg.Radio('Green', 'Color', default=False, key='_green_', enable_events=True), 
				sg.Radio('Blue', 'Color', default=False, key='_blue_', enable_events=True)]]
	
	HSV 	= [[sg.Radio('Hue', 'HSV', default=True, key='_HSV_hue_', enable_events=True),
				sg.Radio('Sat', 'HSV', default=False, key='_HSV_sat_', enable_events=True),
				sg.Radio('Val', 'HSV', default=False, key='_HSV_val_', enable_events=True)]]

	HLS 	= [[sg.Radio('Hue', 'HLS', default=True, key='_HLS_hue_', enable_events=True),
				sg.Radio('Light', 'HLS', default=False, key='_HLS_light_', enable_events=True),
				sg.Radio('Sat', 'HLS', default=False, key='_HLS_sat_', enable_events=True)]]

	minSlider = sg.Slider(range=(0,255), resolution = 1, enable_events = True,  orientation='h', key='_MIN_THRES_')
	maxSlider = sg.Slider(range=(0,255), resolution = 1, enable_events = True,  orientation='h', key='_MAX_THRES_')
	sliders = [[minSlider, maxSlider]]
	
	original = sg.Image(filename='D:/Picture/Capture.png')
	modified = sg.Image(filename='D:/Picture/Capture.png')

	layout 	= [[sg.Frame(layout=channels, title="Channels")], 
				[sg.Frame(layout=Color, title="Color"), sg.Frame(layout=HSV, title="HSV"), sg.Frame(layout=HLS, title="HLS")],
				[sg.Frame(layout=sliders, title=None)], 
				[original,
				modified]]
	#  
	# Create the Window
	# 
	window = sg.Window('Finding thresholds.', layout)
	#
	# Event Loop to process "events" and 
	# Get the "values" of the inputs
	#
	while True:
		event, values = window.read(timeout=2)
		if event == sg.TIMEOUT_KEY:
			continue
		#print(event, values)
		#print("{0} | {1} | {2}".format(values['_RGB_'], values['_HLS_'], values['_HSV_']))

		if values['_filepath_'] != '' and values['_filepath_'] is not None:
			filepath = values['_filepath_']
			image_data = get_img_data(filepath)
			processed_data = cv2_process_img_data(filepath, values=values)
			if image_data is not None:
				original.Update(data=image_data)
				if processed_data is not None:
					modified.Update(data=processed_data)
			else:
				print('Not an image')

		if event in (None, 'Cancel'):	# if user closes window or clicks cancel
			break

	window.close()