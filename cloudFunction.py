import base64
import json
from google.cloud import iot_v1


def device_config(config):
    client = iot_v1.DeviceManagerClient()
    name = client.device_path(<PROJECT_ID>,
                              <REGION>,  <REGISTRY>, <DEVICCE_ID>)
    binary_data = bytes(config, 'utf-8')
    client.modify_cloud_to_device_config(name, binary_data)


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

    print("""This Function was triggered by messageId {} published at {}""".format(
        context.event_id, context.timestamp))

#    name = str(base64.b64decode(event).decode('utf-8'))
    if 'data' in event:
        data = event['data']
        data = base64.b64decode(data)
        data = data.decode('utf-8')
        data = json.loads(data)
        
        temperature = float(data['temperature'])
        
        if temperature > 25.0:
            device_config("ledon")
        else:
            device_config("ledoff")
            
    else:
        print("Data is not present!")
