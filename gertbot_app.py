#!/home/pi/gertbot_app/bin/python3
##!/usr/bin/python3

# The modules here were taken fromt he code that came with the Gertbot.
#
# This code requires python3!
# Todo : detect and bom-out if using python2 
#

import time,sys
import os
import datetime
import signal
import gertbot as gb
import json
import psutil
import pika  #for rabbitMQ

DEBUG = 1

# board is global
board = 0

# channel is global
channel = 0

rabbitmq_pid_file = "/var/run/rabbitmq/pid"

ERROR_CODE = -1

mode_string = [
 "Off",            # 0x00
 "Brushed",        # 0x01
 "DCC",            # 0x02
 "Illegal",        # 0x03
 "Illegal",        # 0x04
 "Illegal",        # 0x05
 "Illegal",        # 0x06
 "Illegal",        # 0x07
 "Step Gray  Off", # 0x08
 "Step Pulse Off", # 0x09
 "Illegal",        # 0x0A
 "Illegal",        # 0x0B
 "Illegal",        # 0x0C
 "Illegal",        # 0x0D
 "Illegal",        # 0x0E
 "Illegal",        # 0x0F
 "Illegal",        # 0x10
 "Illegal",        # 0x11
 "Illegal",        # 0x12
 "Illegal",        # 0x13
 "Illegal",        # 0x14
 "Illegal",        # 0x15
 "Illegal",        # 0x16
 "Illegal",        # 0x17
 "Step Gray  Pwr", # 0x18
 "Step Pulse Pwr", # 0x19
 "Illegal",        # 0x16
 "Illegal" ]       # 0x17
 # In fact there are 256 codes but forget about that


RAMP_OFF=  0 # -
RAMP_010=  1 # 0.10 sec. 
RAMP_025=  2 # 0.25 sec.
RAMP_050=  3 # 0.50 sec.
RAMP_075=  4 # 0.75 sec.
RAMP_100=  5 # 1.00 sec.
RAMP_125=  6 # 1.25 sec.
RAMP_150=  7 # 1.50 sec.
RAMP_175=  8 # 1.75 sec.
RAMP_200=  9 # 2.00 sec.
RAMP_225= 10 # 2.25 sec.
RAMP_250= 11 # 2.50 sec.
RAMP_300= 12 # 3.00 sec.
RAMP_400= 13 # 4.00 sec.
RAMP_500= 14 # 5.00 sec.
RAMP_700= 15 # 7.00 sec.

ramp_string = [
 "no ramp",
 "0.10 sec.",
 "0.25 sec.",
 "0.50 sec.",
 "0.75 sec.",
 "1.00 sec.",
 "1.25 sec.",
 "1.50 sec.",
 "1.75 sec.",
 "2.00 sec.",
 "2.25 sec.",
 "2.50 sec.",
 "3.00 sec.",
 "4.00 sec.",
 "5.00 sec.",
 "7.00 sec." ]

short_string= ["nothing","channel","chan. pair","board","system" ]

movebrush_string = ["Stop","Move A","Move B"]

endstop_string = ["Off", "Low", "High"]

########
#
# Start PWM & DC brushed   
#
########  
def start_pwm_brushed (board=0, channel=0, direction='MOVE_B') :
    #output("Test PWM brushed on board %d\n" % (board))
    #output("Disable short protection for all four channels!!\n")


    # check status first!
    # don't start if already starting.
    try:
        status = get_motor_status(board,channel)
    except:
        output("Could not get status, returning.")
        return ERROR_CODE

    if 'Stop' not in status:
        output("Motor is already moving - ignoring, %s" % (status))
        return 0

    if (('MOVE_B' not in direction) and ('MOVE_A' not in direction)):
        output("Unknown direction given, %s" % (direction))
        return 0
    
    # Set channel for brushed and start motor 
    gb.set_mode(board,channel,gb.MODE_BRUSH)

    #board,channel,ramp_up,ramp_down,ramp_halt
    gb.set_brush_ramps(board, channel, RAMP_125, RAMP_075, RAMP_OFF)
    
    # MOVE_B is forward
    gb.move_brushed(board,channel,gb.MOVE_B)   
    #output("Start test channel %d " % (channel)) 

    freq = 30000

    dc = 100.0
      
    result = gb.pwm_brushed(board,channel,freq,dc)
    output("channel %d, freq %d DC %f\n" % (channel,freq,dc))
    output("Result=%s\n" % (result))
     
    #time.sleep(2)
    #gb.set_mode(board,channel,gb.MODE_OFF)
    return result

