#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np
import cv2
import json
import uuid
import os
import shutil

def main():
	r_coords = {}
	
	#image and geometry
	print("Select image")
	f_name = filedialog.askopenfilename(title="Please select an image:", filetypes=[("Image files", ".png .jpg .jpeg")])
	print("Set block transparency")
	geo_alpha = simpledialog.askinteger("Input", "Geometry alpha. 0 to 100, where 0 is fully transparent:")
	make_geo(f_name, geo_alpha)
	
	#render location and animation
	print("Input coordinates")
	r_coords = [
			simpledialog.askinteger("Input", "Input render coordinate X:"),
			simpledialog.askinteger("Input", "Input render coordinate Y:"),
			simpledialog.askinteger("Input", "Input render coordinate Z:")
		]
	make_animation(r_coords)
	
	#pack creation
	print("Making pack")
	make_pack(f_name)
	print("Done")

def make_geo(f_name, geo_alpha):
	#open image
	img = cv2.imread(f_name, cv2.IMREAD_UNCHANGED)
	height, width, channel = img.shape
	if channel < 4:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
	
	#create block model for each pixel
	pixel_geo = {
				"format_version": "1.12.0",
				"minecraft:geometry": [
					{
						"description": {
							"identifier": "geometry.pixel_projection",
							"texture_width": width,
							"texture_height": height,
							"visible_bounds_width": 5120,
							"visible_bounds_height": 5120,
							"visible_bounds_offset": [0, 0, 0]
						},
						"bones": [
							{
								"name": "static_pivot",
								"pivot": [0, 0, 0]
							},
							{
								"name": "static",
								"parent": "static_pivot",
								"pivot": [0, 0, 0]
							}
						]
					}
				]
			}
	for i in range(height):
		print("Processing pixels... " + str(int((i / height) * 100) + 1) + "%", end="\r")
		for j in range(width):
			new_bone = {
						"name": str(i) + "_" + str(j),
						"parent": "static",
						"pivot": [0, 0, 0],
						"cubes": [
							{
								"origin": [-8 + (j * 16), 0, -8 + (i * 16)],
								"size": [16, 16, 16],
								"inflate": -2,
								"uv": {
										"north": {"uv": [i, j], "uv_size": [1, 1]},
										"east": {"uv": [i, j], "uv_size": [1, 1]},
										"south": {"uv": [i, j], "uv_size": [1, 1]},
										"west": {"uv": [i, j], "uv_size": [1, 1]},
										"up": {"uv": [i, j], "uv_size": [1, 1]},
										"down": {"uv": [i, j], "uv_size": [1, 1]}
									}
							}
						]
					}
			
			pixel_geo["minecraft:geometry"][0]["bones"].append(new_bone)
	
	print("Processing pixels... 100%")
	print("Writing geometry file. This will take several seconds for large images")
	#write geometry file
	with open("pixel_projection/models/entity/pixel_projection.json", "w+") as f0:
		json.dump(pixel_geo, f0, separators=(',', ':'))
	
	print("Writing texture image")
	#set alpha of texture image
	alpha_mask = np.zeros_like(img)
	img_alpha = cv2.addWeighted(alpha_mask, 1.0, img, (geo_alpha / 100), 0)
	
	#write image to texture folder
	cv2.imwrite("pixel_projection/textures/pixel_projection.png", img_alpha)

def make_animation(r_coords):
	render_position = [
					"8 -(query.position(0)- " + str(r_coords[0]) + ")*16",
					"(" + str(r_coords[1]) + " -query.position(1))*16",
					"-8 +(query.position(2)- " + str(r_coords[2]) + ")*16"
				]
	with open("pixel_projection/animations/pixel_projection.json","r+") as f0:
		data=json.load(f0)
		data["animations"]["animation.pixel_projection"]["bones"]["static"]["position"] = render_position
	with open("pixel_projection/animations/pixel_projection.json","w+") as f1:
	    json.dump(data,f1,indent=2, separators=(',', ':'))

def make_pack(f_name):
	pack_name = os.path.basename(f_name).replace(".", "_") + "_pix_proj"
	manifest_name = os.path.basename(f_name).replace(".", "_") + ": Pixel_Projection_v0.0.1"
	
	#manifest
	with open("pixel_projection/manifest.json","r+") as f0:
		data=json.load(f0)
		data["header"]["name"]=manifest_name
		data["header"]["uuid"]=str(uuid.uuid4())
		data["modules"][0]["uuid"]=str(uuid.uuid4())
	with open("pixel_projection/manifest.json","w+") as f1:
	    json.dump(data,f1,indent=2, separators=(',', ':'))
	
	#zip from directory
	shutil.make_archive(pack_name, "zip", "pixel_projection")
	
	#rename zip to mcpack
	os.rename(pack_name + ".zip", pack_name + ".mcpack")

if __name__=="__main__": 
    main() 