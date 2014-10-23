################################################
# Python script that sets up a website for 
# control over the light in Mitch Baertlein's
# room.  Also, monitors a light switch in his
# room.
################################################

from flask import Flask, request, render_template, g, url_for, redirect
import RPi.GPIO as GPIO
import threading

class control:
	
	# Variables
	light_val = False
	app = Flask(__name__)
	
	def device_monitor(self):
	# Monitors the light switch
	
		previous_value = GPIO.input(6)
		print "you made it!"
		while(True):

			current_value = GPIO.input(6)
			
			if(current_value != previous_value):
				
				control.light_val = not control.light_val
				GPIO.output(5, control.light_val)
			
			previous_value = current_value

	def init(self):
	# Initializes the GPIO pins.

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(5, GPIO.OUT)
		GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.output(5, False)

		t = threading.Thread(target = self.start)
		t.daemon = True
		t.start()

	
	@app.route('/')
	def home():
	# Begins the home page

		return render_template('home_screen.html')
	
	@app.route('/control')
	def control_main():
	# Begins the main control web page

		return render_template('room_control.html', 
				       light=control.light_val)
	
	
	@app.route('/add',methods=['POST'])
	def add_entry():
	# Change the light value

		control.light_val = not control.light_val
		GPIO.output(5, control.light_val)
		return redirect(url_for('control_main'))

	@app.route('/contact')
	def about():
		return render_template('about.html')
	def start(self):
	# Beginning the web application

		self.app.run('0.0.0.0', 80)

if __name__ == "__main__":
	application = control()
	application.init()
	application.device_monitor()

