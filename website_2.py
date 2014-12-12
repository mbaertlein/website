# ##################################################
# This program will begin a website that
# will work as my personal website, and 
# a way to control the lights in my room.
# It will work in concert with a teensy,
# so that if the Pi must reboot, or I 
# need to do work on the site, the lights
# will stay on
# ###################################################


# Import flask. This is how we will make our website.
from flask import Flask, request, render_template, g, url_for, redirect, session

# This will be used on the Raspberry Pi. Normal laptops will not 
# have nor be able to use this library.
import RPi.GPIO as GPIO

import threading
import time

# This is a user created file; it stores passwords and usernames.
import config

# Read in our room control username and password from config.py
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
SECRET_KEY = config.SECRET_KEY


class website:
	
	# Stores what value the lights are at:
	lightVal = False
	christmasVal = False
	
	# Outputs:
	latch = 5             # Lets the teensy know we are sending values.
	christmasOut = 22     # Tells the teensy if we want the christmas lights on or off.
	lightOut = 6          # Tells the teensy if we want the light on or off.
	
	# Inputs:
	lightIn = 9
	christmasIn = 10
	
	# For use with the web app
	app = Flask(__name__)
	app.config.from_object(__name__)
	
	# Threads.
	web_thread = None
	teensy_comm_thread = None
	
	
	def init(self):
	# Initializes the website. This is nonblocking,
	# but begins all process for the website to run.
	
		GPIO.setmode(GPIO.BCM)
		
		# Set up the outputs.
		GPIO.setup(self.latch, GPIO.OUT)
		GPIO.setup(self.lightOut, GPIO.OUT)
		GPIO.setup(self.christmasOut, GPIO.OUT)
		
		# Setup the Inputs. They are pull ups, so when the lights are on, 
		# the inputs are low.
		GPIO.setup(self.lightIn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(self.christmasIn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		
		# Check the inputs (are the lights on or off?)
		self.lightVal = not GPIO.input(self.lightIn)
		self.christmasVal = not GPIO.input(self.christmasIn)
		
		# This starts up the website.
		self.web_thread = threading.Thread(target = self.start)
		self.web_thread.daemon = True
		self.web_thread.start()

	
	def start(self):
	# Begin the web application.
		
		control.app.run('0.0.0.0', 80)
		
	
	def monitor(self):
	# Makes sure the website is still running.
	
		while(True):
			if(self.web_thread.is_alive() == False):
				self.web_thread = threading.Thread(target = self.start)
				self.web_thread.daemon = True
				self.web_thread.start()
				
	def update():
		
		GPIO.output(self.lightOut, control.lightVal)
		GPIO.output(self.christmasOut, control.christmasVal)
		GPIO.output(self.latch, True)
		time.sleep(1)
		GPIO.output(self.latch, False)
	
	
	# ############################################################################# #
	#                       Functions for personal website.                         #
	# ############################################################################# #
	
	
	# Home page.
	@app.route('/')  
	def home():
		return render_template('home_screen.html')
		
	# Contact page.
	@app.route('/contact',methods=['POST', 'GET'])  
	def contact():
		return render_template('contact.html')

	# About page.
	@app.route('/about')
	def about():
		return render_template('about.html')

	# Projects page.
	@app.route('/projects')
	def projects():
		return render_template('project.html')
		
	# Page describing this project.
	@app.route('/projects_room_control')
	def room_project():
		return render_template('project_room.html')
		
	# Page describing the garage door opener I made.
	@app.route('/projects_garage')
	def garage_project():
		return render_template('project_garage.html')
	
	
	# ############################################################################### #
	#                                Login and out                                    #
	# ############################################################################### #

	
	@app.route('/login', methods = ['GET', 'POST'])
	def login():
		
		error = None
		if request.method == 'POST':
			if request.form['username'] != control.app.config['USERNAME']:
				error = 'Invalid Username'
			elif request.form['password'] != control.app.config['PASSWORD']:
				error = 'Invalid Password'
			else:
				session['logged_in'] = True
				return redirect(url_for('control_main'))
		
		return render_template('login.html', error = error)


	@app.route('/logout')
	def logout():
		session.pop('logged_in', None)
		return redirect(url_for('home'))
		
		
		
	# ############################################################################### #
	#                                 Room Control                                    #
	# ############################################################################### #
	
	
	@app.route('/control')
	def control_main():
	# Begins the main control web page
	
		# Check our light values.
		control.lightVal = not GPIO.input(control.lightIn)
		control.christmasVal = not GPIO.input(control.christmasIn)
		
		# Render the template.
		return render_template('room_control.html', 
				       light=control.lightVal,
				       christmas=control.christmasVal)
	
	
	@app.route('/add/<which_light>',methods=['POST','GET'])
	def add_entry(which_light):
	# Change the light value
		
		# Try to log in.
		try:
			if not session['logged_in']:
				return redirect(url_for('login'))
		except:
			return redirect(url_for('login'))
		
		# Hey! We were logged in! Now lets change those values.
		
		# Make sure we have the right light values:
		control.lightVal = not GPIO.input(control.lightIn)
		control.christmasVal = not GPIO.input(control.christmasIn)
		
		# Check what we want to do.
		if(which_light == "light"):	
			control.lightVal = not control.lightVal
		
		elif(which_light == "christmas"):
			control.christmasVal = not control.christmasVal
		
		elif(which_light == "both_on"):
			control.christmasVal = True
			control.lightVal = True

		elif(which_light == "both_off"):
			control.christmasVal = False
			control.lightVal = False

		t = threading.Thread(target = control.update)
		t.daemon = True
		t.start()
		
		return redirect(url_for('control_main'))		

			
		
if(__name__ = "__main___"):
	
	web = website()
	web.init()
	
	while(1):
		web.monitor()
	
	
	
	
	
	
	