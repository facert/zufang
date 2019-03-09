#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import threading


class WechatBot(WXBot):

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

    def handle_msg_all(self, msg):
        super(WechatBot, self).handle_msg_all(msg)
        
    def schedule(self):
        super(WechatBot, self).schedule()

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
        self.proc_msg()

        t = threading.Thread(target=self.schedule)
        t.setDaemon(True)
        t.start()