

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging

from flask_mysqldb import MySQL
from flask_wtf import Form
from wtforms import StringFeild, TextAreaField, PasswordField, Validators
from  passlib.hash import sha256_crypt

app = FlasK(__name__) 

# config MySql
app.config[ 'MySQL_HOST'] = 'localhost'
app.config[ 'MySQL_USER'] = 'root'
app.config[ 'MySQL_PASSWORD'] = 'minu'
app.config[ 'MySQL_DB'] = 'register'
app.config[ 'MySQL_CURSORCLASS'] = 'DistCursor'

#init MYSQL
mysql = MySQL(app)

# register form class
class RegisterForm(Form):
   name = StringFieldld('name',[validators.length(min = 2, max = 30)])
   username = StringField('username',[validators.length(min = 2, max = 20)])
   email = StringField('email',[validators.length(min = 6, max = 30)])
   password = PasswordField('password',[validators.DataRequired(), validators.EqualTo('confirm', message = 'Password do not match')])
   confirm = PasswordField('confirm password')

#user register
@app.route('/register', method=['GET', 'POST'])
def register():
   form = RegisterForm(request.form)
   if request.method == 'POST' and form.validate():
      name = form.name.data
      username = form.username.data
      email = form.email.data
      password = sha256_crypt.encrypt(str(form.password.data))

      cur = mysql.connection.cursor

      cur.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))

      mysql.connection.commit()

      cur.close()

      falsh('You are now registered', 'success')

      return redirect(url_for('login'))
   else:
      return render_template('register.html', form=form)

if __name__ == '__main__':
	app.secret_keys = 'secret123'
	app.run(debug=true)