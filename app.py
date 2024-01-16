from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "2005"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

title = surveys.satisfaction_survey.title
instructions = surveys.satisfaction_survey.instructions

responses = []

amt_of_questions = len(surveys.satisfaction_survey.questions)

current_question = 0

@app.route("/")
def display_homepage():
    return render_template("home.html", title=title, instructions=instructions)



@app.route("/questions/<int:x>")
def display_question(x):
    if x != current_question:
        flash("INVALID ACTION", "error")
        return redirect(f"/questions/{current_question}")
    elif current_question >= amt_of_questions:
        return redirect("/thank-you")
        
    try:
        question = surveys.satisfaction_survey.questions[x].question
        question_choices = surveys.satisfaction_survey.questions[x].choices
    
    except:
        question = surveys.satisfaction_survey.questions[x-1].question
        question_choices = surveys.satisfaction_survey.questions[x-1].choices
        

    return render_template("question.html", question=question, question_choices=question_choices, amt_of_questions=amt_of_questions, current_question=current_question)

@app.route("/questions/next")
def get_next_question():
    global current_question
    try:
        responses.append(request.args["last-question-answer"])
        if amt_of_questions > current_question:
            current_question += 1
    except:
        pass
    if amt_of_questions == current_question:
        return redirect(f"/thank-you")
    return redirect(f"/questions/{current_question}")

@app.route("/thank-you")
def display_thanks():
    if amt_of_questions > current_question:
        flash("INAVLID ACTION", "error")
        return redirect(f"/questions/{current_question}")
    return render_template("thank_you.html")