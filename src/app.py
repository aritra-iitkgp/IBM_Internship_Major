from flask import Flask,render_template,redirect,request,flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd
import json
from datetime import datetime,timezone
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__,
            template_folder='../templates', 
            static_folder='../static')
database_url = os.environ.get("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal/ibm_elytespark'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY")
db = SQLAlchemy(app)

class ibm_employee(db.Model):
    sno = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    Name = db.Column(db.String(50),nullable=False)
    Email = db.Column(db.String(50),nullable=False,unique=True)
    Password = db.Column(db.String(50),nullable=False)
    Datetime = db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, "config.json"), 'r') as f:
    param = json.load(f)['contents']

with app.app_context():
    db.create_all()

@app.route("/create-tables")
def create_tables():
    db.create_all()
    return "Tables created"

@app.route("/")
def home():
    return render_template('index.html',params=param)

@app.route("/blog-intro")
def intro():
    return render_template('blog_intro.html',params=param)

@app.route("/signup",methods=['GET','POST'])
def signup():

    if request.method=='POST':
       name=request.form.get("name")
       email=request.form.get("email")
       passwd=request.form.get("password")
       cnmpasswd=request.form.get("confirm_password")
      
       if passwd == cnmpasswd:
           obj = ibm_employee(Name=name,Email=email,Password=passwd)
           db.session.add(obj)
           db.session.commit()
           return redirect("/signin")
    return render_template('signup.html',params=param)

@app.route("/signin",methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        found = ibm_employee.query.filter_by(Email=email).first()
        if found == None:
            return redirect('/signup')
        else:
            if found.Password == passwd:
                return redirect("/machinelearningmodel")
            else:
                return redirect('/signin')

            
    return render_template('signin.html',params=param)

@app.route("/post",methods=["GET","POST"])
def post():
    return render_template('post.html',params=param)
@app.route("/about",methods=["GET","POST"])
def about():
    return render_template('about.html',params=param)
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Email content
        subject = f"New Contact Form Message from {name}"
        body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
        """

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = os.environ.get('EMAIL_ADDRESS')          # Your email
        msg['To'] = os.environ.get('EMAIL_ADDRESS')            # Where you want to receive it
        msg['Subject'] = subject
        msg['Reply-To'] = email
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Gmail SMTP example
            print("Connecting to Gmail SMTP...")
            server = smtplib.SMTP('smtp.gmail.com', 587,timeout=20)
            server.starttls()
            print("Logging in...")
            server.login(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD'))  # Use App Password
            server.send_message(msg)
            server.quit()

            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print("Error:", e)
            flash("Sorry, something went wrong. Please try again later.", "danger")

        return redirect("/contact")

    return render_template('contact.html', params=param)


@app.route("/machinelearningmodel", methods=['GET', 'POST'])
def ml_model():
    prediction = None
    selected_model = None

    if request.method == 'POST':
        # Collect form data
        form_data = {
            'SeniorCitizen': int(request.form.get('SeniorCitizen')),
            'MonthlyCharges': float(request.form.get('MonthlyCharges')),
            'TotalCharges': float(request.form.get('TotalCharges')),
            'gender': request.form.get('gender'),
            'Partner': request.form.get('Partner'),
            'Dependents': request.form.get('Dependents'),
            'PhoneService': request.form.get('PhoneService'),
            'MultipleLines': request.form.get('MultipleLines'),
            'InternetService': request.form.get('InternetService'),
            'OnlineSecurity': request.form.get('OnlineSecurity'),
            'OnlineBackup': request.form.get('OnlineBackup'),
            'DeviceProtection': request.form.get('DeviceProtection'),
            'TechSupport': request.form.get('TechSupport'),
            'StreamingTV': request.form.get('StreamingTV'),
            'StreamingMovies': request.form.get('StreamingMovies'),
            'Contract': request.form.get('Contract'),
            'PaperlessBilling': request.form.get('PaperlessBilling'),
            'PaymentMethod': request.form.get('PaymentMethod'),
            'tenure_group': request.form.get('tenure_group')
        }

        # Convert to DataFrame
        input_df = pd.DataFrame([form_data])

        # One-hot encoding
        input_encoded = pd.get_dummies(input_df)

        # Load saved column order
        with open("models/model_columns.pkl", "rb") as f:
            model_columns = pickle.load(f)

        # Match training columns
        input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

        # Load selected model
        selected_model = request.form.get('model_name')
        model_path = f"models/{selected_model}"

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        # Predict
        result = model.predict(input_encoded)[0]
        prediction = "Churn" if result == 1 else "No Churn"

    return render_template(
        'machinelearning.html',
        params=param,
        prediction=prediction,
        selected_model=selected_model
    )
                           
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port)