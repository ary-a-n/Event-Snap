from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_scss import Scss

app = Flask(__name__)
Scss(app)

# Configuration for the databases
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
app.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///database1.db',
    'db2': 'sqlite:///database2.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class dat(db.Model): #event_data
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(125), nullable=False)
    coordinator_name = db.Column(db.String(30), nullable=False)
    Conatct_info = db.Column(db.Integer(), nullable=False)
    pic_path = db.Column(db.String(700), nullable=False)

class dat1(db.Model): #cutsomer_data
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    dealership_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(125), nullable=False)
    customer_name = db.Column(db.String(30), nullable=False)
    mobile_num = db.Column(db.Integer(), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    occupation = db.Column(db.String(20), nullable=False)
    interest = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(20), default = datetime.utcnow)
    pic_path = db.Column(db.String(700), nullable=False)

with app.app_context():
    # Create tables for db1
    db.metadata.create_all(bind=db.get_engine(app, bind='db1'), tables=[dat.__table__])
    # Create tables for db2
    db.metadata.create_all(bind=db.get_engine(app, bind='db2'), tables=[dat1.__table__])

@app.route("/")
def index():
    return render_template("landing.html")


@app.route("/event-submission")
def eventer():
    return render_template("event.html")

@app.route('/submit-event', methods=['POST'])
def submit_event():
    event_name = request.form['Ename']
    location = request.form['location']
    coordinator_name = request.form['E_coordinator']
    Conatct_info = request.form['E_number']
    images = request.files.getlist('image')  # Retrieve list of uploaded files
    image_paths = []
    # Iterate through each uploaded image
    for image in images:
        if image.filename != '':
            timestamp = datetime.now().strftime('%Y-%m-%d')
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{event_name}_{timestamp}_{filename}")
            image.save(image_path)
            image_paths.append(image_path)

    # Create a new event object with the first image path
    new_event = dat(event_name=event_name, location=location, coordinator_name=coordinator_name,
                    Conatct_info=Conatct_info, pic_path=', '.join(image_paths))

    # Add new_event to session and commit to database
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('eventer'))

@app.route("/enquiry-submission")
def customer():
    return render_template("cust.html")

@app.route('/submit-customer', methods=['POST'])
def submit_customer():
    if request.method == 'POST':
        date = request.form['Date']
        Dealership_name = request.form['Dname']
        location = request.form['location']
        Customer_name = request.form['Customer_N']
        Contact_info = request.form['number']
        Gender = request.form['gender']
        Occupation = request.form['job']
        Interest = request.form['interest']
        images = request.files.getlist('Image')  # Retrieve list of uploaded files
        cust_paths = []
        # Iterate through each uploaded image
        for image in images:
            if image.filename != '':
                timestamp = datetime.now().strftime('%Y-%m-%d')
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{Dealership_name}_{location}_{timestamp}_{filename}")
                image.save(image_path)
                cust_paths.append(image_path)

        # Create a new event object with the first image path
        new_data = dat1(\
            date = date,
            dealership_name=Dealership_name,
            location=location,
            customer_name=Customer_name,
            mobile_num=Contact_info,
            Gender=Gender,
            occupation=Occupation,
            interest=Interest,
            pic_path=', '.join(cust_paths)
        )

        # Add to the database session
        db.session.add(new_data)
        db.session.commit()
    return redirect(url_for('customer'))

if __name__ == "__main__":
    app.run(debug=True)
