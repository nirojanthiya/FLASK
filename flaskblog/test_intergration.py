from unittest import TestCase
from flaskblog import routes

class TestIntergration(TestCase):
    def test_intergration(self):
        input = [('Kumar', 'PERSON'), ('Sangakara', 'PERSON'), ('studied', 'O'), ('at', 'O'), ('University', 'ORGANIZATION'), ('of', 'ORGANIZATION'), ('Moratuwa', 'ORGANIZATION'), ('in', 'O')]
        ne_tree1 = routes.stanfordNE2BIO(input)
        ne_tree = routes.stanfordNE2tree(ne_tree1)
        output = '(S\n  (PERSON Kumar/NNP Sangakara/NNP)\n  studied/VBD\n  at/IN\n  (ORGANIZATION University/NNP of/IN Moratuwa/NNP)\n  in/IN)'

        self.assertTrue(str(ne_tree)==output)



