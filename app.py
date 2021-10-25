from flask import Flask, session, request, render_template, redirect, make_response, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

# from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_survey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# Step Two: The Start Page
responses = []

# Home Page show the surveys to choose from
@app.route('/')
def home_page():
    return render_template("start_survey.html", surveys=surveys.values())

@app.route('/survey', methods=["POST"])
def choose_survey():
    survey_id = request.form["survey_id"]
    # survey_id = request.args["survey_id"]
    survey = surveys[survey_id]
    session['current_survey'] = survey_id

    return render_template("base.html", survey=survey)
    # return render_template('base.html', survey=survey)


# @app.route('/')
# def home_page():
#     return render_template("base.html", survey=survey)

@app.route('/begin', methods=["POST"])
def reset():
    # reset the responses 
    session['responses'] = []
    # responses = []
    return redirect('/questions/0')

#  Step Three: the Question Page -> I don't understand this <int:question_id> where does it come from? 
@app.route('/questions/<int:question_id>')
def question_page(question_id):

    responses = session.get('responses')
    # This current_survey is not being recognized... unsure if it's just not being saved 
    survey_code = session['current_survey']
    survey = surveys[survey_code]

    if (responses is None):
        return redirect('/')
    
    # Step 6: Protecting Questions
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    if (len(responses) != question_id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_id]
    return render_template("questions.html", question_id = question_id, question=question)

# Step Four: Handling Answers
@app.route('/answer', methods=["POST"])
def answer_page():
    # responses = session.get('responses')
    # This current_survey is not being recognized... unsure if it's just not being saved 
    survey_code = session['current_survey']
    survey = surveys[survey_code]
    # get the response choice
    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses


    # Step Five
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    # return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def questions_answered():
    return render_template("complete.html")






# ------------------------------------------------------------------------------------------------------------
# from flask import Flask, request
# # Create application object
# app = Flask(__name__)

# @app.route('/search')
# def search():
#     term = request.args["term"]
#     return f"<h1>Search Results For: {term}</h1>"

# # @app.route('/post', methods=["POST"])
# # def post_demo():
# #     return "YOU MADE A POST REQUEST"

# @app.route('/add-comment')
# def add_comment_form():
#     return """
#     <h1>Add comment</h1>
#     <form>
#         <input type='text' placeholder ='comment' name='comment'/>
        
#         <button>Submit</button>
#     </form>
#     """

# @app.route('/add-comment', methods=["POST"])
# def save_comment():
#     comment = request.form["comment"]
#     return f"""
#     <h1>SAVED YOUR COMMENT WITH TEXT OF {comment}</h1>
#     """



