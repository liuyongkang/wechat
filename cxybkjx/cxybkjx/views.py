from django.http import HttpResponse
from django.template import RequestContext, Template

import hashlib

TOKEN = 'mshl'

def index(request) :
    if request.method == 'GET' :
        response = HttpResponse(checkSignature(request))
    else :
        response = HttpREsponse('hello world')

    return response

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

