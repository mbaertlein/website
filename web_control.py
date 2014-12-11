################################################
# Python script that sets up a website for 
# control over the light in Mitch Baertlein's
# room, including some Christmas lights.   
# Also, monitors a light switch in his
# room.
################################################

#Tell the program if we are in debugging mode
debug_mode = True

from flask import Flask, request, render_template, g, url_for, redirect, session

if not debug_mode:
	import RPi.GPIO as GPIO

import threading
import config

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
SECRET_KEY = config.SECRET_KEY

class control:

	from flask import session

	# Variables
	light_val = False
	christmas_val = False
	f = None
	app = Flask(__name__)
	app.config.from_object(__name__)
	
	global debug_mode
	d_mode = debug_mode
	

	def device_monitor(self):
	# Monitors the light switch
	
		previous_value = GPIO.input(6)

		while(True):

			current_value = GPIO.input(6)
			
			if(current_value != previous_value):
				
				control.light_val = not control.light_val
				GPIO.output(5, control.light_val)
				control.f.seek(0,0)
				control.f.write(str(int(control.light_val))+"\n"+str(int(control.christmas_val))+"\n")
				control.f.flush()
			
			previous_value = current_value

			
	def init(self):
	# Initializes the GPIO pins.
		if not self.d_mode:
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(5, GPIO.OUT)
			GPIO.setup(22, GPIO.OUT)
			GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_UP)

			file_name="/home/Python_Scripts/room_control/source/reboot_vals.txt"
			control.f = open(file_name, "a+")
			control.f.seek(0,0)
			data = control.f.read().split()
			control.light_val = int(data[0])
			control.christmas_val = int(data[1])
			GPIO.output(5, int(data[0]))
			GPIO.output(22, int(data[1]))
			control.f.close()

			control.f = open(file_name, "w")
			control.f.write(str(int(control.light_val))+"\n"+str(int(control.christmas_val))+"\n")
			control.f.flush()
			t = threading.Thread(target = self.start)
			t.daemon = True
			t.start()
			
		else:
			self.start()

	
	@app.route('/')
	def home():
	# Begins the home page

		return render_template('home_screen.html')
	
	@app.route('/control')
	def control_main():
	# Begins the main control web page

		return render_template('room_control.html', 
				       light=control.light_val,
				       christmas=control.christmas_val)
	
	
	@app.route('/add/<which_light>',methods=['POST','GET'])
	def add_entry(which_light):
	# Change the light value
		
		try:
			if not session['logged_in']:
				return redirect(url_for('login'))
		except:
			return redirect(url_for('login'))
		
		if(which_light == "light"):
			control.light_val = not control.light_val
			GPIO.output(5, control.light_val)
		
		elif(which_light == "christmas"):
			control.christmas_val = not control.christmas_val
			GPIO.output(22, control.christmas_val)
		elif(which_light == "both_on"):
			control.christmas_val = True
			control.light_val = True
			GPIO.output(5, True)
			GPIO.output(22, True)
		elif(which_light == "both_off"):
			control.christmas_val = False
			control.light_val = False
			GPIO.output(5, False)
			GPIO.output(22, False)
		
		control.f.truncate()
		control.f.seek(0,0)
		control.f.write(str(int(control.light_val))+"\n"+str(int(control.christmas_val))+"\n")
		control.f.flush()
		return redirect(url_for('control_main'))


	@app.route('/contact',methods=['POST', 'GET'])
	def contact():
		return render_template('contact.html')


	@app.route('/about')
	def about():
		return render_template('about.html')


	@app.route('/projects')
	def projects():
		return render_template('project.html')
		
		
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
		
	@app.route('/projects_room_control')
	def room_project():
		return render_template('project_room.html')
		
	@app.route('/projects_garage')
	def garage_project():
		return render_template('project_garage.html')


	@app.route('/logout')
	def logout():
		session.pop('logged_in', None)
		return redirect(url_for('home'))
		
		
	def start(self):
	# Beginning the web application	
		if not self.d_mode:
			control.app.run('0.0.0.0', 80)
		else:
			control.app.run()
		
if __name__ == "__main__":
	application = control()
	application.init()
	if not debug_mode:
		application.device_monitor()

