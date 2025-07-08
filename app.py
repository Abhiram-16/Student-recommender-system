from flask import Flask,render_template,request,redirect,url_for
import pickle
import pandas as pd
import numpy as np
import math
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
with app.app_context():
    db.create_all()

    db.session.commit()

    users = User.query.all()

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

'''model1=pickle.load(open('model1.pkl','rb'))
model2=pickle.load(open('model2.pkl','rb'))
model3=pickle.load(open('model3.pkl','rb'))'''
model3_2=pickle.load(open('modelfor3_2.pkl','rb'))
model4_1=pickle.load(open('modelfor4_1.pkl','rb'))

prereq=dict()
prereq['ECE']=('BEE','AP','M1')
prereq['MECH']=('M1','M2','AP','EDraw','EWS')
prereq['CIVIL']=('EDraw','EC','M1','M2','EWS')
prereq['CHEM']=('EC','BEE','M1')
prereq['EEE']=('BEE','AP','EC','M1','EDraw')
prereq['CSE']=('PPS1','PPS2','M1')
honords=('P&S','DM','PP','PPS1','PPS2','DStr')
honorcybersec=('PPS1','PPS2','DStr','DLD','DM')

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('cseorothers'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/cseorothers',methods=['POST','GET'])
def cseorothers():
    if request.method=='POST':
        data=request.form
        if data['courses']=='CSE':
            return redirect(url_for('CSE'))

        else:
            return redirect(url_for('others'))
        #return f'<h1>{data}</h1>'


    return render_template('cse or others.html')


@app.route('/CSE',methods=['POST','GET'])
def CSE():
    if request.method=='POST':
        choice=request.form
        if choice['type']=='electives':
            return redirect(url_for('semester'))
        if choice['type']=='honors':
            return redirect(url_for('CSEhonors'))
        if choice['type']=='minors':
            return redirect(url_for('CSEminors'))

    return render_template('CSE.html')

@app.route('/semester',methods=['POST','GET'])
def semester():
    if request.method=='POST':
        choice=request.form
        
        if choice['semester']=='3-2':
            return redirect(url_for('sem3_2'))
        if choice['semester']=='4-1':
            return redirect(url_for('sem4_1'))


    return render_template('semesterselect.html')

@app.route('/sem3_2',methods=['POST','GET'])
def sem3_2():
    if request.method=='POST':
        formdata=request.form
        temp=formdata.copy()
        formdata=dict()
        for k,v in temp.items():
            formdata[k]=int(v)
        print(formdata)
        coursenames=['R Programming','Unix Programming','Object Oriented Analysis and Design','Machine Learning',
                     'E-Commerce','Cyber Forensics','Mobile Computing','Advanced Databases','Human Computer Interaction']
        int_features=[int(i) for i in formdata.values()]
        features=[np.array(int_features)]
        int_preds=list(map(float,model3_2.predict(features)[0]))
        PE1=dict(zip(coursenames[:3],int_preds[:3]))
        PE2=dict(zip(coursenames[3:6],int_preds[3:6]))
        PE3=dict(zip(coursenames[6:],int_preds[6:]))
        m=max(PE1.values())
        for k,v in PE1.items():
            if v==m:
                RecommPE1=k
        m=max(PE2.values())
        for k,v in PE2.items():
            if v==m:
                RecommPE2=k
        m=max(PE3.values())
        for k,v in PE3.items():
            if v==m:
                RecommPE3=k
        return render_template('3_2output.html',R=PE1['R Programming'],UNIX=PE1['Unix Programming'],
                               OOAD=PE1['Object Oriented Analysis and Design'],ML=PE2['Machine Learning'],
                               ECom=PE2['E-Commerce'],CF=PE2['Cyber Forensics'],MC=PE3['Mobile Computing'],
                               AD=PE3['Advanced Databases'],HCI=PE3['Human Computer Interaction'],RecommPE1=RecommPE1,
                               RecommPE2=RecommPE2,RecommPE3=RecommPE3)
    return render_template('3-2.html')

@app.route('/sem4_1',methods=['POST','GET'])
def sem4_1():
    if request.method=='POST':
        formdata=request.form
        temp=formdata.copy()
        formdata=dict()
        for k,v in temp.items():
            formdata[k]=int(v)
        coursenames=['Big Data','Distributed Systems','Soft Computing',
                     'Internet of Things','Computer Graphics','Software Testing Methodologies',
                     'Data Science and Analytics','Cloud Computing','Image Processing']
        int_features=[int(i) for i in formdata.values()]
        features=[np.array(int_features)]
        int_preds=list(map(float,model4_1.predict(features)[0]))
        PE4=dict(zip(coursenames[:3],int_preds[:3]))
        PE5=dict(zip(coursenames[3:6],int_preds[3:6]))
        PE6=dict(zip(coursenames[6:],int_preds[6:]))
        m=max(PE4.values())
        for k,v in PE4.items():
            if v==m:
                RecommPE4=k
        m=max(PE5.values())
        for k,v in PE5.items():
            if v==m:
                RecommPE5=k
        m=max(PE6.values())
        for k,v in PE6.items():
            if v==m:
                RecommPE6=k
        return render_template('4_1output.html',IP=PE6['Image Processing'],BD=PE4['Big Data'],CC=PE6['Cloud Computing'],
                               Dsys=PE4['Distributed Systems'],SC=PE4['Soft Computing'],DSA=PE6['Data Science and Analytics'],
                               IoT=PE5['Internet of Things'],STM=PE5['Software Testing Methodologies'],CG=PE5['Computer Graphics'],
                               RecommPE4=RecommPE4,RecommPE5=RecommPE5,RecommPE6=RecommPE6)

    return render_template('4-1.html')

@app.route('/CSEhonors',methods=['POST','GET'])
def CSEhonors():
    if request.method=='POST':
        formdata=request.form
        temp=formdata.copy()
        formdata=dict()
        for k,v in temp.items():
            formdata[k]=int(v)
        #return f'<h1>{data}</h1>'
        data=pd.read_csv('New dataset.csv')
        data = data.fillna(data.median())
        data = data.to_dict('list')
        toppercentiles=dict()
        for k,v in data.items():
            toppercentiles[k]=np.percentile(v,20)
        counth=0
        dsh=0
        for c in honords:
            if formdata[c]>=toppercentiles[c]:
                counth+=1
        if counth>=5:dsh=1
        counth=0
        cybersech=0
        for c in honords:
            if formdata[c]>=toppercentiles[c]:
                counth+=1
        if counth>=4:cybersech=1

        if cybersech and dsh:
            Honorrecomm='Cybersecurity as well as Data Science honors along with your B.TECH is recommended for you.'
        else:
            if cybersech:
                Honorrecomm='Cybersecurity honors along with your B.TECH is recommended for you.'
            elif dsh:
                Honorrecomm='Data Science honors along with your B.TECH is recommended for you.'
            else:
                Honorrecomm='Not recommended as you did not score well in the pre-requisite subjects. Concentrate on your current B.Tech curriculum.'
        return render_template('Honors_output.html',Recomhonors=Honorrecomm)

    return render_template('CSEhonors.html')


@app.route('/CSEminors',methods=['POST','GET'])
def CSEminors():
    if request.method=='POST':
        formdata=request.form
        temp=formdata.copy()
        formdata=dict()
        for k,v in temp.items():
            formdata[k]=int(v)
        #return f'<h1>{data}</h1>'
        data=pd.read_csv('New dataset.csv')
        data = data.fillna(data.median())
        data = data.to_dict('list')
        toppercentiles=dict()
        for k,v in data.items():
            toppercentiles[k]=np.percentile(v,20)
        minors=[]
        for m,courses in prereq.items():
            countm=0
            for c in courses:
                if formdata[c]>=toppercentiles[c]:
                    countm+=1
            if countm>=math.ceil(int(len(courses))/2):
                minors.append(m)
        for i in range(len(minors)):
            if minors[i]=="CSE":
                break
        if 'CSE' in minors:minors.pop(i)
        if len(minors)==0:
            Recomminor='Not recommended as you did not score well in the pre-requisite subjects.. Concentrate on your current B.Tech curriculum.'
        else:
            Recomminor='Minors '+','.join(minors)+' are recommended along with your B.TECH.'
        return render_template('minors_output.html',Recomminor=Recomminor)

    return render_template('CSEminors.html')

@app.route('/others',methods=['POST','GET'])
def others():
    if request.method=='POST':
        formdata=request.form
        temp=formdata.copy()
        formdata=dict()
        for k,v in temp.items():
            formdata[k]=int(v)
        #return f'<h1>{data}</h1>'
        data=pd.read_csv('New dataset.csv')
        data = data.fillna(data.median())
        data = data.to_dict('list')
        toppercentiles=dict()
        for k,v in data.items():
            toppercentiles[k]=np.percentile(v,20)
        minors=[]
        for m,courses in prereq.items():
            countm=0
            for c in courses:
                if formdata[c]>=toppercentiles[c]:
                    countm+=1
            if countm>=math.ceil(int(len(courses))/2):
                minors.append(m)
        
        if len(minors)==0:
            Recomminor='Not recommended as you did not score well in the pre-requisite subjects. Concentrate on your current B.Tech curriculum.'
        else:
            Recomminor='Minors '+','.join(minors)+' are recommended along with your B.TECH.'
        return render_template('minors_output.html',Recomminor=Recomminor)

    return render_template('others.html')

'''@app.route('/hello',methods=['POST','GET'])
def hello():
    if request.method=='POST':
        formdata=request.form
        temp=formdata.copy()
        formdata=dict()
        for k,v in temp.items():
            formdata[k]=int(v)
        #return f'<h1>{data}</h1>'
        int_features=[int(i) for i in formdata.values()]
        vars=[np.array(int_features)]
        preds=dict()
        preds['Data Science']=float(model1.predict(vars))
        preds['IOT']=float(model2.predict(vars))
        preds['Machine Learning']=float(model3.predict(vars))
        m=max(preds.values())
        for k,v in preds.items():
            if v==m:
                Recommendation=k
        
        
        return render_template('output.html',
        Data_Science=preds['Data Science'],
        IOT=preds['IOT'],
        Machine_Learning=preds['Machine Learning'],
        Recomm=Recommendation)

        #return f'<h1>{pred1, pred2, pred3}</h1>'


        
    return render_template('index.html')

@app.route('/<usr>')
def getdata(usr):
    return f'<h1>{usr}</h1>'''

if __name__=='__main__':
    app.run(debug=True)
