#!/usr/bin/python3
# -*-coding: utf-8 -*-
"""
written by @QIN ZIXUAN
2019/10/31
qin.z.aa@m.titech.ac.jp
Tokyo Institute of Technology
=====================================================================================
how to use it:
1. from smk import *
2. you can send command by "smk.send_data(command)", command can reference to below:
| setting: AT+EMGCONFIG=FFFFFFFF,2000\r\n |
| check setting: AT+EMGCONFIG?\r\n        |
| start IEMG: AT+IEMGSTRT\r\n             |
| triger: AT+TRIGER=1\r\n                 |
| stop: AT+STOP\r\n                       |
| check version: AT+SWVER?\r\n            |
3. you can check the feedback from smk by "smk.read_data()".
4. if you want to acquire IEMG signal, you can type "smk.IEMG()"
5. after acquire all of the data, just use ctrl+c to do KeyboardInterrupt, the data
will be saved automatically.
6. use smk.port_open() or smk.port_close() to connect or disconnect the port.
======================================================================================
"""

import serial
from datetime import datetime
import numpy as np
#import csv
from pylsl import StreamInfo, StreamOutlet

# open serial
class SerialPort:
    def __init__(self, port, baud):
        self.port = serial.Serial(port, baud)
        self.lsl = False
        self.outlet = None
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()

    def send_data(self, command):
        self.port.write(command.encode())

    def read_data(self):
        data = self.port.readline()
        return data

    def IEMG(self):
        feedback = []
        
        self.port.write("AT+IEMGSTRT\r\n".encode())
        print("Start to acquire IEMG signal\n")
        self.start_lsl()
        #name = ['seq', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10',
        #        'ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20',
        #        'ch21', 'ch22', 'ch23', 'ch24', 'ch25', 'ch26', 'ch27', 'ch28', 'ch29', 'ch30',
        #        'ch31', 'ch32', 'Tri1', 'Tri2', 'Tri3']
        #csv_writer.writerow(name)

        try:
            while True:
                count = self.port.inWaiting()
                if count > 0:
                    answer = self.port.read(count)
                    data = []
                    for i in range(len(answer)):
                        data.append(answer[i])
                    data = np.hstack((feedback, data))
                    feedback = self.save(data, 0x71)
                    # self.save(data, 0x71)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.port.write("AT+STOP\r\n".encode())
        print("Stop Successfully!\n")

    def start_lsl(self):
        self.outlet = StreamOutlet(StreamInfo('SMK Array EMG system', 'EMG', 35, 100, 'int16', 'mysmk'))
        self.lsl = True

    def save(self, data, id):
        data_len = len(data)

        i = 0
        while (i < data_len - 1):
            if data[i] == id and i + 70 <= data_len:
                data_set = data[i:i + 70]
                # seq = data_set[1] * 256 + data_set[2]
                iemg = data_set[3:67]
                trigger = []
                trigger.append(data_set[67])
                trigger.append(data_set[68])
                trigger.append(data_set[69])
                iemg_value = []
                for j, k in zip(iemg[0::2], iemg[1::2]):
                    iemg_value.append(j * 256 + k)

                DATA = np.hstack((iemg_value, trigger))
                DATA_str = list(map(lambda x: str(x), DATA))

                if trigger[0] == 0 and trigger[1] == 0 and trigger[2] == 0:
                    print(DATA)
                    try:
                        # csv_writer.writerow(DATA_str)
                        if self.lsl:
                            self.outlet.push_sample(DATA)
                    except Exception as e:
                        raise e

                i = i + 70
            elif data[i] == id and i + 70 > data_len:
                return data[i:data_len]
            else:
                i = i + 1

# port information
serialPort = 'COM4'
baudRate = 460800

# parameters
is_exit = False
id = 0

# file information
#trial = input('trial:')
#filename = "trial_" + trial + "_IEMG.csv"
#dt = datetime.now()
#nowtime_str = dt.strftime('%y-%m-%d')
#filename = nowtime_str + '_' + filename
#path = 'D:/QIN/My_Experiment/data/smk' + '/' + filename
#out = open(path, 'w', encoding='utf8', newline='')
#csv_writer = csv.writer(out)

# port setting
smk = SerialPort(serialPort, baudRate)
smk.send_data("AT+EMGCONFIG=FFFFFFFF,250\r\n")

