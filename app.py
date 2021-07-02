from flask import Flask, render_template, request, redirect, url_for, flash, session
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hahaha'

RESPONSES = []
main_survey = surveys['satisfaction']
all_questions = [question.question for question in main_survey.questions]
answers = [question.choices for question in main_survey.questions]



@app.route('/', methods=['GET'])
def start():
    session.pop('_flashes', None)
    return render_template('start.html', survey=main_survey)


@app.route('/questions/<num>', methods=['GET', 'POST'])
def questions(num):
    new_num = int(num)
    if RESPONSES and new_num != len(RESPONSES) or \
        not RESPONSES and new_num > 0:
        flash('Sorry, you can\'t skip questions!', 'error')
        return redirect(url_for('questions', num=len(RESPONSES) or 0))
    
    if new_num == len(all_questions):
        return redirect(url_for('thanks'))

    if request.method == 'POST':
        if len(RESPONSES) != len(all_questions):
            RESPONSES.append(list(request.form.keys())[0])
        return redirect(url_for('questions', num=new_num+1))
    
    return render_template('questions.html', number=new_num, 
    question=all_questions[new_num], answers=answers[new_num])


@app.route('/thanks', methods=['GET'])
def thanks():
    session.pop('_flashes', None)
    return render_template('thankyou.html')