# start_pwm_brushed
#
########


########
#
# stop_pwm_brushed 
#
########
def stop_pwm_brushed(board=0, channel=0) :
    gb.set_mode(board,channel,gb.MODE_OFF)
# stop_pwm_brushed
#
########




# get version
# Board version MAJOR.MINOR is returned
# as MAJOR*100+MINOR
# return 0 on fail
# 
def get_version(board=0) :
   dest = (board<<2)
   wrtbuf = [0xA0, CMD_VERSION, dest, POST, POST, POST, POST]
   os.write(filehandle,bytes(wrtbuf))
   termios.tcdrain(filehandle)
   ok , data = read_uart(4)
   if (not ok) : # or wrtbuf[0]!=CMD_GET_ERROR or wrtbuf[1]!=dest) :
     return 0
   # convert xx.yy into xx*100+yy 
   # thus version 2.5 comes out as 205
   val = data[2]*100 + data[3]
   return val


########
#
# read error 
#
########  
def read_error(board=0, channel=0) :
   result = ''
   output("Test reading error from board %d\n" % (board))
   # testing if error readback works
   # Not testing all possible error codes
   gb.set_mode(board,0,gb.MODE_OFF)
   output("\nGive PWM brushed command to channel which is off")
   gb.pwm_brushed(board,0,100,50)
   time.sleep(1)
   errno = gb.read_error_status(board)
   output("Error number = %d (%s)" % (errno, gb.error_string(errno)) )
   result += "Error number = %d (%s)" % (errno, gb.error_string(errno)) 
   gb.set_mode(board,1,gb.MODE_BRUSH)
   output("\nGive Freq stepper command to channel which is in brushed mode")
   #result += "\nGive Freq stepper command to channel which is in brushed mode"
   gb.freq_stepper(board,channel,100)
   time.sleep(1)
   errno = gb.read_error_status(board)
   output("Error number = %d (%s)" % (errno, gb.error_string(errno)) )
   
   output("\nGive illegal brushed freq command to channel which is in brushed mode")
   #result += "Give illegal brushed freq command to channel which is in brushed mode"

   gb.send_raw([0xA0, gb.CMD_LINFREQ, 1, 0, 0, 0x50, 0x50])
   errno = gb.read_error_status(board)
   output("Error number = %d (%s)" % (errno, gb.error_string(errno)) )
   result += "Error number = %d (%s)" % (errno, gb.error_string(errno))
   return result


########  
#
# test motor status
#
########  
def test_motor_status(board=0, channel=0) :
   board = 1
   output("Test get motor data board %d" % (board))
   for channel in range (0,4) : 
      output("get_motor_config chan %d" % (channel))
      #input();
      motor_data = gb.get_motor_config(board,channel)
      # Returns a list with 8 integers
      # [0] = operating mode 
      # [1] = endstop mode, 4 bits
      #        0x01: A set, 0x02: B set
      #        0x04: A High 0x08: B high
      # [2] = short mode 
      # [3] = frequency in integer format
      #       brushed motors: integer =freq
      #       stepper motors: integer =freq*256
      # [4] = duty_cycle  (ignore for steppers)
      # [5] = ramp up     (ignore for steppers)
      # [6] = ramp down   (ignore for steppers)
      # [7] = ramp halt   (ignore for steppers)
      output("Operating mode: %s" % (mode_string[ motor_data[0] ]) )
      if (motor_data[0]!=0) : 
         output("Short mode: %s" % (short_string[ motor_data[2] ]) )
        
      if motor_data[0]==gb.MODE_BRUSH or (motor_data[0] & gb.MODE_STEP_MASK) :
      # motor mode 
      
         # end stops 
         if motor_data[1] & 0x01 :
         # A is on 
            if motor_data[1] & 0x04 :
               output("A-high")
            else :
               output("A-low")
         else :
            output("A-off")
         if motor_data[1] & 0x02 :
         # B is on 
            if motor_data[1] & 0x08 :
               output("B-high")
            else :
               output("B-low")
         else :
            output("B-off")
            
         if motor_data[0]==gb.MODE_BRUSH :
            f1 = motor_data[4]/10.0
            output("Frequency = %d" % (motor_data[3]) )
            # this is why I hate python: 
            # f1 = motor_data[4]/10.0  is fine 
            # but 
            # print("Duty Cycle= %.1f" % motor_data[4]/10.0) fails!
            output("Duty Cycle= %.1f" % (f1) )
            output("Ramp up   = %d, %s" % (motor_data[5],ramp_string[ motor_data[5] ]) )
            output("Ramp down = %d, %s" % (motor_data[6],ramp_string[ motor_data[6] ]) )
            output("Ramp halt = %d, %s" % (motor_data[7],ramp_string[ motor_data[7] ]) )
         else : 
            f1 = motor_data[3]/256.0
            output("Freq= %.2f" % (f1))
   ######
   for rep in range(0,5) : 
     output("get_motor_status 1.0")
     #input()
     motor_data = gb.get_motor_config(1,0)
     mode = motor_data[0]
     output("Operating mode:%d, %s" % (mode,mode_string[ mode ]))
     motor_data = gb.get_motor_status(1,0)
     if mode==gb.MODE_BRUSH or (mode & gb.MODE_STEP_MASK) :
        output("Move=%d, %s" % (motor_data[0],movebrush_string[ motor_data[0] ]) )
     if mode & gb.MODE_STEP_MASK : 
        output("%d steps" % (motor_data[1]) )
   for rep in range(0,5) : 
      output("get_motor_missed 1.0")
      #input()
      motor_data = gb.get_motor_missed(1,0)
      output("Missed %d steps" % (motor_data[0]) )


