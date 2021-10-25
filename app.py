from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
# RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_survey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# Step Two: The Start Page
responses = []

# @app.route('/choose_survey')
# def choose_survey():
#     return render_template()

@app.route('/')
def home_page():
    return render_template("base.html", survey=survey)

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
    # get the response choice
    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses
    # fruits = session['fruits']
    # fruits.append("cherry")
    # session['fruits'] = fruits
    # responses.append(choice)

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



