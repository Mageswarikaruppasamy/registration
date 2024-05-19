from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.secret_key="mesh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mageswari:abracadabra@localhost/userinfo'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)


app.app_context().push()


class Data(db.Model):
    __tablename__='userinfo'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    phone=db.Column(db.String(10))
    mail=db.Column(db.String(50))
    password=db.Column(db.String(60))
    
    def __init__(self,name,phone,mail,password):
        self.name=name
        self.phone=phone
        self.mail=mail
        self.password=password

@app.route('/', methods=['POST','GET'])

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        name=request.form['name']
        phone=request.form['phone']
        mail=request.form['mail']
        password=request.form['password']
        encrypted_password=bcrypt.generate_password_hash(password).decode("utf-8")
        
        data=Data(name,phone,mail,encrypted_password)
        db.session.add(data)
        db.session.commit()
        
        return redirect(url_for("login"))
    
    return render_template("registration.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        
        if name and password:
            users=Data.query.filter_by(name=name).all()
            if users:
                for user in users:
                    if bcrypt.check_password_hash(user.password, password):
                        return redirect(url_for("main"))
                flash("Login Unsuccessful", "danger")
            else:
                flash("Login Unsuccessful", "danger")
        else:
            flash("Please fill username and password", "warning")
            
    
    return render_template("login.html")

@app.route('/main')
def main():
    return render_template("main.html")



if __name__ == '__main__':
    app.run(debug=True)