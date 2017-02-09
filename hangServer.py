from flask import Flask, render_template, session, jsonify
from random import randint
app= Flask(__name__)
#set secret key for sessions
app.secret_key='F33z1ibmnouuIcxr3r4j4clevelslove'
with open('words.txt') as f:
	content=f.readlines()
wordArr=[x.rstrip() for x in content]

def genWord(wordArr):
    wordArrLen=len(wordArr)-1
    word_index=randint(0,wordArrLen)
    word=wordArr[word_index]
    wordLen=len(word)
    return word,wordLen

def persistData():
    session['wins']=0
    session['totGames']=0

def sessionData():
    session['correct']=0
    session['guesses']=0
    session['finished']=False

def sessionWord():
    session['total']=genWord(wordArr)
    session['word']=session['total'][0]
    session['wordLen']=session['total'][1]

@app.route('/')
def home():
    sessionData()
    sessionWord()
    persistData()
    return render_template('index.html',my_len=session['wordLen'])

@app.route('/<guess>')
def guess(guess):
    guess=chr(int(guess)+96)
    locations=[]
    inside=False
    session['guesses']+=1
    for i in range(session['wordLen']):
        if guess==session['word'][i]:
            inside=True
            session['correct']+=1
            locations.append(i)
    if session['correct']==session['wordLen']:
        session['finished']=True
        session['wins']+=1
    sessionJSON={'inside':inside,'locations':locations,'correct':session['correct'],
            'guesses':session['guesses'],'finished':session['finished'],
            'wins':session['wins']}
    return jsonify(sessionJSON)
app.run(host='0.0.0.0')
