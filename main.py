from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Configuration SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



# Routes
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


#Login Route
@app.route('/login', methods=['GET','POST'])
def login():
    # Get form data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template("index.html")  # You might want to add an error message here
        
        # Si la méthode est GET, renvoyer simplement le formulaire
    return render_template('index.html')

#Registration Route
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("index.html", error="User already exists")  # You might want to add an error message here
        else:
        # Create new user
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            session['username'] = username
            return redirect(url_for('dashboard'))
     # Si la méthode est GET, renvoyer simplement le formulaire
    return render_template('index.html')

#Dashboard Route
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))


#Logout Route
@app.route('/logout')
def logout():
    # Suppression de l'entrée 'username' de la session
    session.pop('username', None) 
    # Redirection vers la page d'accueil
    return render_template('index.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)