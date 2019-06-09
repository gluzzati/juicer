from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from core import log
from core.events import json2evt, EventKey, validate

port = 8883
pub_topic = "juicer_events"
sub_topic = "juicer_commands"


class AWSProxy:
    def __init__(self, endpoint, rootCA, cert, key, clientId, main_queue):
        self.key = key
        self.rootCA = rootCA
        self.cert = cert
        self.endpoint = endpoint
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.main_queue = main_queue

        # Init AWSIoTMQTTClient
        myAWSIoTMQTTClient = None
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(endpoint, port)
        myAWSIoTMQTTClient.configureCredentials(rootCA, key, cert)

        self.aws_client = myAWSIoTMQTTClient
        self.unacked_messages = dict()
        self.subscribed = False

    def __ack_message(self, mid):
        log.debug("acked message " + str(mid))
        if self.unacked_messages.pop(mid, None) is None:
            log.warn("I have no recollection of message {} you're trying to ack..".format(mid))

    def __ack_subscribe(self, mid, data):
        log.ok("aws subscribe ack: granted QoS " + str(data[0]))
        self.subscribed = True

    def __on_remote_pub(self, client, userdata, message):
        log.debug("received message with topic " + message.topic)
        ok, evt = json2evt(message.payload.decode())
        if ok:
            ok = validate(evt)
        else:
            log.warn("discarding invalid event")
        if ok:
            log.debug("dispatching " + evt[EventKey.type])
            self.main_queue.put(evt)
        else:
            log.warn("discarding malformed event received from the cloud")
            log.warn(message.payload.decode())

    def register(self):
        # AWSIoTMQTTClient connection configuration
        self.aws_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.aws_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.aws_client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.aws_client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.aws_client.configureMQTTOperationTimeout(5)  # 5 sec

        self.aws_client.connect()
        self.subscribe()

    def publish(self, message):
        message_id = self.aws_client.publishAsync(self.pub_topic, message, 1, ackCallback=self.__ack_message)
        self.unacked_messages[message_id] = message

    def subscribe(self):
        """
        *messageCallback* - Function to be called when a new message for the subscribed topic
        comes in. Should be in form :code:`customCallback(client, userdata, message)`, where
        :code:`message` contains :code:`topic` and :code:`payload`. Note that :code:`client` and :code:`userdata` are
        here just to be aligned with the underneath Paho callback function signature. These fields are pending to be
        deprecated and should not be depended on.
        """
        self.aws_client.subscribeAsync(self.sub_topic, 1, messageCallback=self.__on_remote_pub,
                                       ackCallback=self.__ack_subscribe)
