import os
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
from datetime import datetime
import pandas as pd
import time
from src import config
from io import StringIO
import get_blob_data
import main_visualizer


class Receiver:

	def __init__(self):

		self.queue_empty = True

	def read_queue(self):
		try:
		    servicebus_client = ServiceBusClient.from_connection_string(conn_str=config.VIZ_QUEUE_CONNECTION_STR, logging_enable=True)
		    with servicebus_client:
		        # get the Queue Receiver object for the queue
		        receiver = servicebus_client.get_queue_receiver(queue_name=config.VIZ_QUEUE_NAME, max_wait_time=5)
		        with receiver:
		            for msg in receiver:
		            	self.queue_empty = False
		            	self.msg_dict = json.loads(str(msg))
		            	print(self.msg_dict)
		            	data = get_blob_data.get_data(self.msg_dict['container_name'],
                                						self.msg_dict['blob_name'], 
                                						self.msg_dict['request_id'])
		            	main_visualizer.timelineviz(self.msg_dict['request_id'], "dummy", data)
		            	main_visualizer.retweetviz(self.msg_dict['request_id'], "dummy", data)
		            	main_visualizer.hashtagviz(self.msg_dict['request_id'], "dummy", data)
		            	receiver.complete_message(msg)
		    return self.queue_empty

		except Exception as ex:
		    print('Exception:')
		    print(ex)

	def get_flag(self):
		return self.queue_empty

	def get_message(self):
		return self.msg_dict

	def reset_flag(self):
		self.queue_empty = True

	def main(self):
		wait_time = 3
		while True:
		    self.queue_empty = self.read_queue()
		    # wait_time = 5 if self.queue_empty else 1
		    print("Waiting backoff: " + str(wait_time) + " seconds...")
		    time.sleep(wait_time)
		    self.reset_flag()

# if __name__ == '__main__':
receive = Receiver()
# receive.main()

