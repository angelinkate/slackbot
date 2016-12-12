#-*- coding: utf-8 -*-

# http://joequery.me/guides/python-smtp-authenticationerror/

from slackclient import SlackClient
import time
import json
import smtplib
from email.mime.text import MIMEText

class BotClient(SlackClient):
    @staticmethod
    def makebot(conf):
        return BotClient(conf)

    def __init__(self, conf):
        self._token = conf['token'] if 'token' in conf else None
        self._channel =conf['channel'] if 'channel' in conf else None
        self._keywords = conf['keyword'] if 'keyword' in conf else None
        self._mailto = conf['mailto'] if 'mailto' in conf else None

        SlackClient.__init__(self, self._token)
        return

    def run(self):
        con = self.rtm_connect()
        if con is False:
            return con;
        self._greeting()
        self._loop_infinite()
        return con;

    def _greeting(self):
        self.rtm_send_message(self._channel, "Hello you! I'm going to listen your chat.")
        return

    def _loop_infinite(self):
        while True:
            rdata = self.rtm_read()
            if rdata is None or rdata is '':
                continue
            elif len(rdata) == 0:
                continue
            for data in rdata:
                self._process(data)
            time.sleep(1)

    def _process(self, data):
        if not data or len(data) == 0:
            return
        if not 'type' in data:
            return
        mtype = data['type']
        if mtype != 'message':
            return
        if not 'subtype' in data:
            return
        stype = data['subtype']
        if stype != 'bot_message':
            return

        print self._prettyprint(data)

        text = data['text'] if 'text' in data else None
        attachments = data['attachments'] if 'attachments' in data else None
        trigger = self._check_release(text, attachments=attachments)

        if trigger is None:
            return

        subject = '[Bot] Slack ' + ", ".join(self._keywords)
        trigger = trigger + ("\nFrom #noticeman")

        self._send_mail(subject=subject, content=trigger, mailto=self._mailto)

    def _check_release(self, title, attachments=None):
        if all(i in title for i in self._keywords):
            return title
        if None == attachments or len(attachments) == 0:
            return None
        for element in attachments:
            title = element['title'] if 'title' in element else ''
            if all(i in title for i in self._keywords if i != ''):
                return title
            text = element['text'] if 'text' in element else ''
            if all(i in text for i in self._keywords if i != ''):
                return text
            if not 'fields' in element:
                continue
            fields = element['fields']
            if len(fields) == 0:
                continue
            for field in fields:
                value = field['value'] if 'value' in field else ''
                if not value:
                    continue
                if all(i in value for i in self._keywords if i != ''):
                    return value

        return None

    def _send_mail(self, **data):
        if not 'mailto' in data:
            return

        mailto = data['mailto']
        msg = MIMEText(data['content'], 'plain', 'utf-8')
        msg['Subject'] = data['subject']
        msg['From'] = 'slack bot'
        msg['To'] = ','.join(mailto)

        #print msg.as_string()

        #oops @@
        gmail_user = ''
        gmail_pwd = ''
        #@@

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        server.sendmail('slack bot', mailto, msg.as_string())
        server.quit()

        print "sent a mail >>>"
        return

    def _prettyprint(self, data):
        print json.dumps(data, sort_keys=True, indent=2)