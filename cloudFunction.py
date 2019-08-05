import base64
from google.cloud import iot_v1


"""
Python3 implementation of configuration update 
"""
def device_config(config):
    client = iot_v1.DeviceManagerClient()
    name = client.device_path('<ProjectID>', '<Region>',  '<Registry>', '<Device_id>')
    binary_data = bytes(config, 'utf-8')
    client.modify_cloud_to_device_config(name, binary_data)


"""
I am getting 'temperature' data from a DHT11 sensor hooked up to Raspberry Pi. That data is compared 
against float(19.0), and correspondingly LED is turned on/off on ESP32.
My test data is as follows:

For turning ON the LED
{
    "data":"Saikumar",
    "temperature":"25.0" # For turning on the LED
}

For turning OFF the LED
{
    "data":"Saikumar",
    "temperature":"18.0" # For turning off the LED
}

And from Raspberry Pi, we are getting similar data
"""


def hello_pubsub(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))
    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
        temperature = base64.b64decode(event['temperature']).decode('utf-8')
        if float(temperature) > 19.0:
            device_config("ledon")
        else:
            device_config("ledoff")
    else:
        name = 'World'
    print('Hello {}!'.format(name))
    print('Temperature : {}'.format(temperature))
