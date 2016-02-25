from urllib import quote
import hashlib
import base64
import hmac
import random
import string
import time
import collections
import pycurl
import json
import requests

params={}

def SHA(message,secret):
	return hmac.new(secret, msg=message, digestmod=hashlib.sha1).digest()

def genSignature(message,secret):
	digest = SHA(message,secret)
	signature = base64.b64encode(digest).decode()
	return quote(signature,safe='')

def genNonce(length):
	s=string.lowercase+string.digits
	nonce=''.join(random.sample(s,length))
	return nonce

def genTimeStamp():
	timestamp=int(time.time())
	return str(timestamp)

def readFile(filename):
	f=open(filename,'r')
	return f.read()

def genParams(filename):
	fileString=readFile(filename)
	lines=fileString.split('\n')
	for line in lines:
	 	paramsMap=line.split('=')
	 	params[paramsMap[0]]=paramsMap[1]
	params["oauth_nonce"]=genNonce(32)
	# params["oauth_nonce"]="e2734224ae899d5ec98f2374e9d13a31"
	params["oauth_timestamp"]=genTimeStamp()
	# params["oauth_timestamp"]="1456317963"

def genMessage():
	parameterString="oauth_consumer_key="+quote(params["oauth_consumer_key"],safe= '')+"&"
	parameterString=parameterString+"oauth_nonce="+quote(params["oauth_nonce"],safe= '')+"&"
	# parameterString=parameterString+"oauth_nonce="+"8239d07dc7c48e4c93d32876fa797601"+"&"
	parameterString=parameterString+"oauth_signature_method="+quote(params["oauth_signature_method"],safe= '')+"&"
	parameterString=parameterString+"oauth_timestamp="+quote(params["oauth_timestamp"],safe= '')+"&"
	# parameterString=parameterString+"oauth_timestamp="+"1456308387"+"&"
	parameterString=parameterString+"oauth_token="+quote(params["oauth_token"],safe= '')+"&"
	parameterString=parameterString+"oauth_version="+quote(params["oauth_version"],safe= '')+"&"
	parameterString=parameterString+"status="+quote(params["status"],safe= '')
	message=params["httpMethod"]+"&"+quote(params["baseUrl"], safe='')+"&"+quote(parameterString, safe='')
	return message

def genSecret():
	secret=params["oauth_consumer_secret"]+"&"+params["oauth_token_secret"]
	return secret

genParams('twitterParams.txt')
message=genMessage()
secret=genSecret()
params["oauth_signature"]=genSignature(message,secret)
# print params
#send request (Header Info) to server 

def buildCurl():
	import os
	command="curl"
	command=command+" --request \'"+params["httpMethod"]+"\' "
	command=command+"\'"+params["baseUrl"]+"\' "
	command=command+"--data \'"+"status="+params["status"].replace(" ","+")+"\' "
	command=command+"--header \'"+"Authorization: OAuth "
	command=command+"oauth_consumer_key=\""+params["oauth_consumer_key"]+"\", "
	command=command+"oauth_nonce=\""+params["oauth_nonce"]+"\", "
	command=command+"oauth_signature=\""+params["oauth_signature"]+"\", "
	command=command+"oauth_signature_method=\""+params["oauth_signature_method"]+"\", "
	command=command+"oauth_timestamp=\""+params["oauth_timestamp"]+"\", "
	command=command+"oauth_token=\""+params["oauth_token"]+"\", "
	command=command+"oauth_version=\""+params["oauth_version"]+"\"\' "
	command=command+"--verbose "
	print command
	os.system(command)

# getCurl()

buildCurl()