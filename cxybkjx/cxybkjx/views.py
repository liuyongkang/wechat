from django.http import HttpResponse
from django.template import RequestContext, Template
from django.utils.encoding import smart_str, smart_unicode
from django.views.decorators.csrf import csrf_exempt

import hashlib
import xml.etree.ElementTree as ET
import time

TOKEN = 'mshl'

@csrf_exempt
def handleRequest(request) :
    if request.method == 'GET' :
        response = HttpResponse(checkSignature(request), content_type = 'text/plain')
        return response
    elif request.method == 'POST' :
        response = HttpResponse(responseMsg(request), content_type = 'application/xml')
        return response
    else :
        return None

def responseMsg(request) :
    s = smart_str(request.raw_post_data)
    root = ET.fromstring(s)
    xml = {}
    if root.tag == 'xml' :
        for child in root :
            xml[child.tag] = smart_str(child.text)

    msgType = xml.get('MsgType')
    content = xml.get('Content')

    res = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    res = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), xml['MsgType'], xml['Content'])

    return res


def checkSignature(request) :
    global TOKEN

    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echoStr = request.GET.get('echostr')

    token = TOKEN
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpStr = "%s%s%s" % tuple(tmpList)
    tmpStr = hashlib.sha1(tmpStr).hexdigest()

    if tmpStr == signature :
        return echoStr
    else :
        return None

