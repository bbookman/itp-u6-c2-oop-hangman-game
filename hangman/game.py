from .exceptions import *
import pdb, random

class GuessAttempt(object):
    def __init__(self, letter, hit= None, miss = None):
        if hit and miss:
            raise InvalidGuessAttempt
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit:
            return True
        return False
        
    def is_miss(self):
        if self.miss:
            return True
        return False
        
    def is_valid_guess(self):
        if len(self.letter) > 1 or not self.letter.isalpha():
            raise InvalidGuessedLetterException()
        return True
        
class GuessWord(object):
    def __init__(self, answer):
        if not answer or len(answer) == 0:
            raise InvalidWordException()
        self.answer = answer
        masked = ''
        for letter in answer:
            masked += '*'
        self.masked = masked
    
    def perform_attempt(self, letter):
        if not letter or len(letter) > 1:
            raise InvalidGuessedLetterException()
        if letter.lower() in self.answer.lower():
            self.unmask_word(letter)
            return GuessAttempt(letter, hit=True)
        return GuessAttempt(letter, miss=True)
            
   
    def unmask_word(self, letter):
        m = list(self.masked)
        for index in range(len(self.answer)):
            #pdb.set_trace()
            if letter.lower() == self.answer[index].lower():
                m[index] = self.answer[index].lower()
        self.masked = ''.join(m)
        
    def __str__(self):
        return 'Answer word = {a}|Masked word = {m}'.format(a = self.answer, m = word.masked)

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list = None, number_of_guesses = 5 ):
        self.remaining_misses = number_of_guesses
        if not word_list:
            word_list = self.WORD_LIST
        self.word =  GuessWord(self.select_random_word(word_list))
        self.previous_guesses =    []
        self.won = False
        self.lost = False
        self.finished = False
        
    def guess(self, letter):
        attempt = self.word.perform_attempt(letter)
        self.previous_guesses.append(letter.lower())
        
        if self.is_finished():
            raise GameFinishedException()
        
        if attempt.is_hit():
            self.word.unmask_word(letter)
            #pdb.set_trace()
            if self.word.answer == self.word.masked:
                self.won = True
                raise GameWonException()
        elif attempt.is_miss():
            self.remaining_misses -= 1
            if self.remaining_misses <= 0:
                self.lost = True
                raise GameLostException
        
        return attempt
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if len(list_of_words) == 0:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
        
    def is_finished(self):
        return self.won or self.lost
        
    def is_won(self):
        return self.won
        
    def is_lost(self):
        return self.lost
    
        
    