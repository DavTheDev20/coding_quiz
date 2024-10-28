from peewee import *
import os

db = MySQLDatabase("coding_quiz_db", user=os.getenv("DB_USER"), password=os.getenv(
    "DB_PASSWORD"), host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")))


class Quiz(Model):
    quiz_id = AutoField(primary_key=True)
    title = CharField(max_length=50)
    description = TextField()
    creator = CharField(max_length=75)
    creation_date = DateField()

    class Meta:
        database = db


class Question(Model):
    question_id = AutoField(primary_key=True)
    question_text = TextField()
    quiz = ForeignKeyField(Quiz, backref="questions")

    class Meta:
        database = db


class Answer(Model):
    answer_id = AutoField(primary_key=True)
    answer_text = TextField()
    correct = BooleanField()
    question = ForeignKeyField(Question, backref="answers")

    class Meta:
        database = db
