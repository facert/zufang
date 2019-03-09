# coding: utf-8
# import morse_talk as mtalk
from flask import Flask, jsonify
from flask_weixin import Weixin
from flask import render_template, request
import sys
import os
from urllib import quote
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search.whoosh.query import zufang_query

app = Flask(__name__)
app.config['WEIXIN_TOKEN'] = 'zufang'


@app.route('/')
def hello_world():
    keywords = request.args.get('keywords')
    keywords = keywords if keywords else u'望京'
    results = zufang_query(' OR '.join(keywords.strip().split(' ')))
    return render_template('renting.html', results=results, keywords=keywords)



weixin = Weixin(app)
app.add_url_rule('/wechat', view_func=weixin.view_func)


@weixin.register(type='event', event='subscribe')
def send_welcome(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    return weixin.reply(username, sender=sender, content='谢谢关注，请输入需要查询的关键词')


@weixin('*')
def reply_all(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
    results = zufang_query(' OR '.join(content.strip().split(' ')), limit=6)
    result_list = []
    if results:
        for result in results:
            result_list.append('<a href="%s">%s</a>\n%s\n====================\n' % (result['url'], result['title'].strip(), result['create_time']))
        result_list.append('<a href="http://zufang.ngrok.cc/?keywords=%s">%s</a>' % (quote(content.encode('utf-8')), u'更多【%s】租房请点击这里' % content))
    else:
        result_list = [u'暂时没有【%s】房源哦' % content]
    return weixin.reply(username, sender=sender, content=''.join(result_list))

   
if __name__ == '__main__':
    # you need a proxy to serve it on 80
    # app.run('0.0.0.0', 5000)
    app.run()
