import flask
from flask import request, jsonify
from flask_mysqldb import MySQL

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql6405093'
app.config['MYSQL_PASSWORD'] = '9wzwmi2pzJ'
app.config['MYSQL_DB'] = 'sql6405093'
mysql = MySQL(app)


@app.route('/api/userLogin',  methods=['POST'])
def userLogin():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", [email, password])
        account = cur.fetchone()
        mysql.connection.commit()
        if account:
            name = account[0]
            email = account[1]
            active = account[4]
            return jsonify({"name": name, "email": email, "active": active})
        else:
            return jsonify({})


@app.route('/api/adminLogin',  methods=['POST'])
def adminLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE email = %s AND password = %s", [email, password])
        account = cur.fetchone()
        mysql.connection.commit()
        if account:
            name = account[0]
            email = account[1]
            return jsonify({"name": name, "email": email})
        else:
            return jsonify({})


@app.route('/api/adminUsers',  methods=['POST'])
def adminUsers():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE addedBy = %s", [email])
        row = cur.fetchall()
        mysql.connection.commit()
        if row:
            l = []
            for i in row:
                name = i[0]
                email = i[1]
                active = i[4]
                l.append({"name": name, "email": email, "active": active})
            return jsonify(l)
        else:
            return jsonify({})


@app.route('/api/setActive',  methods=['POST'])
def setActive():
    if request.method == 'POST':
        email = request.form['email']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        cur.execute("update users set active = %s where email = %s ", [
                    status, email])
        cur2.execute("SELECT * FROM users WHERE email = %s", [email])
        row = cur2.fetchone()
        mysql.connection.commit()
        if row:
            return jsonify({"result": row[4]})

# create a post request on /api/deleteUser with body as {"email":email}
# return True if query is sucessfully ececuted otherwise {result:_____}

@app.route('/api/deleteUser',  methods=['POST'])
def deleteUser():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        r = cur.execute("delete from users where email = %s ", [email])
        mysql.connection.commit()
        if(r == 1):
            return jsonify({"result": True})
        return jsonify({"result": False})


# create a post request on /api/registerUser with body as {email,name,pass,addedBy,active}
# return True if user is sucessfully added  otherwise False {result:_____}
@app.route('/api/registerUser',  methods=['POST'])
def registerUser():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'name' in request.form:
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        addedBy = request.form['addedBy']
        active = request.form['active']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO users(name,email,password,addedBy,active) VALUES ( %s, %s, %s,%s,%s)', (name, email, password, addedBy, active))
            mysql.connection.commit()
            return jsonify({"result": True})
        except:
            return jsonify({"result": False})


@app.route('/',)
def home():
    return jsonify({"data": "sample data "})


app.run()
