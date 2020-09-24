import scapy.all as scapy
from mac_vendor_lookup import MacLookup, BaseMacLookup
from twilio.rest import Client
from secrets import *
from datetime import datetime
import time
import os 

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

if 'VIRTUAL_ENV' in os.environ.keys():
    BaseMacLookup.cache_path = os.environ['VIRTUAL_ENV'] + '/cache/mac-vendors.txt' 

mac = MacLookup()
# mac.update_vendors()

def send_message(message):
    response = twilio_client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=YOUR_NUMBER)
    if response.sid:
        return True
    else:
        return False

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for item in answered_list:
        client_dict = {
            "ip": item[1].psrc, 
            "mac": item[1].hwsrc
        }
        try:
            client_dict["vendor"] = mac.lookup(item[1].hwsrc)
        except:
            client_dict["vendor"] = "Generic"
        clients_list.append(join_data(client_dict))
    return clients_list

def join_data(device):
    for item in WHITE_LIST:
        if item["mac"].lower() == device["mac"].lower():
            copy = device.copy()
            del copy["mac"]
            return {**copy, **item}
    return device

def detect_intruder(devices):
    intruders = []
    for device in devices:
        if device["mac"] in [item["mac"] for item in WHITE_LIST]:
            print(device)
        else:
            print('intruso', device)
            intruders.append(device)
    return intruders

def write_text(text):
    text = text +'\n'
    if os.path.exists('./intruders.txt'):
        intruder_text =  open('./intruders.txt', 'a+')
    else:
        intruder_text =  open('./intruders.txt', 'w+')
    intruder_text.write(text)
    intruder_text.close()

def parse_dictionary(item):
    text = ''
    for key in item.keys():
        text += '{}: {}\n'.format(key, item[key])
    return text

if __name__ == "__main__":
    while True:
        intruders = detect_intruder(scan(YOUR_NETWORK))
        message = 'Intruders detected!\n\n'
        if len(intruders) > 0:
            write_text('\n\n---> Timestamp: {}'.format(datetime.now()))
            for intruder in intruders:
                message += 'mac: {}\nvendor: {}\n\n'.format(intruder['mac'], intruder['vendor'])
                write_text(parse_dictionary(intruder))
            # if send_message(message):
            #     print('message send!')
        print('sleep .zZ for {} minutes'.format(TIME_MIN))
        time.sleep(TIME_MIN * 60)