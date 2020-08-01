from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        userDetails = request.form
        val = userDetails['search']
        print(val)
        curr = mysql.connection.cursor()
        resultVal = curr.execute('SELECT * FROM users where Name = %s or Designation = %s or Phone = %s', (val,val,val,))
        if resultVal > 0:
            fetchdata = curr.fetchall()
            return render_template('list.html', data=fetchdata)
        else:
            return redirect('/')


@app.route('/list')
def list():
        curr = mysql.connection.cursor()
        resultVal = curr.execute('SELECT * FROM users')
        if resultVal > 0:
            fetchData = curr.fetchall()
            curr.close()
            return render_template('list.html', data=fetchData)
@app.route('/Add')
def add():
    return render_template('Add.html')

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['fname']
        dgn = userDetails['Dgn']
        adrs = userDetails['Address']
        phn = userDetails['phone']
        curr = mysql.connection.cursor()
        curr.execute('INSERT INTO users(Name, Designation, Address, Phone) VALUES(%s,%s,%s,%s)',(name,dgn,adrs,phn))
        mysql.connection.commit()
        curr.close()
        return redirect('/')
@app.route('/Remove')
def remove():
    return render_template('Remove.html')

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['fname']
        curr = mysql.connection.cursor()
        resultValue= curr.execute('SELECT * FROM users where Name=%s',(name,))
        if resultValue > 0:
            curr.execute('DELETE FROM users where Name = %s', (name,))
            mysql.connection.commit()
        curr.close()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

