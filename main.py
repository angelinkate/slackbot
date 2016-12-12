import sys
from rtmbot import BotClient

global _bot
global _keyword
global _token
global _channel
global _mailto

def run():
    global _bot
    conf = dict(token=_token, channel=_channel, keyword=_keyword, mailto=_mailto)
    _bot = BotClient.makebot(conf)
    _bot.run()

def _usage():
    print "=" * 30
    print 'Usage:'
    print '\tpython main.py token=token channel=channel keyword=keyword,.. mailto=address,..'
    print '\tall options are optional. if some option is not set we use values in slackinfo.'
    print "=" * 30
    return

def init(args):
    import slackinfo
    global _token, _channel, _keyword, _mailto

    if len(args) == 2:
        o = args[1]
        if o == '-h' or o == '-help':
            _usage()
            return

    params = dict(a.split('=') for a in args[1:])

    _token = params['token'] if 'token' in params else slackinfo.TOKEN
    _channel = params['channel'] if 'channel' in params else slackinfo.CHANNEL
    _keyword = params['keyword'] if 'keyword' in params else None
    _mailto = params['mailto'] if 'mailto' in params else None

    if _keyword == None:
        _keyword = slackinfo.KEYWORDS
    else:
        _keyword = list(_keyword.split(','))

    if _mailto == None:
        _mailto = slackinfo.MAILTO
    else:
        _mailto = list(_mailto.split(','))

    if not _token or not _channel:
        print "token and channel may not be empty."
        _usage()
        return

    print "=" * 30
    print "token:", _token
    print "channel:", _channel
    print "keyword:", _keyword
    print "mailto:", _mailto
    print "=" * 30

    run()

if __name__ == '__main__':
    init(sys.argv)


