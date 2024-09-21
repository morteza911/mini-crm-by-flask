from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = "3d9e24b8d32d657b579a129c5f1179f4c44593c3a16c90b7a01d8f442dac6704"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)  # فعال‌سازی CSRF Protection
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# تنظیمات مربوط به Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'register'  # روتی که به آن هدایت می‌شود اگر کاربر لاگین نباشد
login_manager.login_message_category = 'info'  # پیامی که نمایش داده می‌شود

from crm.models import User

# تابع user_loader برای بارگذاری کاربر بر اساس user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from crm import routes, models
