from unittest import TestCase

from flaskblog import routes




class TestStanfordNE2BIO(TestCase):
    def test_stanfordNE2BIO(self):
        input=[('Kumar', 'PERSON'), ('Sangakara', 'PERSON'), ('studied', 'O'), ('at', 'O'), ('University', 'ORGANIZATION'), ('of', 'ORGANIZATION'), ('Moratuwa', 'ORGANIZATION'), ('in', 'O')]
        output=[('Kumar', 'B-PERSON'), ('Sangakara', 'I-PERSON'), ('studied', 'O'), ('at', 'O'), ('University', 'B-ORGANIZATION'), ('of', 'I-ORGANIZATION'), ('Moratuwa', 'I-ORGANIZATION'), ('in', 'O')]
        self.assertTrue(routes.stanfordNE2BIO(input)==output )

