import os
from unittest import TestCase
from app import app
from models import db, connect_db, User
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///food_recipe_test'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///food_recipe_test')
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

with app.app_context():
    db.session.commit()
    db.drop_all()
    db.create_all()

class UserTests(TestCase):
    """Test user functions."""

    def setUp(self):
        """Clean up existing Users."""
        with app.app_context():
            User.query.delete()

    def tearDown(self):
        """Clean up any bad inserts."""
        with app.app_context():
            db.session.rollback()

    def test_home(self):
        """Display Homepage"""
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Welcome To Food Recipe Search!</h1>', html)

    def test_signup_form(self):
        """Display signup form."""
        with app.test_client() as client:
            res = client.get("/signup")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="join-message">Sign Up Today.</h2>', html)

    def test_create_user(self):
        """Sign up user."""
        with app.test_client() as client: 
            user = {"username": "TestUser", "password": "123456", "email": "testemail@yahoo.com", "first_name": "test", "last_name": "user"}
            res = client.post("/signup", data=user, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<img src="/static/images/default-pic.png" alt="TestUser"> Profile', html)

    def test_login_form(self):
        """Display login form."""
        with app.test_client() as client:
            res = client.post("/login")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary btn-block btn-lg">Log in</button>', html)

    def test_login_user(self):
        """Log a user in."""
        with app.test_client() as client:
            res = client.post("/login", data={"username": "TestUser", "password": "123456"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('<img src="/static/images/default-pic.png" alt="TestUser"> Profile', html)

    def test_saved_recipes(self):
        """Save a recipe"""
        with app.test_client() as client:
            client.post("/login", data={"username": "TestUser", "password": "123456"}, follow_redirects=True)
            
            res = client.get("/user/1/saved_recipes")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('<h3>Sorry, no saved recipes found</h3>', html)
            client.post("/recipe/1/save")
            res2 = client.get("/user/1/saved_recipes")
            html2 = res2.get_data(as_text=True)
            self.assertIn('<br>Fried Anchovies with Sage</a>', html2)

    def test_meal_plan(self):
        """Show a User's Meal Plan."""
        with app.test_client() as client:
            client.post("/login", data={"username": "TestUser", "password": "123456"}, follow_redirects=True)

            res = client.get("/user/1/meal_plan")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('<h2>Currently, No Plan Has Been Made Yet.</h2>', html)


class RecipeTests(TestCase):
    """Test recipe functions."""

    def setUp(self):
        """Clean up existing Users."""
        with app.app_context():
            User.query.delete()

    def tearDown(self):
        """Clean up any bad inserts."""
        with app.app_context():
            db.session.rollback()

    def test_show_all_cuisine(self):
        """Display list of all cuisines"""
        with app.test_client() as client:
            res = client.get("/cuisine/all")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn("<h1>List of Cuisines</h1>", html)

    def test_search_recipe(self):
        """Search for a recipe"""
        with app.test_client() as client:
            res = client.get("/search/test/page=1")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn("<h1>Showing results for test</h1>", html)

    def test_view_recipe(self):
        """View details of a recipe"""
        with app.test_client() as client:
            res = client.get("/recipe/1")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn("<h3>Instructions</h3>", html)
