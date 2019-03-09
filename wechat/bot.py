#!/usr/bin/env python
# coding: utf-8
import time
from wxbot import *
import sys
import redis
import datetime
import threading


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search.whoosh.query import zufang_query


def get_redis():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    return redis.StrictRedis(connection_pool=pool)

redis = get_redis()


class ZufangWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.robot_switch = True
        # self.contact_schedule_dict = {}

    def get_user_id_by_alias(self, name):
        if name == '':
            return None
        name = self.to_unicode(name)
        for contact in self.contact_list:
            if 'Alias' in contact and contact['Alias'] == name:
                return contact['UserName']
        return ''

    def get_name_by_user_id(self, user_id):
        for account in self.contact_list:
            if user_id == account['UserName']:
                return account['Alias']
        return False

    def run(self):
        self.get_uuid()
        self.gen_qr_code(os.path.join(self.temp_pwd,'wxqr.png'))
        print '[INFO] Please use WeChat to scan the QR code .'

        result = self.wait4login()
        if result != SUCCESS:
            print '[ERROR] Web WeChat login failed. failed code=%s' % (result,)
            return

        if self.login():
            print '[INFO] Web WeChat login succeed .'
        else:
            print '[ERROR] Web WeChat login failed .'
            return

        if self.init():
            print '[INFO] Web WeChat init succeed .'
        else:
            print '[INFO] Web WeChat init failed'
            return
        self.status_notify()
        if self.get_contact():
            print '[INFO] Get %d contacts' % len(self.contact_list)
            print '[INFO] Start to process messages .'

        t = threading.Thread(target=self.schedule)
        t.setDaemon(True)
        t.start()
        self.proc_msg()

    def auto_reply(self, uid, msg, msg_from='self'):
        results = zufang_query(' OR '.join(msg.strip().split(' ')), limit=15)
        result_list = []
        for result in results:
            result_list.append('\n%s\n%s\n%s\n====================\n' % (result['title'].strip(), result['url'], result['create_time']))
        # user_id = uid.replace('@', '')[:30]
        reply_content = ''.join(result_list) if result_list else u'暂时没有【%s】 房源哦' % msg
        if msg_from == 'contact':
            append_content = u'\n（由于机器人受微信限制，所以请客官关注公众号【嗅房】使用功能）输入 start 可设置定时推送，stop 关闭定时推送，多个关键词请用空格隔开， 如 【望京 酒仙桥】,如果有问题，请向公众号【嗅房】反馈'
        elif msg_from == 'group':
            append_content = u'\n如需更多功能，请添加机器人好友或者关注公众号【嗅房】（由于机器人受微信限制，所以请客官关注公众号【嗅房】使用功能）'
        else:
            append_content = ''
        reply_content = reply_content+append_content
        return reply_content

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            is_schedule_auto_switch_cmd, flag = self.is_schedule_auto_switch_cmd(msg)
            if is_schedule_auto_switch_cmd:
                self.schedule_auto_switch(msg, flag)
            else:
                if self.is_schedule_status_open(msg):
                    name = self.get_name_by_user_id(msg['user']['id'])
                    redis.hset('schedule', name, msg['content']['data'])
                    # self.contact_schedule_dict[msg['user']['id']] = msg['content']['data']
                self.send_msg_by_uid(self.auto_reply(msg['user']['id'], msg['content']['data'], msg_from='contact'), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(msg['user']['id'], self.my_account['UserName'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.auto_reply(msg['content']['user']['id'], msg['content']['desc'], msg_from='group')
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])

    def is_schedule_status_open(self, msg):
        name = self.get_name_by_user_id(msg['user']['id'])
        status = redis.hget('schedule', name)
        status = True if status != '0' else False
        return status
        # return self.contact_schedule_dict.get(msg['user']['id'], False)

    def is_schedule_auto_switch_cmd(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = ['stop']
        start_cmd = ['start']
        is_schedule_auto_switch_cmd = True if msg_data in list(stop_cmd+start_cmd) else False
        flag = False

        for i in stop_cmd:
            if i == msg_data:
                name = self.get_name_by_user_id(msg['user']['id'])
                redis.hset('schedule', name, 0)
                # self.contact_schedule_dict[msg['user']['id']] = False
                flag = False

        for i in start_cmd:
            if i == msg_data:
                name = self.get_name_by_user_id(msg['user']['id'])
                redis.hset('schedule', name, 1)
                # self.contact_schedule_dict[msg['user']['id']] = True
                flag = True

        return is_schedule_auto_switch_cmd, flag

    def schedule_auto_switch(self, msg, flag):
        if flag:
            self.send_msg_by_uid(u'输入多个关键词【如"望京 酒仙桥"】开启定时推送（6小时推送一次）', msg['user']['id'])
        else:
            self.send_msg_by_uid(u'定时推送服务关闭，谢谢使用', msg['user']['id'])

    def schedule(self):
        while True:
            time.sleep(60*60)
            for name, value in redis.hgetall('schedule').items():
                user_id = self.get_user_id_by_alias(name)
                if user_id and value not in ['1', '0'] and datetime.datetime.now().hour in [9, 15, 21]:
                    self.send_msg_by_uid(self.auto_reply(user_id, value.decode('utf-8'), msg_from='contact'), user_id)


def main():
    bot = ZufangWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'

    bot.run()


if __name__ == '__main__':
    main()

