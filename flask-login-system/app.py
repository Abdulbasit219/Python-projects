from flask import Flask, render_template, request, redirect, url_for
import requests
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
Base_url = "https://jsonplaceholder.typicode.com"
app.config["SECRET_KEY"] = "adsknfjksdfwjejfdslkdf;slkd;a"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users_db = [
    {
        "username": "user123",
        "password": "abcd"
    },
    {
        "username": "user456",
        "password": "abcd"
    }
]

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        
@login_manager.user_loader
def load_user(username):
    for user in users_db:
        if user['username'] == username:
            return User(username)
        else:
            return None 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get('password')
        
        for user in users_db:
            if user['username'] == username and user['password'] == password:
                user = User(username)
                login_user(user)
                return redirect(url_for("user"))
            else:
                return render_template('error.html')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/user")
@login_required
def user():
    try:
        response = requests.get(f'{Base_url}/users/')
        users = response.json()
        # return render_template('users.html', data= users)
        return render_template('users.html', data=users)
    except Exception as e:
        return render_template("error.html", error=e)
    
@app.route("/user/<int:user_id>")
@login_required
def user_detail(user_id):
    try:
        response = requests.get(f'{Base_url}/users/{user_id}')
        user = response.json()
        return render_template("user_details.html", user=user)
    except Exception as e:
        return render_template("error.html", message=f"Error fetching user: {e}"), 500

if __name__ == "__main__":
    app.run(debug=True)
