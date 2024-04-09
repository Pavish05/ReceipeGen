from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.Text, nullable=False, unique=True) # Todo: implement an email validation here.

    username = db.Column(db.Text, nullable=False, unique=True) # Todo: implement username validation (like checking for length/special characters)

    first_name = db.Column(db.String(), nullable=False)

    last_name = db.Column(db.String(), nullable=False)

    image_url = db.Column(db.Text, default="/static/images/default-pic.png")

    header_image_url = db.Column(db.Text, default="/static/images/warbler-hero.jpg")

    bio = db.Column(db.Text)

    password = db.Column(db.String(60), nullable=False)

    saved_recipes = db.Column(db.Integer, db.ForeignKey('recipes.id', name="users_saved_recipes_fk", ondelete='cascade'))

    recipe = db.relationship("Recipe", backref="user", cascade="all,delete", primaryjoin="User.id == Recipe.created_by")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url, first_name, last_name):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
class Recipe(db.Model):
    """Details of recipe with description and instructions."""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    image = db.Column(db.Text, nullable=False)

    summary = db.Column(db.Text, nullable=False, unique=True)

    cuisine = db.Column(db.Text, nullable=False)

    instructions = db.Column(db.Text, nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id', name="users_recipe_fk", ondelete='cascade'), nullable=False) 

    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False) 

    api_id = db.Column(db.Integer, nullable=False, unique=True)

class Shopping_Cart(db.Model):
    """Holds ingredients a user plans to buy."""

    __tablename__ = 'shopping-cart'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.Text, nullable=False, unique=True) 

    user = db.relationship('User', backref='shopping_cart')

class Meal_Plan(db.Model):
    """Info with a User's 'To-Eat-List' for a give day for a week."""

    __tablename__ = 'meal-plan'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    recipe_id = db.Column(db.Integer, nullable=False)
    recipe_name = db.Column(db.Text, nullable=False)
    # consider creating a foreign key relationship with Recipe to reduce redundancy

    day = db.Column(db.String(), nullable=False, ) 

    meal = db.Column(db.String(), nullable=False)

    user = db.relationship('User', backref='meal_plan')


class Cuisine(db.Model):
    """Category for cuisines."""

    __tablename__ = 'cuisines'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False, unique=True)
