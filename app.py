from urllib import parse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), '.')
sys.path.append(topdir)

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hahaha'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

main_survey = surveys['satisfaction']
all_questions = [question.question for question in main_survey.questions]
all_answers = [question.choices for question in main_survey.questions]

def parse_number(num):
    if '.' in num:
        num = num[0]
    return abs(int(num))


@app.route('/', methods=['GET', 'POST'])
def start():
    """The main, or home, page of the survey. A POST request
    fires a redirect to a dummy route used to setup session, and
    a GET request renders the template for the start page."""
    session.pop('_flashes', None)

    if request.method == 'POST':
        return redirect(url_for('test'))
    return render_template('start.html', survey=main_survey)


@app.route('/test', methods=['POST'])
def test():
    """A dummy route only used to setup session['responses']
    to an empty list. No GET requests are accepted, because there
    is no template for this route."""
    session['responses'] = []
    return redirect(url_for('questions', num=0))


@app.route('/questions/<num>', methods=['GET', 'POST'])
def questions(num):
    """This route has additional logic to handle scenarios related
    to POST requests. If the length of the session object list is equal
    to the amount of questions, we redirect to the thanks page. If the
    user tries to skip questions, we flash a message and redirect to the
    correct question. This page appends the answer to the session['responses']
    list if there is a POST request, and just renders the page if there is a GET
    request."""
    new_num = parse_number(num)
    responses = session['responses']

    if len(responses) == len(all_questions):
        return redirect(url_for('thanks'))

    if responses and new_num != len(responses) or \
        not responses and new_num > 0:
        flash('Sorry, you can\'t skip questions!', 'error')
        return redirect(url_for('questions', num=len(responses) or 0))

    if request.method == 'POST':
        answers = session['responses']
        response = request.form['radio']
        answers.append(response)
        session['responses'] = answers
        return redirect(url_for('questions', num=new_num+1))
    
    return render_template('questions.html', number=new_num, 
    question=all_questions[new_num], answers=all_answers[new_num])


@app.route('/thanks', methods=['GET'])
def thanks():
    """A simple thank you page. Pops any unflashed messages
    so that they won't be flashed when a user start a new survey."""
    session.pop('_flashes', None)
    return render_template('thankyou.html', questions=all_questions, answers=session['responses'])