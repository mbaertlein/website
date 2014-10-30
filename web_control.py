################################################
# Python script that sets up a website for 
# control over the light in Mitch Baertlein's
# room.  Also, monitors a light switch in his
# room.
################################################

from flask import Flask, request, render_template, g, url_for, redirect, session
import RPi.GPIO as GPIO
import threading

USERNAME = 'mitchell'
PASSWORD = 'pimAn123!'
SECRET_KEY = 'password_05181995'

class control:

	from flask import session

	# Variables
	light_val = False
	app = Flask(__name__)
	app.config.from_object(__name__)
	
	def device_monitor(self):
	# Monitors the light switch
	
		previous_value = GPIO.input(6)

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
	
	
	@app.route('/add',methods=['POST','GET'])
	def add_entry():
	# Change the light value
		try:
			if not session['logged_in']:
				return redirect(url_for('login'))
		except:
			return redirect(url_for('login'))

		control.light_val = not control.light_val
		GPIO.output(5, control.light_val)
		return redirect(url_for('control_main'))


	@app.route('/contact',methods=['POST', 'GET'])
	def contact():
		return render_template('contact.html')


	@app.route('/about')
	def about():
		return render_template('about.html')


	@app.route('/projects')
	def projects():
		return render_template('projects.html')
		
		
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
		return redirect(url_for('control_main'))
		
		
	def start(self):
	# Beginning the web application	
		
		control.app.run('0.0.0.0', 80)

if __name__ == "__main__":
	application = control()
	application.init()
	application.device_monitor()

