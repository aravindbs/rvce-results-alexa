import logging, yaml, json
from flask import Flask, render_template, request, session as flaskSession
from flask_ask import Ask, statement, question, session
from scraper import get_result
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def index() :
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent('usn', mapping = { 'year' : 'year',  'department' : 'department', 'number' : 'number'}) 
def getRes(year, department, number):

    YEAR = "%02d"%int(year)
    DEPT = department
    NUM = "%03d"%int(number)
    usn = "1RV{}{}{}".format(YEAR, DEPT, NUM)

    result = get_result (usn)

    if (result == "400") :
        notFound = render_template("notFound", usn = usn)
        return statement (notFound).simple_card(title='Not Found', content= "Result Not Found for {}".format(usn))

    else:
        Found = render_template("found", result = result)
        card_content = BeautifulSoup(Found)
        return statement (Found).simple_card(title=result["sgpa"], content= card_content.text)

@app.route('/status', methods = ['GET', 'POST'])
def status():
    return "running"

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
 
    


