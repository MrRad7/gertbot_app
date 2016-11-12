#
# This code requires python3!
# Todo : detect and bom-out if using python2 
#

import time,sys
import gertbot as gb

# board is global
board = 0


def usage() :
   print("Usage: [-tTEST] [-bBOARD]")
#   print("PORT is the comport number to use (1-32)")
   print("BOARD is the board to use (0-3)")
   print("TEST is the test to run:")
   print("  0 : run all")
   print("  1 : test_mode")
   print("  2 : test_endstop_short")
   print("  3 : test_move_brushed")
   print("  4 : test_pwm_brushed")
   print("  5 : test_move_stepper")
   print("  6 : test_stop_stepper")
   print("  7 : test_freq_stepper")
   print("  8 : test_read_error_status")
   print("  9 : test_set_pin_mode")
   print(" 10 : test_set_all_pins_mode")
   print(" 11 : test_outputs")
   print(" 12 : test_adc_dac")
   print(" 13 : test_inputs")
   print(" 14 : test_get_io_setup")
   print(" 15 : test_dcc")
   print(" 16 : test_get_motor")
   print(" 17 : test_set_baud")
   print(" 18 : test_quad")
   print(" 19 : test_endstop2")
   print(" 20 : test_hotshort (new rev)")
   print("")
   exit(1)
#  usage

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
 
