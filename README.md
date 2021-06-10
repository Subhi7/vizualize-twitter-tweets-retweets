# vizualize-twitter-tweets-retweets

This code uses Azure Service Bus to receive messages from ML module which stores predictions in Azure Storage Blob. 

The receiver_queue code reads the queue and triggers the visualization modules once the ML model has completed a request ID.

The main_visulizer file has functions for all three visualizations which makes interactive visualizations and stores them.

The app file contains Flask endpoints which renders these saved files as responses to GET requests from the Frontend module.

The render_template function of Flask Restapi uses a folder templates from which it renders the html hence the folder is named templates.

The following values have to be stored in the config file.
CONNECTION_STR
QUEUE_NAME
AZURE_STORAGE_CONNECTION_STRING
ML_QUEUE_CONNECTION_STR
ML_QUEUE_NAME
TENANT_ID

In order to run this code on local, the modules in requirements.txt file should be downloaded. Then app.py should be run. Once the endpoint receives a GET request, the receiver_queue thread is triggered and is listening for messages from the ML module. Flask endpoint has to be requested every 1 min until visualization is found. 

In order to run this code on Azure, this has to be published as an Azure Web Service App.
