# SMK_dataAcquire
use python to acquire IEMG signal from SMK 32ch mask

how to use it:
1. from smk import *
2. you can send command by "smk.send_data(command)", command can reference to below:
setting: "AT+EMGCONFIG=FFFFFFFF,2000\r\n" 
check setting: "AT+EMGCONFIG?\r\n"
start IEMG: "AT+IEMGSTRT\r\n"
triger: "AT+TRIGER=1\r\n"
stop: "AT+STOP\r\n"
check version: "AT+SWVER?\r\n"            
3. you can check the feedback from smk by "smk.read_data()".
4. if you want to acquire IEMG signal, you can type "smk.IEMG()"
5. after acquire all of the data, just use ctrl+c to do KeyboardInterrupt, the data
will be saved automatically.
6. use smk.port_open() or smk.port_close() to connect or disconnect the port.
