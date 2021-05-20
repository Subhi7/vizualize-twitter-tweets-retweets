from flask import Flask, render_template, request
import main_visualizer
import os
import glob
# import os, shutil
import os.path
from os import path
import get_blob_data
from flask_executor import Executor
from receiver_queue import receive

app = Flask('flaskwp1')
app.config['TEMPLATES_AUTO_RELOAD'] = True
# webcode = open('webcode.html').read() - not needed
executor = Executor(app)

flag = 0
cnt = 0

# def long_running_job():
# 	print("started")
# 	global flag
# 	flag = 1

# 	while 1:
# 		global cnt
# 		cnt = cnt + 1
# 		if cnt == 1000000:
# 			print('thats it')

def receiver():
	global flag
	flag = 1
	receive.main()


 
@app.route("/")
def hello_test():
	return render_template('1414_RTN.html')

@app.route("/random")
def hello():
	message = request.args.get('message')
	return {"hi": message}

@app.route('/timeline-viz')
def webprint():

	global flag
	print("flag value isssss", flag)
	if flag == 0:
		executor.submit(receiver)

	request_id = request.args.get('request_id')
	hashtag = request.args.get('hashtag')
	filename = f"{request_id}_timeline.html"

	if str(path.isfile('templates/filename')):
		return render_template(filename)

	# data = get_blob_data(1,2,3)

	# main_visualizer.timelineviz(request_id, data)
	# main_visualizer.retweetviz(request_id, data)

	return {'status': 'ML model still working on {request_id}'}

@app.route('/graph-viz')
def webprint_2():
	global flag
	print("flag value isssss", flag)
	if flag == 0:
		executor.submit(receiver)

	request_id = request.args.get('request_id')
	hashtag = request.args.get('hashtag')
	filename = f"{request_id}_RTN.html"

	# if str(path.isfile('templates/filename')):
	# 	return render_template(filename)

	# while receive.get_flag():
	# 	time.sleep(1)
	
	# receiver.reset_flag()
	# msg_dict = receive.get_message()
	# data = get_blob_data(msg_dict['container_name'],
	#                         msg_dict['blob_name'], 
	#                         msg_dict['request_id'])

	if str(path.isfile('templates/filename')):
		return render_template(filename, hashtag = hashtag)

	return {'status': 'ML model still working on {request_id}'}

# if __name__ == '__main__':
#     app.run(host = '127.0.0.1', port = 3000)

if __name__ == '__main__':
	app.run(debug=True)
	