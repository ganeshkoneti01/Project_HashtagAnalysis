from bottle import run,route,get,post,request,template,static_file
from twarc import Twarc
import pandas as pd
t=Twarc("OGh7cQ6tLezofTRc1r2Gk38Mo","Jl7XxuagDALyOYQqbbl0M32uDE8f3gAKau8RHpIB21d5EZoWqU","1136145916929253376-diwYTpirtPvj6bMc6mmVQJRnd9Rg8W","ASvr17ddDe3jpK6M5TKDcpEtYBGomIq1YetIcEdmtwi7I")										        
twdata = None
@route("/<hashtag>")
def search(has):
	global twdata,data2,data4,data6
	c=0
	news=[]
	for tweet in t.search(has):
		tweet['followers_count'] = tweet['user']['followers_count']
		news.append(tweet)
		if c>100:
			break
		c=c+1
	data = pd.DataFrame(news)
	data['favorite_count'] = data['favorite_count'].apply(pd.to_numeric)
	data = data.sort_values(by='favorite_count', ascending=False)
	twdata = data
	data1 = data.sort_values(by='followers_count', ascending=False)
	data2 = data1
	data3 = data.sort_values(by='retweet_count', ascending=False)
	data4 = data3
	data5 = data.sort_values(by='full_text', ascending=False)
	data6 = data5
	return template('temp', data=twdata)
@route('/favs')
def favs():
	global twdata
	count = twdata.sort_values(by='favorite_count',ascending=False)
	return template('favs',data=twdata)
@route('/user')
def user():
	global data2
	user = twdata.sort_values(by='followers_count',ascending=False)
	return template('favs',data=data2)
@route('/retweets')
def retweets():
	global data4
	user = twdata.sort_values(by='retweet_count',ascending=False)
	return template('favs',data=data4)
@route('/fulltext')
def fulltext(): 											
	global data6
	user = twdata.sort_values(by='full_text',ascending=False)
	return template('favs',data=data6)
@get("/proj")
def hello():
	return template("proj", data=twdata)
@post("/get_details")
def do_get():
	has=request.forms.get("hashtag")
	return search(has)
run(host="localhost",reloader="True",port="8003")

