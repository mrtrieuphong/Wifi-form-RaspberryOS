#by nguyentrieuphong
#follow me on nguyentrieuphong.com

from requests import get
import requests
import json
import os, sys
from flask import Flask, request, render_template, jsonify
from subprocess import check_output

global wifi_ID, wifi_PW
app = Flask(__name__)
def do_something(idp, pwp):
   ssid = idp
   password = pwp
   f = open('wpa_supplicant.conf', 'w')
   f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
   f.write('update_config=0\n')
   f.write('country=VN\n')
   f.write('network={\n')
   f.write('ssid=' + '"' + ssid + '"\n')
   f.write('psk=' + '"' + password + '"\n')
   f.write('key_mgmt=WPA-PSK\n')
   f.write('priority=1\n')
   f.write('}\n')
   f.close()
   os.system('sudo cp /home/pi/Phong_van/wpa_supplicant.conf /etc/wpa_supplicant')
   #os.system('reboot')
   os.system('sudo wpa_cli -i wlan0 reconfigure')   

@app.route('/')
def home():   
    scanoutput = check_output("iwgetid -r", shell = True)
    ssid = scanoutput.decode()
    wifi_ID = ssid
    wifi_PW = "********"
    return render_template('index.html', wifi_id= wifi_ID, wifi_pass= wifi_PW)

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    idp = request.form['idp']
    pwp = request.form['pwp']
    do_something(idp, pwp)
    result = {
       "output": idp + pwp }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)