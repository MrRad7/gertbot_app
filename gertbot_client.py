#!/home/pi/gertbot_app/bin/python3
import pika
import uuid
import json
import argparse

class GertbotRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = str(body.decode("utf-8","strict"))

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='gertbot_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)
    

################################################################

parser = argparse.ArgumentParser()    
parser.add_argument("command", help="The command that you want to run.\n Valid commands are: start_a start_b stop status config version read_error emergency_stop")
args = parser.parse_args()


command = str(args.command)
print("Command=",command)

gertbot_rpc = GertbotRpcClient()

print(" [x] Requesting GertBot(status)")

#command = "config" #start_a start_b stop status config version read_error emergency_stop
#command_json = json.dumps([{"command" : command}], sort_keys=True)
command_json = json.dumps({"command" : command}, sort_keys=True)

print("CommandJSON=",command_json)

response = gertbot_rpc.call(command_json)
#response = str(response,('utf-8'))
#print(type(response), repr(response))
print(" [.] Got %s" % response)


exit()

command_list = ["version", "config", "status", "start", "status", "read_error", "stop", "status"]

for item in command_list:
    command_json = json.dumps({"command" : item}, sort_keys=True)
    print("CommandJSON=",command_json)
    response = gertbot_rpc.call(command_json)
    print(" [.] Got %s" % response)
