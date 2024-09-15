from flask import Flask,render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6514@localhost/grocery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    product_id = db.Column(db.String)
    quantity = db.Column(db.Numeric)
    unit = db.Column(db.String)
    price = db.Column(db.Numeric)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
