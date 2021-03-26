from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key" # can be anything
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/FlaskCRUD'
# database://username:'password'@localhost/DatabaseName
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # If it's not False, sqlalchemy will send warnings

db = SQLAlchemy(app)

class Employee(db.Model): # Table Class
    empId = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(100))
    empEmail = db.Column(db.String(100))
    empPhone = db.Column(db.String(100))

    def __init__(self, empName, empEmail, empPhone):
        self.empName = empName
        self.empEmail = empEmail
        self.empPhone = empPhone


db.create_all() # To create Table

@app.route('/')
def index():
    all_data = Employee.query.all()

    return render_template('index.html', employees_all_data = all_data)

@app.route('/insert/', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Employee(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash('Employee inserted successfully !!!')

        return redirect(url_for('index'))

@app.route('/update/', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))

        my_data.empName = request.form['name']
        my_data.empEmail = request.form['email']
        my_data.empPhone = request.form['phone']

        db.session.commit()
        flash('Updated Successfully !!!')

        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)

    db.session.commit()
    flash('Deleted Successfully !!!')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)