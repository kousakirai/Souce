from flask import *
import psutil
import feedparser
import os
from os import listdir
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import discord
from flask_xcaptcha import XCaptcha
import requests
import json
'''
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
'''#許可次第でやる(まあサイトかな〜)
from threading import Thread

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per hour"])
HCAPTCHA_SITE_KEY = os.getenv("sitekey")
HCAPTCHA_SECRET_KEY = os.getenv("secretkey")
app.config['XCAPTCHA_SITE_KEY'] = HCAPTCHA_SITE_KEY
app.config['XCAPTCHA_SECRET_KEY'] = HCAPTCHA_SECRET_KEY
app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"
xcaptcha = XCaptcha(app=app)

with open("auth.json", mode="r") as f:
    auth = json.load(f)

def verify(user_id):
  rjson={
    "user_id": user_id
  }
  main_content = {
    "content": json.dumps(rjson)
  }
  requests.post(os.getenv("webhook_url"), main_content)

@app.route('/')
def main():
	return render_template("index.html")

@app.route("/captcha",methods=["POST","GET"])
def captcha():
  with open("auth.json", mode="r") as f:
    auth = json.load(f)
  _id=request.args.get('id')
  if _id in auth["auth"]:
    if request.method == "GET":
      return render_template("verify.html",id2=_id)
    elif request.method == "POST":
      if xcaptcha.verify():
        userid=auth["auth"][_id]
        verify(userid)
        return render_template("verifed.html")
      else:
        return render_template("verify.html",id2=_id)

@app.route("/test")
def test():
  return redirect('https://www.google.com')

@app.route("/news")
def news_main():
  return render_template("news.html")

@app.route("/news/nhk")
def news_nhk():
  d = feedparser.parse("https://www.nhk.or.jp/rss/news/cat0.xml")
  return render_template("nhk.html", e_title=d.entries)

@app.route("/news/yahoo")
def news_yahoo():
  d = feedparser.parse("https://news.yahoo.co.jp/rss/categories/domestic.xml")
  return render_template("yahoo.html", e_title=d.entries)
  
@app.route("/help")
def help():
  return render_template("help.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/form")
def form():
  return render_template("form.html")
  
@app.route("/status")
def status():
  return render_template("status.html",cpu=psutil.cpu_percent(interval=1), memory=psutil.cpu_percent(interval=1),disk=psutil.disk_usage('/').percent)
  
@app.route("/diary")
def diary():
  return render_template("diary.html",m=listdir("diary"))
  
def run():
	app.run(host="0.0.0.0", port=8080)


def keep_alive():
	server = Thread(target=run)
	server.start()