ramp_string = [
 "no ramp  ",
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

short_string= ["nothing   ","channel   ","chan. pair","board     ","system    " ]

movebrush_string = ["Stop  ","Move A","Move B"]


########
#
# Test operating modes 
#
########
def test_mode() :
   TST_NUM_MODES = 7
   test_mode_table = [
     gb.MODE_OFF,
     gb.MODE_BRUSH,
     gb.MODE_DCC,
     gb.MODE_STEPG_OFF,
     gb.MODE_STEPP_OFF,
     gb.MODE_STEPG_PWR,
     gb.MODE_STEPP_PWR
   ]

   print("Test operating modes on board %d\n" % board)
   for channel in range(0,4) : 
      for mode in range(0,TST_NUM_MODES) :
         mode_code = test_mode_table[mode]
         if not ((mode_code & gb.MODE_STEP_MASK) and (channel & 1)) : 
            gb.set_mode(board,channel,mode_code)
            print("channel %d, mode %d (%s)\n" % (channel,mode_code,mode_string[mode_code]))
            input()
         # if not 
      # for mode
   # for channel
#
########
  
 

######## 
#
# Test end stops 
#
########
def test_endstop_short() :
   endstop_string= ["Off ","Low ","High"]
   print("Test end-stop mode on board %d\n" % board)
   for channel in range(0,4) :
      gb.set_mode(board,channel,gb.MODE_BRUSH) # endstop controls visible
      for mode_A in range(0,3) :
         for mode_B in range(0,3) :
            gb.set_endstop(board,channel,mode_A,mode_B)
            print("channel %d, mode A %d (%s) mode B %d (%s)\n" % \
               (channel,mode_A,endstop_string[mode_A],mode_B,endstop_string[mode_B]) )
            input()
         # for mode B
      # for mode A
   # for channel
   
   print("Test short/hot mode on board %d\n" % board);
   for channel in range(0,4) :
      for shrt in range(gb.SHORT_NONE,gb.SHORT_SYST+1) :
         print("channel %d, short/hot mode %d (Stop %s)\n" % (channel,shrt,short_string[shrt] ));
         gb.set_short(board,channel,shrt);
         input()
      # for short
   # for channel

   
# test_endstop
#
########


######## 
#
# Test end stops new revision
#
########
def test_endstop2() :
   endstop_string= ["Off ","Low ","High"]
   print("Test end-stop mode on board %d\n" % board)
   for channel in range(0,4) :
      gb.set_mode(board,channel,gb.MODE_BRUSH) # endstop controls visible
      for mode_A in range(0,3) :
         for mode_B in range(0,3) :
            filtA=85*mode_A
            filtB=75*mode_B+75
            gb.set_endstop2(board,channel,mode_A,mode_B,filtA,filtB)
            print("channel %d, mode A %d (%s) mode B %d (%s) A-filt %d b_filt %d\n" % \
               (channel,mode_A,endstop_string[mode_A],mode_B,endstop_string[mode_B],filtA,filtB) )
            input()
         # for mode B
      # for mode A
   # for channel
   
# test_endstop2
#
########


######## 
#
# Test new hot/short
#
########
def test_hotsort() :
   print("Test short/hot mode on board %d\n" % board);
   for channel in range(0,4) :
      for shrt in range(gb.SHORT_NONE,gb.SHORT_SYST+1) :
         print("channel %d, short/hot mode %d (Stop %s)\n" % (channel,shrt,short_string[shrt] ));
         gb.set_shorthot(board,channel,shrt);
         input()
   

########
#
# Test move brushed   
#
########  
def test_move_brushed() :
 
   print("Test move brush mode on board %d" % board)
   for channel in range(0,4) :
     gb.set_mode(board,channel,gb.MODE_BRUSH)
     gb.set_endstop(board,channel,gb.ENDSTOP_OFF,gb.ENDSTOP_OFF)
     for mode in range(0,3) :
        for ramp in range(2,15,4) : # Not testing each ramp!
           if mode==0 : 
             # need a running motor to test stop
             gb.move_brushed(board,channel,1)
             time.sleep(0.5)
           gb.move_brushed(board,channel,mode)
           print("channel %d, mode %d (%s) ramp %d (%s)\n" % \
              (channel,mode,movebrush_string[mode],ramp,ramp_string[ramp]))
           input()
           gb.move_brushed(board,channel,0) # fast stop 
           time.sleep(0.5)
       # ramp
     # mode
  # channel
# test_move_brushed
#
########

########
#
# Test PWM & DC brushed   
#
########  
def test_pwm_brushed () :
   print("Test PWM brushed on board %d\n",board)
   print("Disable short protection for all four channels!!\n")
   input()
   for channel in range(0,4) :
      # Set channel for brushed and start motor 
      gb.set_mode(board,channel,gb.MODE_BRUSH)
      gb.move_brushed(board,channel,gb.MOVE_B)   
      print("Start test channel %d " % channel) 
      freq = 250
      while freq<10000 : 
         dc=0.0
         while  dc<=100.0 :
            gb.pwm_brushed(board,channel,freq,dc)
            print("channel %d, freq %d DC %f\n" % (channel,freq,dc))
            dc = dc + 2
            time.sleep(0.2)
         # duty cycle
         freq=freq*2+3 
      # frequency
      gb.set_mode(board,channel,gb.MODE_OFF)
   # channel
# test_pwm_brushed
#
########  


########
#
# Test move stepper 
#
########  
def test_move_stepper() :
   step_table = [100000,50000,25000,5000,500,4,4 ] 
   print("Test move stepper on board %d\n" % board)
   for channel in range(0,4,2) :
      gb.set_mode(board,channel,gb.MODE_STEPG_OFF)
      gb.freq_stepper(board,channel,5000)
      # Now at 5000 Hz 
      for s in range (0,7) :
         steps = step_table[s]
         if step_table[s]>50000 :
            gb.freq_stepper(board,channel,5000) #
            freq = 5000
         else : 
            gb.freq_stepper(board,channel,1000) #
            freq = 1000
         gb.move_stepper(board,channel,steps)
         secs = (int)(steps/freq)
         print("channel %d, steps %d (%d sec.)\n" % (channel,steps,secs))
         # wait secs + 1 seconds 
         secs = secs + 1
         for dot in range(0,secs) :
           sys.stdout.write('.')
         sys.stdout.flush()
         for dot in range(0,secs) :
            time.sleep(1)
            sys.stdout.write("\u0008 \u0008")
            sys.stdout.flush()
         print("done\n")
      # steps
      
      for s in range (0,7) :
         steps = step_table[s]
         if step_table[s]>50000 :
            gb.freq_stepper(board,channel,5000) #
            freq = 5000
         else : 
            gb.freq_stepper(board,channel,1000) #
            freq = 1000
         gb.move_stepper(board,channel,-steps)
         secs = (int)(steps/freq)
         print("channel %d, steps %d (%d sec.)\n" % (channel,-steps,secs))
         # wait secs + 1 seconds 
         secs = secs + 1
         for dot in range(0,secs) :
           sys.stdout.write('.')
         sys.stdout.flush()
         for dot in range(0,secs) :
            time.sleep(1)
            sys.stdout.write("\u0008 \u0008")
            sys.stdout.flush()
         print("done\n")
      # steps        
      gb.set_mode(board,channel,gb.MODE_OFF)
   # channel
# test_move_stepper


########
#
# Test stop stepper 
# 
########  
def test_stop_stepper() :
   stop_string = ["Passive","Active"]
   print("Test stop stepper on board %d\n" % board)
   for channel in range(0,4,2) :
      # Set channel for stepper and start motor 
      gb.set_mode(board,channel,gb.MODE_STEPG_PWR)
      gb.freq_stepper(board,channel,100)
      for mode in range (0,2) :
         gb.move_stepper(board,channel,5000000)
         print("channel %d, stop %d (%s) (press return to stop)\n" % \
            (channel,mode,stop_string[mode]) )
         input()
         gb.stop_stepper(board,channel,mode)
         print("check anchor, then press return\n");
         input()
      # mode
      print("Done: stop %d (%s)\n" % \
         (gb.STOP_OFF,stop_string[gb.STOP_OFF]) )
      gb.stop_stepper(board,channel,gb.STOP_OFF) # always end with stop passive
   # channel
# test_stop_stepper
#
########  

  
########
#
# Test freq stepper 
#
########  
def test_freq_stepper() :
   print("Test stepper frequency on board %d\n" % board)
   for channel in range(0,4,2) :
      # Set up channel for stepper  
      gb.set_mode(board,channel,gb.MODE_STEPG_OFF)
      gb.move_stepper(board,channel,5000)
      freq = 0.5
      while freq<=1000 :
         print("channel %d, freq %4.2f\n" % (channel,freq))
         gb.freq_stepper(board,channel,freq)
         freq=freq*2.0+0.5
         time.sleep(2)
    # frequency
  # channel
# test_freq_stepper
#
########  


########
#
# Test read error 
#
########  
def test_read_error() : 
   print("Test reading error from board %d\n" % board)
   # testing if error readback works
   # Not testing all possible error codes
   gb.set_mode(board,0,gb.MODE_OFF)
   print("\nGive PWM brushed command to channel which is off")
   gb.pwm_brushed(board,0,100,50)
   time.sleep(1)
   errno = gb.read_error_status(board)
   print("Error number = %d (%s)" % (errno, gb.error_string(errno)) )
   
   gb.set_mode(board,1,gb.MODE_BRUSH)
   print("\nGive Freq stepper command to channel which is in brushed mode")
   gb.freq_stepper(board,1,100)
   time.sleep(1)
   errno = gb.read_error_status(board)
   print("Error number = %d (%s)" % (errno, gb.error_string(errno)) )
   
   print("\nGive illegal brushed freq command to channel which is in brushed mode")
   gb.send_raw([0xA0, gb.CMD_LINFREQ, 1, 0, 0, 0x50, 0x50])
   errno = gb.read_error_status(board)
   print("Error number = %d (%s)" % (errno, gb.error_string(errno)) )


  

########
#
# Test set_pin_mode 
#
########  
def test_set_pin_mode() :
  print("Test set J3 pin mode in board %d" % board )
  
  print("Going to switch pins 1-10 to output (press return)") 
  input()
  for i in range(1,11) :
    gb.set_pin_mode(board,i,gb.PIN_OUTPUT)
    input()
    
  print("Going to switch pins 1-8 to endstop (press return)") 
  input()
  for i in range(1,9) :
    gb.set_pin_mode(board,i,gb.PIN_ENDSTOP)
    input()
    
  print("Going to switch pins 1-10 to input (press return)") 
  input()
  for i in range(1,11) :
    gb.set_pin_mode(board,i,gb.PIN_INPUT)
  ##
  print("Going to switch pins 13 to output (press return)") 
  input()
  gb.set_pin_mode(board,13,gb.PIN_OUTPUT)
  print("Going to switch pins 14 to output (press return)") 
  input()
  gb.set_pin_mode(board,14,gb.PIN_OUTPUT)
  print("Going to switch pins 15 to output (press return)") 
  input()
  gb.set_pin_mode(board,15,gb.PIN_OUTPUT)
  print("Going to switch pins 16 to output (press return)") 
  input()
  gb.set_pin_mode(board,16,gb.PIN_OUTPUT)
    
  print("Going to switch pins 13-16 to ADC (press return)") 
  input()
  for i in range(13,17) :
    gb.set_pin_mode(board,i,gb.PIN_ADC)
    
  print("Going to switch pins 13-16 to input (press return)") 
  input()
  for i in range(13,17) :
    gb.set_pin_mode(board,i,gb.PIN_INPUT)
  ##
  print("Going to switch pins 18 to DAC (press return)") 
  input()
  gb.set_pin_mode(board,18,gb.PIN_DAC)
  print("Going to switch pins 20 to DAC (press return)") 
  input()
  gb.set_pin_mode(board,20,gb.PIN_DAC)
    
  print("Going to switch pins 20 to output (press return)") 
  input()
  gb.set_pin_mode(board,20,gb.PIN_OUTPUT)
  print("Going to switch pins 18 to output (press return)") 
  input()
  gb.set_pin_mode(board18,gb.PIN_OUTPUT)
    
  print("Going to switch pins 18,20 to input (press return)") 
  input()
  gb.set_pin_mode(board,18,gb.PIN_INPUT)
  gb.set_pin_mode(board,20,gb.PIN_INPUT)
  
  print("Going to switch pins 18,20 to DAC (press return)") 
  input()
  gb.set_pin_mode(board,18,gb.PIN_DAC)
  gb.set_pin_mode(board,20,gb.PIN_DAC)
#
########  
 
 
   
########
#
# Test set_pin_mode 
#
########  
def test_set_all_pins() : 
  modes = [None]*20
  print("Test set all pins mode on board %d\n" % board)
  modes[0]  = gb.PIN_ENDSTOP
  modes[1]  = gb.PIN_OUTPUT
  modes[2]  = gb.PIN_INPUT
  modes[3]  = gb.PIN_ENDSTOP
  modes[4]  = gb.PIN_OUTPUT 
  modes[5]  = gb.PIN_INPUT  
  modes[6]  = gb.PIN_ENDSTOP
  modes[7]  = gb.PIN_OUTPUT 
  modes[8]  = gb.PIN_INPUT  
  modes[9]  = gb.PIN_OUTPUT
  modes[10] = gb.PIN_INPUT # impossible but should be ignored
  modes[11] = gb.PIN_INPUT # impossible but should be ignored
  modes[12] = gb.PIN_INPUT
  modes[13] = gb.PIN_INPUT
  modes[14] = gb.PIN_ADC
  modes[15] = gb.PIN_ADC
  modes[16] = gb.PIN_INPUT # impossible but should be ignored
  modes[17] = gb.PIN_INPUT 
  modes[18] = gb.PIN_INPUT # impossible but should be ignored
  modes[19] = gb.PIN_DAC
  print("E O I E O I E O I O - - I I A A - I - D")
  gb.set_allpins_mode(board,modes)
  input()

  modes[0]  = gb.PIN_OUTPUT
  modes[1]  = gb.PIN_INPUT
  modes[2]  = gb.PIN_ENDSTOP
  modes[3]  = gb.PIN_OUTPUT 
  modes[4]  = gb.PIN_INPUT  
  modes[5]  = gb.PIN_ENDSTOP
  modes[6]  = gb.PIN_OUTPUT 
  modes[7]  = gb.PIN_INPUT  
  modes[8]  = gb.PIN_OUTPUT
  modes[9]  = gb.PIN_INPUT
  modes[10] = gb.PIN_INPUT # impossible but should be ignored
  modes[11] = gb.PIN_INPUT # impossible but should be ignored
  modes[12] = gb.PIN_ADC
  modes[13] = gb.PIN_ADC
  modes[14] = gb.PIN_OUTPUT
  modes[15] = gb.PIN_INPUT
  modes[16] = gb.PIN_INPUT # impossible but should be ignored
  modes[17] = gb.PIN_DAC 
  modes[18] = gb.PIN_INPUT # impossible but should be ignored
  modes[19] = gb.PIN_OUTPUT
  print("O I E O I E O I O I - - A A O I - D - O")
  gb.set_allpins_mode(board,modes)
  input()
#
########  



########
#
# Test set_output_pin_state 
#
########  
def test_set_output() : 

   for i in range (0,4) :
      d0 = i & 1;
      d1 = (i & 2)>>1;
      print("Open drain %d %d\n" % (d0,d1));
      gb.activate_opendrain(board,d0,d1);
      input()
 
   modes = [None]*20
   for p in range (0,20) :
      modes[p] = gb.PIN_OUTPUT
   gb.set_allpins_mode(board,modes)  
   for r in range (0,10) :
      for p in range (0,16) :
         gb.set_output_pin_state(board,(1<<p))
         time.sleep(0.25)
   # back to input (is safer) 
   for p in range (0,20) :
      modes[p] = gb.PIN_INPUT
   gb.set_allpins_mode(board,modes)  
#
########  
     

########
#
# Test DACs and ADC 
#
########  
def test_dac_adc() : 
   # Test DAC
   board = 1
   print("Five step DAC0 increment Board 1\n")
   gb.set_pin_mode(board,20,gb.PIN_DAC);
   dac_value = gb.DAC_MIN
   for i in range (0,5) :
      gb.set_dac(board,0,dac_value)
      dac_value = dac_value + (gb.DAC_MAX - gb.DAC_MIN)/5
      input()
   print("Five step DAC1 increment Board 1\n")
   gb.set_pin_mode(board,18,gb.PIN_DAC);
   dac_value = gb.DAC_MIN
   for i in range (0,5) :
      gb.set_dac(board,1,dac_value)
      dac_value = dac_value + (gb.DAC_MAX - gb.DAC_MIN)/5
      input()
   
   # set ADC mode 
   for i in range(13,17) :
      gb.set_pin_mode(0,i,gb.PIN_ADC)
   print("Five times ADC's read from BOARD1 !!!\n")
   for i in range (0,5) :
      print("ADC0 : %6.3f\n" % gb.read_adc(board,0))
      print("ADC1 : %6.3f\n" % gb.read_adc(board,1))
      print("ADC2 : %6.3f\n" % gb.read_adc(board,2))
      print("ADC3 : %6.3f\n" % gb.read_adc(board,3))
      print("press return\n")
      input()
#
########  
 

######## 
#
# Test inputs 
#
########  
def test_inputs() :
   board = 1
   print("Test inputs board %d\n" % board)
   print("Performing ten reads\n");
   modes = [None]*20
   for pin in range(0,20) :
      modes[pin]=gb.PIN_INPUT;
   gb.set_allpins_mode(board,modes);
   for i in range (0,10) :
      print("Press return to read")
      input()
      status = gb.read_inputs(board);
      if status== -1 :
         print("read inputs failed\n");
      else :
         print("try %d: 0x%08X\n" % (i+1,status));
#
########  


########  
#
# Test get pin status  
#
########  
def test_get_io_setup() :
   io_string = [  " ---   ", "input  ", "output ", "endmode", "adc    ", "dac    ", "i2c    " ]
   board = 1
   print("Get I/O status board %d\n" % board)
   print("Performing four reads\n")
   for r in range (0,4) :
      print("Press return to read")
      input()
      pin_status = gb.get_io_setup(board)
      if not pin_status :
         print("gb.get_io_setup failed")
      else :
         for pin in range(0,20) :
            print("pin %d = %s" % (pin,io_string[pin_status[pin]]) )
      # if pin status
   # repeat test 
#
########  


########  
#
# Test DCC
#
########  
def test_dcc() :
   board = 0
   print("DCC test on board %d\n" % board)
   for chan in range(0,4) :
     gb.set_mode(board,chan,gb.MODE_DCC)
     
   print("Performing number of writes\n")
   message = [0x03, 0x68 ]
   print("0x03,0x68: move loc 3. Press return to send")
   input()
   gb.send_dcc_mess(board,0xF,message)
   
   message = [0x02, 0x67 ]
   print("0x02,0x67: move loc 2. Press return to send")
   input()
   gb.send_dcc_mess(board,0xF,message)

   message = [0x00, 0x40 ]
   print("0x00,0x40: Stop All. Press return to send")
   input()
   gb.send_dcc_mess(board,0xF,message)
   
   # Call the DCC config fuction to see if the syntax is correct 
   # I have no scope set-up now to verify it is functioning
   print("DCC config: pre-amble 64")
   gb.dcc_config(board,0,4,64,0)
   print("DCC config: repeat 15")
   gb.dcc_config(board,0,15,16,0)

#
########  


########  
#
# Test get motor
#
########  
def test_get_motor() :
   board = 1
   print("Test get motor data board %d" % board)
   for channel in range (0,4) : 
      print("get_motor_config chan %d" % channel)
      input();
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
      print("Operating mode: %s" % mode_string[ motor_data[0] ])
      if (motor_data[0]!=0) : 
         print("Short mode: %s" % short_string[ motor_data[2] ])
        
      if motor_data[0]==gb.MODE_BRUSH or (motor_data[0] & gb.MODE_STEP_MASK) :
      # motor mode 
      
         # end stops 
         if motor_data[1] & 0x01 :
         # A is on 
            if motor_data[1] & 0x04 :
               print("A-high")
            else :
               print("A-low")
         else :
            print("A-off")
         if motor_data[1] & 0x02 :
         # B is on 
            if motor_data[1] & 0x08 :
               print("B-high")
            else :
               print("B-low")
         else :
            print("B-off")
            
         if motor_data[0]==gb.MODE_BRUSH :
            f1 = motor_data[4]/10.0
            print("Frequency = %d" % motor_data[3])
            # this is why I hate python: 
            # f1 = motor_data[4]/10.0  is fine 
            # but 
            # print("Duty Cycle= %.1f" % motor_data[4]/10.0) fails!
            print("Duty Cycle= %.1f" % f1 )
            print("Ramp up   = %d, %s" % (motor_data[5],ramp_string[ motor_data[5] ]) )
            print("Ramp down = %d, %s" % (motor_data[6],ramp_string[ motor_data[6] ]) )
            print("Ramp halt = %d, %s" % (motor_data[7],ramp_string[ motor_data[7] ]) )
         else : 
            f1 = motor_data[3]/256.0
            print("Freq= %.2f" % f1)
   ######
   for rep in range(0,5) : 
     print("get_motor_status 1.0")
     input()
     motor_data = gb.get_motor_config(1,0)
     mode = motor_data[0]
     print("Operating mode:%d, %s" % (mode,mode_string[ mode ]))
     motor_data = gb.get_motor_status(1,0)
     if mode==gb.MODE_BRUSH or (mode & gb.MODE_STEP_MASK) :
        print("Move=%d, %s" % (motor_data[0],movebrush_string[ motor_data[0] ]) )
     if mode & gb.MODE_STEP_MASK : 
        print("%d steps" % motor_data[1] )
   for rep in range(0,5) : 
      print("get_motor_missed 1.0")
      input()
      motor_data = gb.get_motor_missed(1,0)
      print("Missed %d steps" % motor_data[0] )
     

########  
#
# Test baudrate change
#
########  
def test_baudrate() :
   print("Test baudrate change")
   for baud in range(1,4) : 
     # check we can talk now
     version = gb.get_version(board)
     if (version==-1) : 
        print("Can't get version pre baudrate change")
        return
     else:
        print("Pre-set version=%d" % version)        
        print("Set baudrate %d" % baud)
        gb.set_baudrate(baud) 
        version = gb.get_version(board)
        if (version==-1) : 
           print("Can't get version post baudrate change")
           return
        else:
           print("Post set version %d" % version)
   # restore 57.6K baudrate!!!
   print("Restoring 57K6 baudrate")
   gb.set_baudrate(2) 
 

########  
#
# Test Quadrature encoder modes
#
########  
def test_quad():  
   print("Test QUAD modes\n")
   errors = 0
   gb.set_mode(board,chan,gb.MODE_BRUSH);
   for p in range(-8000000, 8000000, 1000000) :
      gb.quad_on(board,chan,1,p,0);
      pos,err = gb.quad_read(board,chan)
      if  pos!=p :
         print("Quad position error set=%d, read pos=%d\n" % (p,pos))
         errors = errors + 1
      if err!=0:
         print("Quad read error set:%d\n" % err)
         errors = errors + 1
  
   if errors!=0 : 
      return
      
   print("Quad set/read test passed")

# temp. skip this test 
##   for t in range (0,3) : 
##     if t==0 :
##        start = 0 
##        dc =  50.0
##     if t==1 :
##        start = 8300000 
##        dc =  75.0
##     if t==2 :
##        start = -8300000 
##        dc =  100.0
##       
##     gb.quad_on(board,chan,1,start,1)
##     print("Quad At %d" % start)
##     for p in range (-5000, 5000, 2500) :
##        print("Goto %d %d% (press return when done) " % ((p+start),dc)) 
##        gb.quad_goto(board,chan,p+start,dc)
##        input()
##    

   gb.quad_on(board,chan,1,0,1);
   print("Quad At 0\n")
   print("Limits: all on, 1000..-1000, 30% @200\n")
  
#int quad_limit(int board,int channel,
#               int max_on, int min_on,int slow_on,
#               int max_pos,int min_pos,
#               int slow_dist,float slow_dc);  
  
   gb.quad_limit(board,chan,1,1,1,1000,-1000,200,30.0)
   print("goto 500 @75 (press return when done)")
   gb.quad_goto(board,chan,500,75.0)
   input()
   print("goto 2000 @100% (press return when done)")
   gb.quad_goto(board,chan,2000,100.0)
   input()
   print("goto 500 @75% (press return when done)")
   gb.quad_goto(board,chan,500,75.0)
   input()
   print("goto 0 @100% (press return when done)")
   gb.quad_goto(board,chan,0,100.0)
   input()
   print("goto -2000 @60%(press return when done)")
   gb.quad_goto(board,chan,-2000,60.0)
   input()
  


      

##########################################################################################
##########################################################################################
##########################################################################################

test = 0
board = 0
chan  = 0
for i in range(len(sys.argv)) :
  if sys.argv[i][0:2]=="-t" : # why 2 ?????
    test = int(sys.argv[i][2:])
  if sys.argv[i][0:2]=="-b" :
    board = int(sys.argv[i][2:])
  if sys.argv[i][0:2]=="-c" :
    chan = int(sys.argv[i][2:])

print("Test=%d  Board=%d  Channel=%d \n" % (test, board, chan))

if test==0 :
   usage() 

print("Running test %d\n" % test)   
gb.open_uart(0)

if test==1  :   test_mode() # 1/10/14 passed (using GUI)
if test==2  :   test_endstop_short() # 18/10/14 passed (using GUI) 
if test==3  :   test_move_brushed() # 1/10/14 passed chan 0 & 2
if test==4  :   test_pwm_brushed()  # 1/10/14 passed
if test==5  :   test_move_stepper() # 1/10/14 passed 
if test==6  :   test_stop_stepper() # 1/10/14 passed
if test==7  :   test_freq_stepper() # 1/10/14 passed
if test==8  :   test_read_error()   # 1/10/14 passed
if test==9  :   test_set_pin_mode() # 1/10/14 passed
if test==10 :   test_set_all_pins() # 1/10/14 passed
if test==11 :   test_set_output()   # 18/10/14 passed
if test==12 :   test_dac_adc()      # 18/10/14 passed
if test==13 :   test_inputs()       # 18/10/14 passed
if test==14 :   test_get_io_setup() # 19/10/14 passed
if test==15 :   test_dcc()          # 19/10/14 send_dcc_mess passed 
if test==16 :   test_get_motor()    # 19/10/14 passed
if test==17 :   test_baudrate()     # 25/04/15 passed for 1,2,3 
if test==18 :   test_quad()         # 25/04/15 passed
if test==19 :   test_endstop2()     # 26/04/15 passed
if test==20 :   test_hotsort()      # 

  
  
  
