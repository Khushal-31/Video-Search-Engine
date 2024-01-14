from flask import Blueprint, render_template, request,session,redirect,url_for

import mysql.connector

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=["GET","POST"])
def login():

    conn = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd ="watermelon",
                               database ="cactus_login",
                               auth_plugin='mysql_native_password')

    cursor = conn.cursor()

    # Getting Username and Password

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

        cursor.execute("SELECT * FROM users WHERE username = '{}';".format(username))

        user = cursor.fetchone()

        if user:
            
            if username == user[1] and password == user[2]:
                
                session['user'] = username
                session['logged_in'] = True

                return redirect(url_for('views.home_page'))
            
            elif username == user[1] and password != user[2]:

                return redirect('/login')
            
        else:

            cursor.execute("INSERT INTO users (`username`,`password`) VALUES ('{}','{}');".format(username,password))

            conn.commit()

            return redirect('/login')
            
    conn.close()

    return render_template("login.html")

@auth.route('/logout')
def logout():

    if session.get('user') is not None or session.get('logged_in') is not False:

        session['user'] = None
        session['logged_in'] = False

    return redirect('/login')
