from hangServer import *
import unittest
import string

PRESERVE_CONTEXT_ON_EXCEPTION = False

class ServerTests(unittest.TestCase):

##########################################################
#test the word generation function to make sure
#words with apostrophes are never used

    def test_word_generation(self):
        word_array = ['don\'t','won\'t','hello']
        word = genWord(word_array)
        for i in range(1000):
            self.assertEqual(word,('hello',5))

##########################################################
# test routes for clean get requests 

    def test_routes(self):
        with app.test_client() as c:
            response = c.get('/')
            self.assertEqual(response.status_code,200)
            response=c.get('/sessionCover')
            self.assertEqual(response.status_code,200)
            #guess A
            response=c.get('/guess/1')
            self.assertEqual(response.status_code,200)

##########################################################
#test game logic

    def test_logic(self):
        with app.test_client() as c:

#get home route to create the session objects

            response = c.get('/')
            '''check session objects and set our word to hello
            for effective testing
            '''
            with c.session_transaction() as session:
                session['total'] = genWord(['hello'])
                session['word'] = session['total'][0]
                session['wordLen'] = session['total'][1]
                self.assertEqual(session['correct'],0)
                self.assertEqual(session['wins'],0)
                self.assertEqual(session['guesses'],0)

#!!!make some guesses against hello!!!
#guess 'e' (correct)

            response = c.get('/guess/5')
            with c.session_transaction() as session:
                self.assertEqual(session['guesses'],1)
                self.assertEqual(session['correct'],1)

#guess 'a' (wrong)
            response = c.get('/guess/1')
            with c.session_transaction() as session:
                self.assertEqual(session['guesses'],2)
                self.assertEqual(session['correct'],1)

# test one full json response, guess 'l'

            response = c.get('/guess/12')
            data = json.loads(response.data)
            self.assertEqual(data, dict(inside=True,
                locations = [2,3],correct = 2,guesses = 3,
                finished = False,wins = 0,totGames = 0
                ))

#finish the game and test wins and totGames correctness

            response = c.get('/guess/8')
            response = c.get('/guess/15')
            with c.session_transaction() as session:
                self.assertEqual(session['wins'],1)
                self.assertEqual(session['totGames'],1)
                self.assertEqual(session['finished'],True)

##########################################################

unittest.main()
