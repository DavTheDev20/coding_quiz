from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from db_connect import db, Quiz, Question, Answer
import datetime
import traceback
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()

db.connect()

if not db.table_exists([Quiz, Question, Answer]):
    db.create_tables([Quiz, Question, Answer])

db.close()


# UI Routes
@app.route('/')
def index():
    quizzes = get_quizzes().json
    return render_template("index.html", title="Py Quiz", quizzes=quizzes)


@app.route("/quiz/<quiz_id>")
def quiz_page(quiz_id):
    quiz = get_quiz(quiz_id=quiz_id)['quiz']
    return render_template("quiz.html", quiz=quiz,)


@app.route("/quiz/<quiz_id>/result")
def quiz_result_page(quiz_id):
    quiz = get_quiz(quiz_id=quiz_id)['quiz']
    return render_template("result.html", quiz=quiz)


# API Routes
@app.route('/api/quiz', methods=["POST"])
def create_quiz():
    db.connect()
    data = request.json
    try:
        new_quiz = Quiz.create(
            title=data['title'], description=data['description'], creator=data['creator'])
        new_quiz.creation_date = datetime.date.today()
        new_quiz.save()
        db.close()
        return {'success': True}
    except KeyError:
        db.close()
        return {'error': traceback.format_exc(),
                'msg': "title, description, and creator must be included in request body."}, 400


@app.route("/api/quiz/<quiz_id>", methods=["GET"])
def get_quiz(quiz_id):
    db.connect()
    quiz_data = Quiz.select().join(Question).switch(
        Quiz).where(Quiz.quiz_id == quiz_id).get()
    quiz = {
        "quiz_id": quiz_data.quiz_id,
        "title": quiz_data.title,
        "description": quiz_data.description,
        "creator": quiz_data.creator,
        "creation_date": quiz_data.creation_date,
        "questions": [
            {
                "question_id": question.question_id,
                "question_text": question.question_text,
                "answers": [
                    {
                        "answer_id": answer.answer_id,
                        "text": answer.answer_text
                    } for answer in question.answers
                ]
            } for question in quiz_data.questions
        ]
    }
    db.close()
    return {"quiz": quiz}


@app.route('/api/quiz/<quiz_id>/question', methods=['GET', 'POST'])
def get_add_questions(quiz_id):
    db.connect()
    if request.method == "POST":
        data = request.json
        try:
            new_question = Question(
                question_text=data['question_text'], quiz_id=quiz_id)
            new_question.save()
            db.close()
            return {'success': True}
        except KeyError:
            db.close()
            return {'error': traceback.format_exc()}, 400


@app.route('/api/question/<question_id>/answer', methods=["GET", "POST"])
def get_add_answers(question_id):
    db.connect()
    if request.method == "POST":
        data = request.json
        try:
            for answer in data["answers"]:
                new_answer = Answer(
                    answer_text=answer['answer_text'],
                    correct=answer["correct"],
                    question_id=question_id
                )
                new_answer.save()
            db.close()
            return {'success': True}
        except KeyError:
            return {'error': traceback.format_exc()}, 400
        except Exception:
            return {'error': traceback.format_exc()}, 400


@app.route('/api/quizzes', methods=["GET"])
def get_quizzes():
    db.connect()
    quizzes = [{
        "quiz_id": quiz.quiz_id,
        "title": quiz.title,
        "description": quiz.description,
        "creator": quiz.creator,
        "creation_date": quiz.creation_date
    } for quiz in Quiz.select()]
    db.close()
    return jsonify(quizzes)


@app.route('/api/quiz/<quiz_id>/check-answers', methods=["POST"])
@cross_origin()
def check_answers(quiz_id):
    db.connect()
    submitted_answers = request.json["submitted_answers"]
    current_quiz_data = Quiz.select().where(Quiz.quiz_id == quiz_id).get()
    current_quiz_questions = [
        {
            "question_id": question.question_id,
            "correct_answer": [answer.answer_text for answer in question.answers if answer.correct == True][0]
        } for question in current_quiz_data.questions
    ]
    total_questions = len(current_quiz_questions)
    number_of_correct = 0
    for question in current_quiz_questions:
        for submitted_answer in submitted_answers:
            if submitted_answer == question["correct_answer"]:
                number_of_correct += 1
            else:
                pass
    return {"msg": f"You got {number_of_correct} out of {total_questions} questions correct."}


app.run(debug=True)
