from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length

CUISINE_CHOICES = [("african", "African"), ("asian", "Asian"), ("american", "American"), ("british", "British"), ("cajun", "Cajun"), ("caribbean", "Caribbean"), ("chinese", "Chinese"), ("eastern european", "Eastern European"), ("european", "European"), ("french", "French"), ("german", "German"), ("greek", "Greek"), ("indian", "Indian"), ("irish", "Irish"), ("italian", "Italian"), ("japanese", "Japanese"), ("jewish", "Jewish"), ("korean", "Korean"), ("latin american", "Latin American"), ("mediterranean", "Mediterranean"), ("mexican", "Mexican"), ("middle eastern", "Middle Eastern"), ("nordic", "Nordic"), ("southern", "Southern"), ("spanish", "Spanish"), ("thai", "Thai"), ("vietnamese", "Vietnamese")]

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('(Optional) Image URL')

class RecipeAddForm(FlaskForm):
    """Form for adding new recipe."""

    title = StringField("Title", validators=[DataRequired()])
    image = TextAreaField("Image URL", validators=[DataRequired()])
    summary = TextAreaField("(Optional) Summary")
    instructions =TextAreaField("Instructions", validators=[DataRequired()])
    cuisine = SelectField("Type of Cuisine", choices=CUISINE_CHOICES)
    servings = IntegerField("Servings", validators=[DataRequired()])
    ready = IntegerField("Ready In Minutes", validators=[DataRequired()])

class RecipeEditForm(FlaskForm):
    """Form for editting a recipe."""

    title = StringField("Title", validators=[DataRequired()])
    summary = TextAreaField("(Optional) Summary")
    instructions =TextAreaField("Instructions", validators=[DataRequired()])
    cuisine = SelectField("Type of Cuisine", choices=CUISINE_CHOICES)

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class MealAddForm(FlaskForm):
    """Form for adding a new meal plan."""

    title = StringField("Title of Recipe", validators=[DataRequired()])
    day = SelectField("Day of the week", choices=[("monday", "Monday"), ("tuesday", "Tuesday"), ("wednesday", "Wednesday"), ("thursday", "Thursday"), ("friday", "Friday"), ("saturday", "Saturday"), ("sunday", "Sunday")])
    meal = SelectField("Type of meal", choices=[("breakfast", "Breakfast"), ("lunch", "Lunch"), ("dinner", "Dinner")])

class RefrigeratorForm(FlaskForm):
    """Form for adding new ingredients to the refrigerator."""

    title = StringField("Ingredient", validators=[DataRequired()])
    