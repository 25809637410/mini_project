from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite 데이터베이스 경로 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Track modifications 비활성화
db = SQLAlchemy(app)

# 가상의 데이터베이스
# user_database = {
#     'user1': 'password1',
#     'user2': 'password2',
#     'user3': 'password3',
# }

# 사용자 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# 데이터베이스 생성
with app.app_context():
    db.create_all()
    # 사용자 추가
    users = [
        {'username': 'user1', 'password': 'password1'},
        {'username': 'user2', 'password': 'password2'},
        {'username': 'user3', 'password': 'password3'}
    ]

    for user_data in users:
        username = user_data['username']
        password = user_data['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login', methods = ['GET' ,'POST'])
def login():
    message = '' # 초기화된 메시지

    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        # 사용자 검증
        user = User.query.filter_by(username=userid, password=password).first()
        if user:
            return redirect(url_for('success'))
        else:
            message = '잘못된 사용자 이름 또는 비밀번호입니다.'

    return render_template('login.html', message=message)

@app.route('/success')
def success():
    return '로그인 성공!'

if __name__ == "__main__":
    app.run(debug=True)
