import os;
import sqlite3;
import time;
import requests;
import subprocess;
import threading;
_db_address = '/etc/x-ui/x-ui.db'
_max_allowed_connections = 1
def getUsers():
    conn = sqlite3.connect(_db_address)
    cursor = conn.execute("select remark,port from inbounds");
    users_list = [];
    for c in cursor:
        users_list.append({'name':c[0],'port':c[1]})
    conn.close();
    return users_list

def disableAccount(user_port):
    conn = sqlite3.connect(_db_address) 
    conn.execute("update inbounds set enable = 0 where port="+str(user_port));
    conn.commit()
    conn.close();
    time.sleep(2)
    os.popen("x-ui restart")
    time.sleep(3)
    
class AccessChecker(threading.Thread):
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user;
    def run(self):
        while True:
            user_remark = self.user['name'];
            user_port = self.user['port'];
            netstate_data =  os.popen("netstat -np 2>/dev/null | grep :"+str(user_port)+" | awk '{if($3!=0) print $5;}' | cut -d: -f1 | sort | uniq -c | sort -nr | head").read();
            netstate_data = str(netstate_data)
            connection_count =  len(netstate_data.split("\n")) - 1;
            print("c "+str(user_port) + "-"+ str(connection_count))
            if connection_count > _max_allowed_connections:
                requests.get('https://api.telegram.org/[bot_token]/sendMessage?chat_id=[chat_id]&text='+user_remark+'%20locked')
                disableAccount(user_port=user_port)
                print("inbound with port " + str(user_port) + " blocked")
            else:
                time.sleep(2)


users_list = getUsers();
for user in users_list:
    thread = AccessChecker(user)
    thread.start()
