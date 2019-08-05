import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import Adafruit_DHT

# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script

ssl_private_key_filepath = '<Path for private key>'
ssl_algorithm = 'RS256' # Either RS256 or ES256
root_cert_filepath = '<Path for Root key>'
project_id = '<ProjectID>'
gcp_location = '<Region>'
registry_id = '<Registry>'
device_id = '<Device_id>'

# end of user-variables

#Define DHT Model here: DHT11 / DHT22
DHT = Adafruit_DHT.DHT11

#DHT sensor Pin Definition.Please give GPIO pin numbering / BCM model
pin = 4

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, ssl_algorithm)

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)

client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

client.on_connect = on_connect
client.on_publish = on_publish

client.tls_set(ca_certs='/home/pi/Desktop/MyTestDHT22/roots.pem') # Replace this with 3rd party cert if that was used when creating registry
client.connect('mqtt.googleapis.com', 8883)
client.loop_start()

# Could set this granularity to whatever we want based on device, monitoring needs, etc
temperature = 0
humidity = 0

for i in range(1, 11):
  cur_humidity, cur_temperature = Adafruit_DHT.read_retry(DHT, pin)

  if cur_temperature == temperature and cur_humidity == humidity:
    time.sleep(1)
    continue

  temperature = cur_temperature
  humidity = cur_humidity

  payload = '{{ "ts": {}, "temperature": {}, "humidity": {} }}'.format(int(time.time()), temperature, humidity)

  # Uncomment following line when ready to publish
  client.publish(_MQTT_TOPIC, payload, qos=1)

  print("{}\n".format(payload))

  time.sleep(3)

client.loop_stop()