########  
#
# Test baudrate change
#
########  
def test_baudrate() :
   output("Test baudrate change")
   for baud in range(1,4) : 
     # check we can talk now
     version = gb.get_version(board)
     if (version==-1) : 
        output("Can't get version pre baudrate change")
        return
     else:
        output("Pre-set version=%d" % (version))        
        output("Set baudrate %d" % (baud))
        gb.set_baudrate(baud) 
        version = gb.get_version(board)
        if (version==-1) : 
           output("Can't get version post baudrate change")
           return
        else:
           output("Post set version %d" % (version))
   # restore 57.6K baudrate!!!
   output("Restoring 57K6 baudrate")
   gb.set_baudrate(2)


def get_motor_config(board=0, channel=0) :
    # Returns a list with 8 integers
    # [0] = operating mode 
    # [1] = endstop mode, 4 bits
    #        0x01: A set, 0x02: B set
    #        0x04: A High 0x08: B high
    # [2] = short mode 
    # [3] = frequency in integer format
    #       brushed motors: integer =freq
    #       stepper motors: integer =freq*256
    # [4] = duty_cycle  (ignore for steppers)
    # [5] = ramp up     (ignore for steppers)
    # [6] = ramp down   (ignore for steppers)
    # [7] = ramp halt   (ignore for steppers)
    motor_config = gb.get_motor_config(board,channel)

    #assign words to codes
    motor_config[0] = movebrush_string[int(motor_config[0])]
    #motor_config[1] = endstop_string[int(motor_config[1])]
    motor_config[2] = short_string[int(motor_config[2])]
    motor_config[5] = ramp_string[int(motor_config[5])]
    motor_config[6] = ramp_string[int(motor_config[6])]
    motor_config[7] = ramp_string[int(motor_config[7])]
    
    #put in json
    motor_config_header = ['mode', 'endstop', 'short', 'freq', 'duty-cycle', 'ramp-up', 'ramp-down', 'ramp-halt']
    # combine header with config info
    motor_config_list = list(zip(motor_config_header, motor_config))
    #print("Z: %s\n" % str(z))
    
    #return motor_config
    return motor_config_list


def get_motor_status(board=0, channel=0) :
    try:
        motor_status_list = gb.get_motor_status(board,channel)
    except:
        output("Cannot get motor_list_status!\n")
        return -1

    # motor status :    0 = off
    #                   1 = MOVE_A backwards
    #                   2 = MOVE_B forwards
    # backwareds and forwards are relative
    #output("Motor status=%s\n" % (motor_status_list[0]) )
    return movebrush_string[motor_status_list[0]]


def output(output_string='') :
    if DEBUG :
        print("%s" % output_string)
    return 0


