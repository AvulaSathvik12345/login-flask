from flask import Flask,render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,migrate
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from flask_bootstrap import Bootstrap
from flask_login import UserMixin,LoginManager,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6514@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sathvik'
db = SQLAlchemy(app)
migrate=Migrate(app,db)
bootstrap=Bootstrap(app)
login_manager=LoginManager(app)
login_manager.login_view='login'


class User(UserMixin,db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class regform(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired()])
    conformpassword=PasswordField('conform password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('register')
class loginform(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    submit=SubmitField('submit')

@app.route("/")
def index():
    return "Hello"

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dashboard.html',user=current_user.username,email=current_user.email)
@app.route('/register',methods=['GET','POST'])
def register():
    form=regform()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('registration sussessfull')
        return redirect(url_for('login'))
    return render_template('registration.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and  check_password_hash(user.password,form.password.data):
            login_user(user)
            return  redirect(url_for('dash'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)


