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
            if letter.lower() in self.answer.lower():
                attempt = GuessAttempt(letter, hit=True)
                if attempt.is_valid_guess():
                    self.unmask_word(attempt)
                else:
                    attempt = GuessAttempt(letter, miss=True)
            return attempt
   
    def unmask_word(self, attempt):
        m = list(self.masked)
        for index in range(len(self.answer)):
            if attempt.letter.lower() == self.answer[index].lower():
                m[index] = self.answer[index].lower()
        self.masked = ''.join(m)

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list = None, number_of_guesses = 5 ):
        self.remaining_misses = number_of_guesses
        if not word_list:
            word_list = self.WORD_LIST
        word = GuessWord(self.select_random_word(word_list))
        self.word = word
        self.masked_word = word.masked
        previous_guesses = []
        self.previous_guesses =   previous_guesses
            
    def guess(self, letter):
        self.remaining_misses -= 1
        attempt = self.word.perform_attempt(letter)
        if attempt.is_hit():
            self.word.unmask_word(attempt)
            self.is_finished()
            self.is_won()
        elif attempt.is_miss():
            self.is_finished()
            self.is_lost()
            
    @classmethod
    def select_random_word(cls, list_of_words):
        if len(list_of_words) == 0:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
        
    def is_finished(self):
        if self.is_won() or self.is_lost() or self.remaining_misses <= 0:
            raise GameFinishedException()
        
    def is_won(self):
        if self.word.answer.lower() == self.word.masked.lower():
            raise GameWonException()
        return False
        
    def is_lost(self):
        if self.remaining_misses <= 0:
            raise GameLostException()
    
        
    