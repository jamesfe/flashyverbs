import unittest
from scraping.get_conjugations import get_verb_conj_by_tense, vtrans


class TestPresentTenseVerbs(unittest.TestCase):

    def test_parse_acheter(self):
        """Test acheter in the present tense"""
        tense = 'présent'
        tval = get_verb_conj_by_tense('acheter', tense)
        self.assertEqual(tval['acheter']['tenses'][tense]['je'], 'achète')
        self.assertEqual(tval['acheter']['tenses'][tense]['nous'], 'achetons')

    def test_parse_avoir(self):
        """Test avoir in the present tense"""
        tense = 'présent'
        verb = 'avoir'
        tval = get_verb_conj_by_tense(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'ai')
        self.assertEqual(tval[verb]['tenses'][tense]['nous'], 'avons')

    def test_parse_profiter(self):
        """Test profiter in the present tense"""
        tense = 'présent'
        verb = 'profiter'
        tval = get_verb_conj_by_tense(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'profite')
        self.assertEqual(tval[verb]['tenses'][tense]['il,elle,on'], 'profite')


class TestPasseComposeTenseVerbs(unittest.TestCase):

    def test_parse_acheter(self):
        """Test acheter in the present tense"""
        tense = 'passé composé'
        tval = get_verb_conj_by_tense('acheter', tense)
        self.assertEqual(tval['acheter']['tenses'][tense]['je'], 'ai acheté')
        self.assertEqual(tval['acheter']['tenses'][tense]['nous'], 'avons acheté')

    def test_parse_avoir(self):
        """Test avoir in the present tense"""
        tense = 'passé composé'
        verb = 'avoir'
        tval = get_verb_conj_by_tense(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'ai eu')
        self.assertEqual(tval[verb]['tenses'][tense]['nous'], 'avons eu')

    def test_parse_profiter(self):
        """Test profiter in the present tense"""
        tense = 'passé composé'
        verb = 'profiter'
        tval = get_verb_conj_by_tense(verb, tense)
        self.assertEqual(tval[verb]['tenses'][tense]['je'], 'ai profité')
        self.assertEqual(tval[verb]['tenses'][tense]['il,elle,on'], 'a profité')


class TestComprehensiveProblems(unittest.TestCase):

    def test_all_present(self):
        for k, v in vtrans.items():
            get_verb_conj_by_tense(k, 'présent')

    def test_all_passecompose(self):
        for k, v in vtrans.items():
            get_verb_conj_by_tense(k, 'passé composé')
