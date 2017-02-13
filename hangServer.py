from flask import Flask, render_template, session, jsonify,redirect,abort,json
from random import choice
app= Flask(__name__)
#set secret key for sessions
app.secret_key='F33z1ibmnouuIcxr3r4j4clevelslove'
with open('words.txt') as f:
	content = f.readlines()
wordArr = [x.rstrip() for x in content]

def genWord(wordArr):
    word=choice(wordArr)
    if '\'' in word:
        return genWord(wordArr)
    wordLen=len(word)
    return word,wordLen

def persistData():
    session['wins'] = 0
    session['totGames'] = 0

def sessionData():
    session['correct'] = 0
    session['guesses'] = 0
    session['finished'] = False
    session['totalCorrect'] = 0
    session['guessList'] = []

def sessionWord():
    session['total'] = genWord(wordArr)
    session['word'] = session['total'][0]
    session['wordLen'] = session['total'][1]

@app.route('/')
@app.route('/<cover>',methods = ['GET'])
def home(cover=None):
    if cover == 'sessionCover':
        sessionWord()
        sessionData()
        return render_template('index.html',my_len = session['wordLen'])
    elif cover==None:
        persistData()
        sessionData()
        sessionWord()
        return render_template('index.html',my_len = session['wordLen'])
    else:
        abort(404)

@app.route('/guess/<guess>')
def guess(guess):
    guess=chr(int(guess)+96)
    if guess in session['guessList']:
        return ('',204)
    else:
        session['guessList'].append(guess)
    locations = []
    inside=False
    session['guesses'] += 1
    correctOnce=False
    wordFiller = {}
    for i in range(session['wordLen']):
        if guess == session['word'][i]:
            inside = True
            session['totalCorrect'] += 1
            if not correctOnce:
                session['correct'] += 1
                correctOnce = True
            locations.append(i)
    if session['totalCorrect'] == session['wordLen']:
        session['finished'] = True
        session['wins'] += 1
        session['totGames'] += 1
    elif session['guesses']-session['correct'] == 10:
        session['finished'] = True
        session['totGames'] += 1
        wordFiller = {}
        word=session['word']
        for char in range(session['wordLen']):
            if (word[char] not in session['guessList'] and 
                    word[char] not in wordFiller):
                wordFiller[word[char]] = [char]
            elif word[char] not in session['guessList']:
                wordFiller[word[char]].append(char)
    sessionJSON = {'inside':inside,'locations':locations,
            'wordFiller':wordFiller,
            'correct':session['correct'],
            'guesses':session['guesses'],
            'finished':session['finished'],
            'wins':session['wins'],
            'totGames':session['totGames']}
    return jsonify(sessionJSON)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
