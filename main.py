from flask import redirect, url_for
from app import create_app

app = create_app()

# Redirect root URL (/) to /home
@app.route('/')
def index():
    return redirect(url_for('home.home_home'))  # Redirects to home_home route of the 'home' blueprint

if __name__ == '__main__':
    app.run(debug=True)