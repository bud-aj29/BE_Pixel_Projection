#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import numpy as np
import cv2
import json
import uuid
import os
import shutil

class PixelProjectionApp:
	def __init__(self):
		# build ui
		tk1 = tk.Tk()
		icon_image = b'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NzQtOWI3Yy00MjIyMjllMTQxOTQiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6YmNlMjlmNGUtMGNmNS00MjE1LTg1MDUtNjU2MzgyOWQ3MmQ3IgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6OGRkNjAwMWUtZjIzMy00ZGQ1LTk0MTEtOGQxYjI3MDc3MzI0IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE2NzIxMDU5MDgxNTA3MDgiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4yNCIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo0MzE2MjBkMS0zNmEzLTQ4NzMtYmU1Yi1kZTVkOGUyNjk5ODQiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjItMTItMjdUMDc6NTA6MjkiLz4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6OGYyNWI3MTEtOWY1MC00ZDJiLTgxNjQtOThlZWNjMmM5YTQzIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDIyLTEyLTI3VDEwOjM0OjE5Ii8+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmU5ODU0NDNiLTRmNGEtNGM1NC1iNjljLTQ3OGJhZGMyYzBmOCIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyMi0xMi0yN1QxMDo1MTo0OCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz54crxtAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5gwbATMwnVFQCwAAAFdJREFUOMulk1EKwDAIQ3P/S7/9DqblpRMKkpREW02+QebY8OoSluR1lAgiX0VOLqoSUyoDx+R2qmTFkO2sOZdzgHWNecTI/iuBimvnHwvyZx+aH7rfiwfWfD7CfJp2fwAAAABJRU5ErkJggg=='
		tk1.iconphoto(True, tk.PhotoImage(data=icon_image))
		tk1.geometry("308x448")
		tk1.title("Pixel_Projection")
		frame1 = ttk.Frame(tk1)
		frame1.configure(height=440, width=300)
		label1 = ttk.Label(frame1)
		label1.configure(font="TkDefaultFont", text='Select image')
		label1.grid(column=0, columnspan=3, padx=2, row=0, sticky="w")
		entry1 = ttk.Entry(frame1)
		self.f_name = tk.StringVar()
		entry1.configure(textvariable=self.f_name, width=33)
		entry1.grid(column=0, columnspan=2, padx=4, row=1, sticky="w")
		button1 = ttk.Button(frame1)
		button1.configure(text='Browse')
		button1.grid(column=2, row=1, sticky="w")
		button1.configure(command=self.get_filename)
		separator1 = ttk.Separator(frame1)
		separator1.configure(orient="horizontal")
		separator1.grid(
			column=0,
			columnspan=3,
			padx=4,
			pady=4,
			row=2,
			sticky="ew")
		label2 = ttk.Label(frame1)
		label2.configure(
			text='Block transparency\n(0 to 100, where 100 is fully opaque)')
		label2.grid(column=0, columnspan=3, padx=2, row=3, sticky="w")
		scale1 = tk.Scale(frame1)
		self.geo_alpha = tk.IntVar()
		scale1.configure(
			from_=0,
			orient="horizontal",
			to=100,
			variable=self.geo_alpha)
		scale1.grid(column=0, columnspan=2, padx=4, row=4, sticky="ew")
		separator2 = ttk.Separator(frame1)
		separator2.configure(orient="horizontal")
		separator2.grid(
			column=0,
			columnspan=3,
			padx=4,
			pady=4,
			row=5,
			sticky="ew")
		label3 = ttk.Label(frame1)
		label3.configure(text='Threshold (skip pixels with alpha below this)')
		label3.grid(column=0, columnspan=3, padx=2, row=6, sticky="w")
		scale2 = tk.Scale(frame1)
		self.alpha_threshold = tk.IntVar()
		scale2.configure(
			from_=0,
			orient="horizontal",
			to=100,
			variable=self.alpha_threshold)
		scale2.grid(column=0, columnspan=2, padx=4, row=7, sticky="ew")
		separator3 = ttk.Separator(frame1)
		separator3.configure(orient="horizontal")
		separator3.grid(
			column=0,
			columnspan=3,
			padx=4,
			pady=4,
			row=8,
			sticky="ew")
		label4 = ttk.Label(frame1)
		label4.configure(
			justify="left",
			state="normal",
			text='Render coordinates')
		label4.grid(column=0, columnspan=3, padx=2, row=9, sticky="w")
		label5 = ttk.Label(frame1)
		label5.configure(text='x:')
		label5.grid(column=0, padx=2, row=10, sticky="w")
		entry2 = ttk.Entry(frame1)
		self.r_coords_x = tk.IntVar(value=0)
		entry2.configure(textvariable=self.r_coords_x, width=5)
		_text_ = '0'
		entry2.delete("0", "end")
		entry2.insert("0", _text_)
		entry2.grid(column=0, padx=20, row=10, sticky="w")
		label6 = ttk.Label(frame1)
		label6.configure(text='y:')
		label6.grid(column=0, padx=6, row=10, sticky="e")
		entry3 = ttk.Entry(frame1)
		self.r_coords_y = tk.IntVar(value=-60)
		entry3.configure(textvariable=self.r_coords_y, width=5)
		_text_ = '-60'
		entry3.delete("0", "end")
		entry3.insert("0", _text_)
		entry3.grid(column=1, row=10, sticky="w")
		label7 = ttk.Label(frame1)
		label7.configure(text='z:')
		label7.grid(column=2, padx=2, row=10, sticky="w")
		entry4 = ttk.Entry(frame1)
		self.r_coords_z = tk.IntVar(value=0)
		entry4.configure(textvariable=self.r_coords_z, width=5)
		_text_ = '0'
		entry4.delete("0", "end")
		entry4.insert("0", _text_)
		entry4.grid(column=2, padx=20, row=10, sticky="w")
		separator4 = ttk.Separator(frame1)
		separator4.configure(orient="horizontal")
		separator4.grid(
			column=0,
			columnspan=3,
			padx=4,
			pady=4,
			row=11,
			sticky="ew")
		label8 = ttk.Label(frame1)
		label8.configure(text='Alignment')
		label8.grid(column=0, columnspan=3, padx=2, row=12, sticky="w")
		radiobutton1 = ttk.Radiobutton(frame1)
		self.align_dir = tk.IntVar(value=0)
		radiobutton1.configure(
			text='horizontal',
			value=0,
			variable=self.align_dir)
		radiobutton1.grid(column=0, padx=4, row=13)
		radiobutton2 = ttk.Radiobutton(frame1)
		radiobutton2.configure(
			text='vertical',
			value=1,
			variable=self.align_dir)
		radiobutton2.grid(column=1, padx=4, row=13)
		separator5 = ttk.Separator(frame1)
		separator5.configure(orient="horizontal")
		separator5.grid(
			column=0,
			columnspan=3,
			padx=4,
			pady=4,
			row=14,
			sticky="ew")
		button2 = ttk.Button(frame1)
		button2.configure(text='Make pack')
		button2.grid(column=2, row=15, sticky="w")
		button2.configure(command=self.make_pack)
		self.text1 = tk.Text(frame1)
		self.text1.configure(height=5, state="normal", width=33, wrap="word")
		self.text1.grid(column=0, columnspan=3, padx=4, pady=4, row=16, sticky="ew")
		frame1.grid(column=0, padx=4, pady=4, row=0)
		frame1.grid_propagate(0)
		tk1.grid_propagate(0)
		
		#defaults
		self.geo_alpha.set(70)
		self.alpha_threshold.set(20)
		self.align_dir.set(0)

		# Main widget
		self.mainwindow = tk1
	
	def run(self):
		self.mainwindow.mainloop()
	
	def print_to_text(self, p_text):
		self.text1.insert("end", p_text)
		self.text1.see("end")
		self.text1.update_idletasks()
	
	def get_filename(self):
		self.f_name.set(filedialog.askopenfilename(title="Please select an image:", filetypes=[("Image files", ".png .jpg .jpeg")]))
	
	def make_pack(self):
		if not self.f_name.get():
			messagebox.showerror("Error", "No image was selected")
			return
		
		self.make_geo()
		self.make_animation()
		
		#print("Making pack")
		self.print_to_text("\n" + "Making pack" + "\n")
		
		pack_name = os.path.basename(self.f_name.get()).replace(".", "_") + "_pix_proj"
		manifest_name = os.path.basename(self.f_name.get()).replace(".", "_") + ": Pixel_Projection"
		
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
		
		#print("Done")
		self.print_to_text("\n" + "All finished." + "\n")
	
	def make_geo(self):
		#open image
		img = cv2.imread(self.f_name.get(), cv2.IMREAD_UNCHANGED)
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
		#horizontal
		if self.align_dir.get() == 0:
			for i in range(height):
				#print("Processing pixels... " + str(int((i / height) * 100) + 1) + "%", end="\r")
				self.print_to_text("\n" + "Processing pixels... " + str(int((i / height) * 100) + 1) + "%")
				
				for j in range(width):
					#exclude transparent pixels
					if img[i][j][3] > (self.alpha_threshold.get() * (255/100)):
						new_bone = {
									"name": str(i) + "_" + str(j),
									"parent": "static",
									"pivot": [0, 0, 0],
									"cubes": [
										{
											"origin": [-8 + (i * 16), 0, -8 + (j * 16)],
											"size": [16, 16, 16],
											"inflate": -2,
											"uv": {
													"north": {"uv": [j, i], "uv_size": [1, 1]},
													"east": {"uv": [j, i], "uv_size": [1, 1]},
													"south": {"uv": [j, i], "uv_size": [1, 1]},
													"west": {"uv": [j, i], "uv_size": [1, 1]},
													"up": {"uv": [j, i], "uv_size": [1, 1]},
													"down": {"uv": [j, i], "uv_size": [1, 1]}
												}
										}
									]
								}
						
						pixel_geo["minecraft:geometry"][0]["bones"].append(new_bone)
		#vertical
		else:
			for i in range(height):
				#print("Processing pixels... " + str(int((i / height) * 100) + 1) + "%", end="\r")
				self.print_to_text("\n" + "Processing pixels... " + str(int((i / height) * 100) + 1) + "%")
				
				i_rev = (height - 1) - i
				for j in range(width):
					#exclude transparent pixels
					if img[i][j][3] > (self.alpha_threshold.get() * (255/100)):
						new_bone = {
									"name": str(i) + "_" + str(j),
									"parent": "static",
									"pivot": [0, 0, 0],
									"cubes": [
										{
											"origin": [-8, (i * 16), -8 + (j * 16)],
											"size": [16, 16, 16],
											"inflate": -2,
											"uv": {
													"north": {"uv": [j, i_rev], "uv_size": [1, 1]},
													"east": {"uv": [j, i_rev], "uv_size": [1, 1]},
													"south": {"uv": [j, i_rev], "uv_size": [1, 1]},
													"west": {"uv": [j, i_rev], "uv_size": [1, 1]},
													"up": {"uv": [j, i_rev], "uv_size": [1, 1]},
													"down": {"uv": [j, i_rev], "uv_size": [1, 1]}
												}
										}
									]
								}
						
						pixel_geo["minecraft:geometry"][0]["bones"].append(new_bone)
		
		#print("Processing pixels... 100%")
		#print("Writing geometry file. This will take several seconds for large images")
		self.print_to_text("\n" + "Processing pixels... 100%" + "\n")
		self.print_to_text("\n" + "Writing geometry file. This will take several seconds for large images" + "\n")
		
		#write geometry file
		with open("pixel_projection/models/entity/pixel_projection.json", "w+") as f0:
			json.dump(pixel_geo, f0, separators=(',', ':'))
		
		#print("Writing texture image")
		self.print_to_text("\n" + "Writing texture image" + "\n")
		
		#set alpha of texture image
		alpha_mask = np.zeros_like(img)
		img_alpha = cv2.addWeighted(alpha_mask, 1.0, img, (self.geo_alpha.get() / 100), 0)
		
		#write image to texture folder
		cv2.imwrite("pixel_projection/textures/pixel_projection.png", img_alpha)
	
	def make_animation(self):
		#print("Writing animation file")
		self.print_to_text("\n" + "Writing animation file" + "\n")
		
		render_position = [
						"8 -(query.position(0)- " + str(self.r_coords_x.get()) + ")*16",
						"(" + str(self.r_coords_y.get()) + " -query.position(1))*16",
						"-8 +(query.position(2)- " + str(self.r_coords_z.get()) + ")*16"
					]
		with open("pixel_projection/animations/pixel_projection.json","r+") as f0:
			data=json.load(f0)
			data["animations"]["animation.pixel_projection"]["bones"]["static"]["position"] = render_position
		with open("pixel_projection/animations/pixel_projection.json","w+") as f1:
		    json.dump(data,f1,indent=2, separators=(',', ':'))

if __name__ == "__main__":
    app = PixelProjectionApp()
    app.run()