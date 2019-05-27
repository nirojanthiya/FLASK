from unittest import TestCase
from flaskblog import routes

class TestStanfordNE2tree(TestCase):
    def test_stanfordNE2tree(self):
        input = [('Kumar', 'B-PERSON'), ('Sangakara', 'I-PERSON'), ('studied', 'O'), ('at', 'O'), ('University', 'B-ORGANIZATION'), ('of', 'I-ORGANIZATION'), ('Moratuwa', 'I-ORGANIZATION'), ('in', 'O')]
        output = '(S\n  (PERSON Kumar/NNP Sangakara/NNP)\n  studied/VBD\n  at/IN\n  (ORGANIZATION University/NNP of/IN Moratuwa/NNP)\n  in/IN)'
        self.assertTrue(str(routes.stanfordNE2tree(input))==output)



