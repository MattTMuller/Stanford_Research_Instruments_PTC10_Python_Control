# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:38:37 2022

@author: Microprobe_Station
"""

import socket
import smtplib
import time
import telnetlib



# # Prepare 3-byte control message for transmission
# HOST = '169.254.106.220'
# tn = telnetlib.Telnet(HOST, port= 23, timeout=20)


# command = input('Enter command: ') + "\r\n"
# tn.write(command.encode('ascii'))
# #ret1 = tn.read_until(b'\r\n').decode('ascii')
# #print(ret1)
# MESSAGE = 'POWER.PID.setpoint = 20' # Relays 1 permanent off

# tn.close()



class PTC10:
    def __init__(self, host_IP, port = 23, timeout=20):
        self.tn = telnetlib.Telnet(host=host_IP, port=port, timeout=timeout)
        self._variable_names = self.get_variable_names()
        self._power_variable_name = self._variable_names[0]
        self._temperature_variable_name = self._variable_names[2]
        
    def __del__(self):
        self.tn.close()
        
    def _send_command(self, command):
        message = command + "\r\n"
        self.tn.write(message.encode())
        
    def _retrieve_data(self):
        return self.tn.read_until(b'\r\n').decode('ascii')
    
    def get_variable_names(self):
        self._send_command('getOutput.names')
        names_as_string = self._retrieve_data()
        names_as_list = names_as_string.split(',')
        return names_as_list
        
    def get_outputs(self):
        self._send_command('getOutputs')
        outputs_as_sting = self._retrieve_data()
        outputs_as_float = [float(val) for val in outputs_as_sting.split(',')]
        return outputs_as_float
        
    def enable_PID(self):
        command = self._power_variable_name + ".PID.mode = on"
        self._send_command(command)
        
    def disable_PID(self):
        command = self._power_variable_name + ".PID.mode = off"
        self._send_command(command)
        
    def temperature_setpoint(self, setpoint):
        command = self._power_variable_name + f".PID.setpoint = {setpoint}"
        self._send_command(command)
        
    def set_power(self, power):
        """power value set by this function
        will be overwritten by PID if PID is still enabled"""
        command = self._power_variable_name + f".value = {power}"
        self._send_command(command)
        
        
    def enable_output(self):
        self._send_command('outputEnable on')
    
    def disable_output(self):
        self._send_command('outputEnable off')


#controller = PTC10('169.254.106.220')
#controller.temperature_setpoint(20)
#del controller
 
def driver():
    controller = PTC10('169.254.106.220')
    #controller.temperature_setpoint()
    controller.disable_PID()
    controller.set_power(10)
    
driver()
   
"""







"""