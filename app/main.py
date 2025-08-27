from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

# Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)

# Home Route
@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        short_url = request.host_url + short_code

        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

    return render_template('index.html', short_url=short_url)

# Redirect Short URL
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.long_url)
    else:
        return 'URL Not Found', 404

# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
