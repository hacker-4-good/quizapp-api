# FastAPI ⚡ + HarperDB 🚀 + AWS 🔥 

#HarperDB Connection credentials 💀

import harperdb

HARPERDB_PASSWORD = 'Mayank@04102002'
HARPERDB_URL = 'https://quizapp-noteapplication.harperdbcloud.com'
HARPERDB_USERNAME = 'mayankhacker'

db = harperdb.HarperDB(
    url = HARPERDB_URL,
    username = HARPERDB_USERNAME,
    password = HARPERDB_PASSWORD
)

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI() 

# React app is running on port 5173
origins = [
    'http://localhost:5173'
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Root route
@app.get('/')
def root():
    return "Welcome to quiz application"

# GET: All Quizes
@app.get('/quiz')
def getQuizs():
    quiz = db.sql('SELECT * FROM quizapp.quizs ORDER BY __updatedtime__ DESC')
    return {"data":quiz} 

# POST: Add a new Quiz
@app.post('/quiz')
def addQuizs(data = Body(default={"question":"", "optionA":"", "optionB":"", "optionC":"", "optionD":"", "answer":""})):
    db.insert('quizapp', 'quizs', [{'question':data['question'],'optionA':data['optionA'],'optionB':data['optionB'],'optionC':data['optionC'],'optionD':data['optionD'],'answer':data['answer']}])
    quiz = db.search_by_value('quizapp', 'quizs', 'id', '*', get_attributes=['*'])
    return quiz

# GET: A single Quiz using unique ID
@app.get('/quiz/{pk}')
def getQuiz(pk: str):
    quiz = db.search_by_hash('quizapp', 'quizs', [pk], get_attributes=['*'])
    return {'data':quiz[0]}

# PUT: Update a Quiz using unique ID
@app.put('/quiz/{id}')
def updateQuiz(id: str, data = Body(default={"body":""})):
    db.update('quizapp', 'quizs', [{'id':id, 'question':data['question']}])
    quiz = db.search_by_value('quizapp', 'quizs', 'id', '*', get_attributes=['*'])
    return quiz

# DELETE: Delete a Quiz using unique ID
@app.delete('/quiz/{id}')
def deleteQuiz(id: str):
    db.delete('quizapp', 'quizs', [id])
    quiz = db.search_by_value('quizapp', 'quizs', 'id', '*', get_attributes=['*'])
    return quiz

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)
