from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, PostForm
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required
# import pickle

import secrets

from nltk import tag
from nltk.tag import stanford
from nltk.tag.stanford import StanfordNERTagger

import os

from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree


import nltk
# from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import regex as re

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def preprocess(data):
     stopWords = set(stopwords.words('english'))
     words = data.split()

#     words = word_tokenize(data)
     wordsFiltered = []
     for w in words:
         if w not in stopWords:
             wordsFiltered.append(w)
#
#     #print(wordsFiltered)
#     #print(nltk.pos_tag(wordsFiltered))
#     review=nltk.pos_tag(wordsFiltered)
#     #print(review)
#
#     a=[]
#     for pos in review:
#         a.append("/".join(pos))
#     #print(a)
#     #print(" ".join(a))
     return wordsFiltered

def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O":  # O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":  # Begin NE
            bio_tagged_sent.append((token, "B-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:  # Inside NE
            bio_tagged_sent.append((token, "I-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
            bio_tagged_sent.append((token, "B-" + tag))
            prev_tag = tag

    return bio_tagged_sent

def stanfordNE2tree(ne_tagged_sent):
    # bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    # print(bio_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*ne_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree


@app.route("/")
def homepage():
    return render_template('homepage.html',title='Homepage')



@app.route("/review")
@login_required
def review():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('review.html', title='Review',posts=posts)


def save_document(from_doc):
    random_hex = secrets.token_hex(8)
    name, f_ext = os.path.splitext(from_doc.filename)
    document_fn = random_hex + f_ext
    doc_path = os.path.join(app.root_path, 'static/documents', document_fn)
    from_doc.save(doc_path)
    return document_fn


    # if not (".txt" in file.filename):
    #     return render_template("file Error.html")
    # if file:
        # destination = "/".join([target, filename])
        # file.save(destination)
        # doc_path = os.path.join(app.root_path, 'static/documents', filename)
        # # from_doc.save(doc_path)
        # file.save(doc_path)
    # return doc_path



@app.route("/home", methods=['GET','POST'])
@login_required
def home():

    # pkl = open('mlmodel.pickle', 'rb')
    # vec = open('vectorizer.pickle', 'rb')
    #
    # clf = pickle.load(pkl)
    # v = pickle.load(vec)

    # file = request.files['file']
    # filename = file.filename
    # target = os.path.join(APP_ROOT, 'static/documents/')
    # random_hex = secrets.token_hex(8)
    # name,f_ext = os.path.splitext(from_doc.filename)
    # document_fn = random_hex+f_ext
    #
    # if not (".txt" in file.filename):
    #     return render_template("file Error.html")
    # if file:
    #     destination = "/".join([target, filename])
    #     file.save(destination)
        # doc_path = os.path.join(app.root_path, 'static/documents', filename)
        # # from_doc.save(doc_path)
        # file.save(doc_path)
    # return doc_path

    form = PostForm()
    if form.validate_on_submit():
        if form.dumpFile.data:
            dump_file = save_document(form.dumpFile.data)
            doc_path = os.path.join(app.root_path, 'static/documents',dump_file)
            with open(doc_path)as file:
                lines=''
                for line in file:
                    lines =lines+line
                info =lines

            # for line in savedata:
            #     print(line)
            # return render_template('savedata.html')
        else:
            if form.content.data:
                info = form.content.data
        java_path = "C:\\Program Files\\Java\\jre1.8.0_201\\bin\\java.exe"
        os.environ['JAVAHOME'] = java_path

        st1 = StanfordNERTagger(
            'C:\\Users\\Niro\\PycharmProjects\\FLASK\\stanford-ner-2018-10-16\\classifiers\\english.all.3class.distsim.crf.ser.gz',
            'C:\\Users\\Niro\\PycharmProjects\\FLASK\\stanford-ner-2018-10-16\\stanford-ner.jar')

        st2 = StanfordNERTagger(
            'C:\\Users\\Niro\\PycharmProjects\\FLASK\\stanford-ner-2018-10-16\\classifiers\\english.muc.7class.distsim.crf.ser.gz',
            'C:\\Users\\Niro\\PycharmProjects\\FLASK\\stanford-ner-2018-10-16\\stanford-ner.jar')

        r1 = st1.tag(info.split())
        # print(r1)
        ne_tagged_sent12 = r1

        # print(stanfordNE2BIO(ne_tagged_sent1))

        ne_tree1 = stanfordNE2BIO(ne_tagged_sent12)
        ne_tree = stanfordNE2tree(ne_tree1)

        print(ne_tree)

        # print (ne_tree)


        ne_in_sent1 = []
        info_data = []
        info_name = []
        info_date = []
        info_location = []
        info_organization = []
        info_email = []

        for subtree in ne_tree:

            if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
                # print(subtree)
                ne_label = subtree.label()
                # print(ne_label)
                ne_string = " ".join([token for token, pos in subtree.leaves()])
                # print(ne_string)
                ne_in_sent1.append((ne_string, ne_label))
                print(ne_in_sent1)
        # print(ne_in_sent)


    ### Person
        for i in ne_in_sent1:
            if(i[1] == 'PERSON'):
                info_name.append(i[0])
                info_data.append(i)
                #form.name.data = i
                #flash('This review is contains Names!!!', 'danger')

        if (len(info_name)>0):
            flash('This review is contains Names!!!:-     ' + str(info_name), 'danger')


        form.name.data = str(info_name)


    ###  Organization
        for i in ne_in_sent1:
            if(i[1] == 'ORGANIZATION'):
                info_organization.append(i[0])
                info_data.append(i)
                #form.name.data = i
                #flash('This review is contains Names!!!', 'danger')

        if (len(info_organization)>0):
            flash('This review is contains Organizations!!!:-     ' + str(info_organization), 'danger')


        form.organization.data = str(info_organization)


    # form = PostForm()
    # if form.validate_on_submit():
    #     info = form.content.data
        r2 = st2.tag(info.split())

        ne_tagged_sent23 = r2
        ne_tree2 = stanfordNE2BIO(ne_tagged_sent23)


        ne_tree = stanfordNE2tree(ne_tree2)

        # print (ne_tree)


        ne_in_sent2 = []
        for subtree in ne_tree:
            if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
                ne_label = subtree.label()
                ne_string = " ".join([token for token, pos in subtree.leaves()])
                ne_in_sent2.append((ne_string, ne_label))
        # print(ne_in_sent)

    #####  DATE
        for i in ne_in_sent2:
            if (i[1] == 'DATE'):
                info_date.append(i[0])
                info_data.append(i)
                #form.result.data = str(ne_in_sent2)
                #flash('This review is contains Dates!!!', 'danger')

        if (len(info_date)>0):
            flash('This review is contains Date!!!:-     ' + str(info_date), 'danger')

        form.date.data = str(info_date)

      #### Location
        for i in ne_in_sent2:
            if (i[1] == 'LOCATION'):
                info_location.append(i[0])
                info_data.append(i)
                #form.result.data = str(ne_in_sent2)
                #flash('This review is contains Dates!!!', 'danger')

        if (len(info_location)>0):
            flash('This review is contains Locations!!!:-'+ "  "+ "  " + str(info_location), 'danger')

        form.location.data = str(info_location)



    ####  Email
        data = preprocess(info)
        email_info = [i for i in data if (re.search('@gmail.com$', i) or re.search('@gmail.com.$', i) )]
        #print(email_info)
        if (len(email_info) > 0):
            for i in email_info:
                # print(i)
                #a= tuple(i,'EMAIL')
                info_email.append(i)
                info_data.append(i )
            # form.result.data = str(ne_in_sent2)
            flash('This review is contains email address!!!:-  ' + str(info_email), 'danger')

        #form.result.data = str(info_data)
        form.email.data = str(info_email)

        # data = [preprocess(review)]
        # vect = v.transform(data).toarray()
        # my_prediction = clf.predict(vect)
        # if my_prediction == 'deceptive':
        #     form.result.data = 'deceptive'
        #     flash('This review is considered as A FAKE REVIEW!!!', 'danger')
        # elif my_prediction == 'truth':
        #     form.result.data = 'truth'
        #     flash('This review is considered as NOT A FAKE REVIEW!!!', 'success')

        post = Post(content=info, name=form.name.data, location=form.location.data, organization=form.organization.data, date=form.date.data, email=form.email.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()

        #return redirect(url_for('review'))
    return render_template('home.html', title='Home', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