def check_request(body):
    try:
        command_json = str(body.decode("utf-8","strict"))
    except:
        output("body is not a byte code: %s\n" % (str(body)))
        return ERROR_CODE

    
    #output("Command = %s\n" % (command_json))

    try:
        #wrap this all in a "Try" for error checking!
        parsed_json = json.loads(command_json)
        #output("JSON=%s\n" % (parsed_json))
    except:
        output("JSON Loads failed=%s\n" % (str(parsed_json)))
        return ERROR_CODE

    #print(type(parsed_json), repr(parsed_json))
    #try:
        #for key in parsed_json:
            #print("Key:%s\n" % (key))
        #for k, v in parsed_json.items():
            #temp = [key, value]
            #dictlist.append(temp)
            #print("Key=%s  Value=%s \n" % (str(k),str(v)))
    #except:
        #output("Error with dict to list")
        #return ERROR_CODE
        
    #first_command = parsed_json[0]
    #output("First_command = %s\n" % (first_command))
    
    try:
        my_command = parsed_json['command']
        output("Command received = %s" % (my_command))
    except:
        output("No command given in JSON: %s\n" % (str(parsed_json)))
        return ERROR_CODE

    #output("Board=%s\n" % (gertbot_board))
    #output("Channel=%s\n" % (gertbot_channel))
    
    if my_command == "status":
        result = get_motor_status(gertbot_board,gertbot_channel)
        return result

    if my_command == "config":
        result = get_motor_config(gertbot_board,gertbot_channel)
        return result

    if my_command == "version":
        result =  gb.get_version(gertbot_board)
        return result
    
    if my_command == "read_error":
        result = read_error(gertbot_board)
        return result
    
    if my_command == "start_a":
        result = start_pwm_brushed(gertbot_board,gertbot_channel, 'MOVE_A')
        return result

    if my_command == "start_b":
        result = start_pwm_brushed(gertbot_board,gertbot_channel,'MOVE_B')
        return result
    
    if my_command == "stop":
        result = stop_pwm_brushed(gertbot_board,gertbot_channel)
        return result

    if my_command == "emergency_stop":
        result = gb.emergency_stop()
        return result
    
    return ERROR_CODE


def on_request(ch, method, props, body):
    #body should be a byte code 
    #print(type(body), repr(body))

    response = check_request(body)

    #response needs to be in JSON format
    response = json.dumps({"response" : response}, sort_keys=True)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    output("%s Response=%s  ID:%s\n" % (str(timestamp), str(response), str(props.correlation_id)) )

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)


def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S") 
    output("Exiting at %s\n" % (str(timestamp)))
    gb.stop_all()
    sys.exit(1)
    return 0

##########################################################################################
##########################################################################################
##########################################################################################

### Initialize ######
test = 0
board = 0
chan  = channel
gertbot_board = 0
gertbot_channel = 0

gb.open_uart(0)

gb.stop_all()

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)

output("Starting gertbot_app\n")

version = gb.get_version(board)
output("GertBot Version is %d\n" % (version))


#test_baudrate()
#read_error()
#test_move_brushed()


#start_pwm_brushed()
#time.sleep(10)
#stop_pwm_brushed()

#get_motor_status(brd,mot)

#motor_data = gb.get_motor_config(board,channel)
motor_data = get_motor_config()
#output("Operating mode: %s" % str(mode_string[ motor_data[0] ]) )
#output("Short mode: %s" % (short_string[ motor_data[2] ]) )
output("Motor Configuration: %s \n" % (str(motor_data)))


mode = motor_data[0]   

motor_status = get_motor_status(gertbot_board, gertbot_channel)
output("Motor status: %s \n" % (motor_status))

#stop_pwm_brushed()

# Make sure that RabbitMQ is running!
if os.path.exists(rabbitmq_pid_file):
        try:
            f = open(rabbitmq_pid_file, 'r')    
        except:
            output("Cannot open pid file for RabbitMQ (%s), exiting." % (rabbitmq_pid_file))
            exit()
        else:
            rabbitmq_pid = f.read()
            f.close()
            #output("PID=%s" % (rabbitmq_pid))
            if not psutil.pid_exists(int(rabbitmq_pid)):
                output("RabbitMQ-server doesn't seem to be running, exiting.")
                exit()
else:
    output("PID file does not exist (%s), exiting." % (rabbitmq_pid_file))
    exit()

#output("PID=%s\n" % (rabbitmq_pid))

# Configure RabbitMQ event loop
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='gertbot_queue')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='gertbot_queue')

# Start RabbitMQ event loop
print(" [x] Awaiting RPC requests")
channel.start_consuming()
