import unittest
from scraping.get_conjugations import verb_to_csv

class TestPresentTenseVerbs(unittest.TestCase):

    def test_parse_acheter(self):
        """Test acheter in the present tense"""
        tense = 'présent'
        tval = verb_to_csv('acheter', tense)
        self.assertEqual(tval['acheter']['tenses'][tense]['je'], 'achète')
        self.assertEqual(tval['acheter']['tenses'][tense]['nous'], 'achetons')

    def test_parse_avoir(self):
        """Test avoir in the present tense"""
        tense = 'présent'
        verb = 'avoir'
        tval = verb_to_csv(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'ai')
        self.assertEqual(tval[verb]['tenses'][tense]['nous'], 'avons')

    def test_parse_profiter(self):
        """Test profiter in the present tense"""
        tense = 'présent'
        verb = 'profiter'
        tval = verb_to_csv(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'profite')
        self.assertEqual(tval[verb]['tenses'][tense]['il,elle,on'], 'profite')


class TestPasseComposeTenseVerbs(unittest.TestCase):

    def test_parse_acheter(self):
        """Test acheter in the present tense"""
        tense = 'passé composé'
        tval = verb_to_csv('acheter', tense)
        self.assertEqual(tval['acheter']['tenses'][tense]['je'], 'ai acheté')
        self.assertEqual(tval['acheter']['tenses'][tense]['nous'], 'avons acheté')

    def test_parse_avoir(self):
        """Test avoir in the present tense"""
        tense = 'passé composé'
        verb = 'avoir'
        tval = verb_to_csv(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'ai eu')
        self.assertEqual(tval[verb]['tenses'][tense]['nous'], 'avons eu')

    def test_parse_profiter(self):
        """Test profiter in the present tense"""
        tense = 'passé composé'
        verb = 'profiter'
        tval = verb_to_csv(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'ai profité')
        self.assertEqual(tval[verb]['tenses'][tense]['il,elle,on'], 'a profité')

