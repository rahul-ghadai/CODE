import os
from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin , login_user, login_required, logout_user,current_user
import json
import base64

basedir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config['SECRET_KEY']='rahulghadai'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class UD(UserMixin,db.Model):
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String(80),unique=True)
	firstname=db.Column(db.String(15))
	lastname=db.Column(db.String(15))
	password=db.Column(db.String(80))
def convert_save(b64_string):
	print(type(b64_string))
	with open('imgt.png','wb') as fh:
		fh.write(base64.standard_b64decode(b64_string[22:]))

@login_manager.user_loader
def load_user(user_id):
	return UD.query.get(int(user_id))

@app.route('/')
def index():
	return render_template('welcome.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
	if(request.method=='POST'):
		first=request.form.get('firstname')
		last=request.form.get('lastname')
		email=request.form.get('email')
		psw=request.form.get('password')
		hash_psw=generate_password_hash(psw, method='sha256')
		new_user=UD(firstname=first,lastname=last,email=email,password=hash_psw)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('signin.html')


@app.route('/fsignin', methods=['GET','POST'])
@login_required
def fsignin():
	# if(request.method=='POST'):
	# 	datalocation=request.get_json()
	# 	d=datalocation['imgs1']
	# 	# print(d)
	# 	convert_save(d)
	# 	return jsonify('founded img')
	return render_template('facesignin.html')
	

@app.route('/login', methods=["GET", "POST"])
def login():
	if(request.method=='POST'):
		email=request.form.get('email')
		psw=request.form.get('password')
		check=request.form.get('check')
		user=UD.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password,psw):
				login_user(user,remember=check)
				return redirect(url_for('dashboard'))
		return '<h1> check </h1>'
	return render_template('login.html')

@app.route('/flogin', methods=["GET", "POST"])
def flogin():
	if(request.method=='POST'):
		datalocation=request.get_json()
		f=datalocation['imgsrc']
		convert_save(f)
		# print(d)
		if (True):
			return jsonify('login')
		else:
			return jsonify('')
	return render_template('facelogin.html')
	

@app.route('/forgotpsw')
def forgotpsw():
	return render_template('forgot-password.html')

@app.route('/dashboard')
# @login_required
def dashboard():
	return render_template('dashboard.html',name=current_user.firstname)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
@app.route('/assistent')
@login_required
def assistent():
	return render_template('assistent.html')
@app.route('/circuit')
@login_required
def circuit():
	return render_template('circuit.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)



