from awscrt import io, mqtt5
from awsiot import mqtt_connection_builder
import time as t
import json

ENDPOINT = ""
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = ""
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
PATH_TO_PRIVATE_KEY = ""
MESSAGE = "HELLO WORLD"
TOPIC = "TEST/TESTING"
RANGE = 20

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(endpoint=ENDPOINT,
                                                         cert_filepath=PATH_TO_CERTIFICATE,
                                                         pri_key_filepath=PATH_TO_PRIVATE_KEY,
                                                         client_bootstrap=client_bootstrap,
                                                         ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
                                                         clean_session=False,
                                                         keep_alive_secs=6
                                                         )
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range(RANGE):
    data = "{} [{}]".format(MESSAGE, i + 1)
    message = {"message": data}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt5.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
    t.sleep(0.1)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
