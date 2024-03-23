from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Form(db.Model):
    sno = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    address = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f"{self.name}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        entry = Form(name=name, email=email, phone=phone,address=address)
        db.session.add(entry)
        db.session.commit()   
    
    allData = Form.query.all()
    return render_template('index.html', allData=allData)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        entry = Form.query.filter_by(sno=sno).first()
        entry.name = name
        entry.email = email
        entry.phone = phone
        entry.address = address
        db.session.add(entry)
        db.session.commit()
        return redirect("/")

    entry = Form.query.filter_by(sno=sno).first()
    return render_template('update.html', entry=entry)

@app.route('/delete/<int:sno>')
def delete(sno):
    entry = Form.query.filter_by(sno=sno).first()
    db.session.delete(entry)
    db.session.commit()  
    return redirect("/")

if __name__ == "__main__" :
    app.run(debug=True)