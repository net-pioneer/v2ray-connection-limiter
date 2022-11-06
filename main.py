import os
import sqlite3
import time
import requests
import threading
import schedule
import logging
import argparse

logger = logging.getLogger('x-ui')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

user_last_id = 0

def getUsers(db_address):
    global user_last_id
    conn = sqlite3.connect(db_address)
    cursor = conn.execute(f"select id,remark,port from inbounds where id > {user_last_id}")
    users_list = list()
    for c in cursor:
        users_list.append({'name':c[1],'port':c[2]})
        user_last_id = c[0]
    conn.close()
    return users_list

def disableAccount(user_port, db_address):
    conn = sqlite3.connect(db_address) 
    conn.execute(f"update inbounds set enable = 0 where port={user_port}")
    conn.commit()
    conn.close()
    time.sleep(2)
    os.popen("x-ui restart")
    time.sleep(3)
    
def checkNewUsers(db_address):
    conn = sqlite3.connect(db_address)
    cursor = conn.execute(f"select count(*) from inbounds WHERE id > {user_last_id}")
    new_counts = cursor.fetchone()[0]
    conn.close()
    if new_counts > 0:
        init(args)

def init(args):
    for user in getUsers(args.db_address):
        thread = AccessChecker(user, args)
        thread.start()
        logger.info(f"starting checker for : {user['name']}")


class AccessChecker(threading.Thread):
    def __init__(self, user, args):
        threading.Thread.__init__(self)
        self.user = user
        self.max_allowed_connections = args.max_allowed_connections
        self.telegram_bot_token = args.telegram_bot_token
        self.telegram_channel_id = args.telegram_channel_id
        self.db_address = args.db_address
        self.user_check_interval = args.user_check_interval

    def run(self):
        user_remark = self.user['name']
        user_port = self.user['port']
        while True:
            netstate_msg = f"netstat -np 2>/dev/null | grep :{user_port} |"
            netstate_msg += " awk '{if($3!=0) print $5;}' | cut -d: -f1 | sort | uniq -c | sort -nr | head"
            netstate_data =  os.popen(netstate_msg).read()
            netstate_data = str(netstate_data)
            connection_count =  len(netstate_data.split("\n")) - 1
            if connection_count > self.max_allowed_connections:
                disableAccount(user_port, self.db_address)
                self.max_connections[user_remark] = connection_count
                logger.info(f"inbound {user_remark} with port {user_port} and {connection_count} connections was blocked!")
                if self.telegram_channel_id is not None and self.telegram_bot_token is not None:
                    msg = 'https://api.telegram.org/bot'
                    msg += self.telegram_bot_token
                    msg += '/sendMessage?chat_id='
                    msg += self.telegram_channel_id
                    msg += '&text='
                    msg += f'{user_remark} has {connection_count} connections and will be locked'.replace(' ', '%20')
                    requests.get(msg)
            else:
                time.sleep(self.user_check_interval)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument('--db-address', default='/etc/x-ui/x-ui.db', help='database path')
    parser.add_argument('--max-allowed-connections', type=int, default=1, help='maximum allowed connection')
    parser.add_argument('--newuser-check-interval', type=int, default=60, help='minutes')
    parser.add_argument('--user-check-interval', type=int, default=60, help='seconds')
    parser.add_argument('--telegram-bot-token', type=str, default=None, help='telegram bot token')
    parser.add_argument('--telegram-channel-id', type=str, default=None, help='telegram channel id: has to be a public channel')
   
    args = parser.parse_args()

    init(args)
    schedule.every(args.newuser_check_interval).minutes.do(checkNewUsers, args.db_address)
    while True:
        schedule.run_pending()
        time.sleep(1)
