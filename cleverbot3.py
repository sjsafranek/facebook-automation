#!/usr/bin/python

import urllib.request
import hashlib
import re
import html.parser
import http.cookiejar

class ServerFullError(Exception):
        pass

ReplyFlagsRE = re.compile('<INPUT NAME=(.+?) TYPE=(.+?) VALUE="(.*?)">', re.IGNORECASE | re.MULTILINE)

class Session(object):
        keylist=['stimulus','start','sessionid','vText8','vText7','vText6','vText5','vText4','vText3','vText2','icognoid','icognocheck','prevref','emotionaloutput','emotionalhistory','asbotname','ttsvoice','typing','lineref','fno','sub','islearning','cleanslate']
        arglist=['','y','','','','','','','','','wsf','','','','','','','','','0','Say','1','false']
        MsgList=[]

        def __init__(self):
                self.cj = http.cookiejar.CookieJar()
                self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
                urllib.request.install_opener(self.opener)
                urllib.request.urlopen("http://www.cleverbot.com")
                
        def Send(self):
                data=encode(self.keylist,self.arglist)
                digest_txt=data[9:35].encode('utf-8')
                hash=hashlib.md5(digest_txt).hexdigest()
                self.arglist[self.keylist.index('icognocheck')]=hash
                data=encode(self.keylist,self.arglist)
                binary_data = data.encode('utf-8') 
                req = urllib.request.Request("http://www.cleverbot.com/webservicemin", binary_data)
                with urllib.request.urlopen(req,None,5000) as url:
                	reply=url.read()
                return reply

        def Ask(self,q):
                self.arglist[self.keylist.index('stimulus')]=q
                if self.MsgList: self.arglist[self.keylist.index('lineref')]='!0'+str(len(self.MsgList)/2)
                asw=self.Send()
                self.MsgList.append(q)
                answer = parseAnswers(asw)
                for k,v in answer.items():
                        try:
                                self.arglist[self.keylist.index(k)] = v
                        except ValueError:
                                pass
                self.arglist[self.keylist.index('emotionaloutput')]=''
                text = answer['ttsText']
                self.MsgList.append(text)
                h = html.parser.HTMLParser()
                text = h.unescape(text)
                return text

def parseAnswers(text):
        d = {}
        keys = ["text", "sessionid", "logurl", "vText8", "vText7", "vText6", "vText5", "vText4", "vText3",
                        "vText2", "prevref", "foo", "emotionalhistory", "ttsLocMP3", "ttsLocTXT",
                        "ttsLocTXT3", "ttsText", "lineRef", "lineURL", "linePOST", "lineChoices",
                        "lineChoicesAbbrev", "typingData", "divert"]
        text = str(text, 'utf-8')
        values = text.split("\r")
        i = 0
        for key in keys:
                d[key] = values[i]
                i += 1
        return d

def encode(keylist,arglist):
        text=''
        for i in range(len(keylist)):
                k=keylist[i]; v=quote(arglist[i])
                text+='&'+k+'='+v
        text=text[1:]
        return text

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')
def quote(s, safe = '/'):   #quote('abc def') -> 'abc%20def'
        safe += always_safe
        safe_map = {}
        for i in range(256):
                c = chr(i)
                safe_map[c] = (c in safe) and c or  ('%%%02X' % i)
        res = map(safe_map.__getitem__, s)
        return ''.join(res)


def main():
        import sys
        cb = Session()

        q = ''
        while q != 'bye':
                try:
                        q = input("> ")
                except KeyboardInterrupt:
                        print
                        sys.exit()
                print(cb.Ask(q))

if __name__ == "__main__":
        main()
