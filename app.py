import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for
import requests
from bs4 import BeautifulSoup
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserEditForm, RecipeAddForm, RecipeEditForm, LoginForm, MealAddForm, RefrigeratorForm
from models import db, connect_db, User, Meal_Plan, Shopping_Cart, Recipe, Cuisine

CURR_USER_KEY = "curr_user"
key = '4c38af58cbe74ecfac48f137ccfef40b' # this should be in a secret file, but for testing/grading purposes, I'll leave this here

app = Flask(__name__)
#app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = (
    #os.environ.get('DATABASE_URL', 'postgresql:///food'))
    os.environ.get('DATABASE_URL', 'postgresql://gbjvilsf:QpZbq8Aw5Uh3jTz_D8pII7IL0V8L-uDI@berry.db.elephantsql.com/gbjvilsf'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
#toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username/Email already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have been logged out.", "danger")
    return redirect("/login")


##############################################################################
# Turn off all caching in Flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    # Show random recipe
    res = requests.get("https://api.spoonacular.com/recipes/random?number=1", params={"apiKey": key}).json()
    recipes = get_random_recipe(res)

    # 'RESULTS': title, image, instructions, summary, extendedIngredients[id, name, original, unit, amount]
    return render_template('home.html', recipes=recipes)
    


##############################################################################
# Routes for recipes

def get_random_recipe(res):
    summary = res["recipes"][0]['summary']
    clean_summary = BeautifulSoup(summary, 'html.parser')

    recipes = {'id': res["recipes"][0]['id'], 
               'title': res["recipes"][0]['title'], 
               'image': res["recipes"][0]['image'], 
               'summary': clean_summary.get_text(), 
               'readyInMinutes': res["recipes"][0]['readyInMinutes'], 
               'servings': res["recipes"][0]['servings']
               }
    return recipes

def get_recipe(res):
    clean_summary = BeautifulSoup(res['summary'], 'html.parser')
    clean_instructions = BeautifulSoup(res['instructions'], 'html.parser')

    recipes = {
        'id': res['id'], 
        'title': res['title'], 
        'image': res['image'], 
        'instructions': clean_instructions.get_text(), 
        'summary': clean_summary.get_text(), 
        'extendedIngredients': res['extendedIngredients'], 
        'readyInMinutes': res['readyInMinutes'], 
        'servings': res['servings']
        } 
    return recipes

@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    """Show the recipe."""

    res = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/information", params={"apiKey": key}).json()
    recipe = get_recipe(res)

    return render_template('recipes/show.html', recipe=recipe, res=res)

@app.route('/recipe/add', methods=['GET', 'POST']) # # # # # NEEDS WORK
def add_recipe():
    """Form for handling adding new recipe."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = RecipeAddForm()

    if form.validate_on_submit():
        new_recipe = Recipe(
            title=form.title.data,
            image=form.image.data,
            summary=form.summary.data,
            cuisine=form.cuisine.data,
            instructions=form.instructions.data,
            created_by=g.user.id 
        )
        db.session.add(new_recipe)
        db.session.commit()
        flash(f"{new_recipe.title} added.")
        return redirect(url_for('homepage'))
    
    else:
        return render_template('recipes/add.html', form=form) # need to create this template  
    
@app.route('/recipe/edit/<int:recipe_id>', methods=['GET', 'POST']) # # # # # NEEDS WORK
def edit_recipe(recipe_id):
    """Edit recipe."""

    if not g.user:
        flash("Access unauthorized.", "danger") # not sure but need a way to check that the recipe is owned/saved by the user in order to edit
        return redirect("/login")
    
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeEditForm(obj=recipe)

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.summary = form.summary.data
        recipe.instructions = form.instructions.data
        recipe.cuisine = form.cuisine.data
        db.session.commit()
        flash(f"{recipe.title} updated.")
        return redirect(url_for('homepage'))
    
    else:
        return render_template("recipe/edit.html", form=form, recipe=recipe) # need to create this template
    
@app.route('/recipe/<int:recipe_id>/save', methods=['GET','POST']) # # # # # NEEDS WORK
def save_recipe(recipe_id):
    """Save this recipe to user."""

    if not g.user:
        flash("Please Log In To Save Recipes!", "danger")
        return redirect("/login")
    
    if Recipe.query.filter_by(api_id=recipe_id).first(): # check for this and if the recipe belongs to the user
        flash("You've already saved this recipe")
        return redirect(f"/recipe/{recipe_id}")

    res = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/information", params={"apiKey": key}).json()

    save = Recipe(
        title = res['title'],
        image = res['image'],
        summary = res['summary'],
        cuisine = res['cuisines'],
        instructions = res['instructions'],
        created_by = g.user.id,
        api_id= res['id']
    )

    db.session.add(save) 
    db.session.commit()

    return redirect(f'/user/{g.user.id}/profile')

#################################################################################
# User Routes

@app.route('/user/<int:user_id>/profile', methods=['GET'])
def user_show(user_id):
    """This is the logged in User's profile. Should show their areas with saved recipes, meal plan, and refrigerator."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)

    return render_template("users/profile.html", user=user)

@app.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    """Edit the user profile."""

    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')
    
    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data

            db.session.commit()
            return redirect(f"/user/{user_id}/profile")
        
        flash("Wrong Password, Please Try Again.", 'danger')

    return render_template("/users/edit.html", form=form, user_id=user.id)

@app.route('/user/<int:user_id>/saved_recipes') 
def show_saved_recipes(user_id):
    """Show all of a user's saved/created recipes."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    user = User.query.get_or_404(user_id)
    recipes = Recipe.query.filter_by(created_by=user_id).all()
    
    return render_template("users/saved-recipes.html", recipes=recipes, user=user)

@app.route('/user/<int:user_id>/saved_recipes/<int:recipe_id>/delete', methods=["GET","POST"])
def remove_recipe(user_id, recipe_id):
    """Remove this recipe from user's saved recipes."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')
    
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash("Removed recipe", "danger")
    return redirect(f'/user/{user_id}/saved_recipes')

@app.route('/user/<int:user_id>/meal_plan', methods=['GET'])
def show_user_plan(user_id):
    """Show this user's current plan over the week."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    plan = Meal_Plan.query.filter_by(user_id=user_id).all()
    
    return render_template("users/meal-plan.html", plan=plan)
    
@app.route('/user/<int:user_id>/meal_plan/<int:recipe_id>', methods=['GET', 'POST'])
def add_recipe_to_plan(user_id, recipe_id):
    """Show this user's current plan over the week."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    form = MealAddForm()

    if form.validate_on_submit():
        new_plan = Meal_Plan(
            user_id=user_id,
            recipe_id=recipe_id, # this is the api's id
            recipe_name=form.title.data,
            day=form.day.data,
            meal=form.meal.data
        )
        db.session.add(new_plan)
        db.session.commit()
        flash("New recipe has been added to plan.")
        return redirect(url_for('user_show', user_id=user_id))
    
    else:
        return render_template("users/add-meal.html", form=form) 

    
#############################################################################
# Search Routes

@app.route('/cuisine/all', methods=['GET'])
def show_all_cuisines():
    """Show all cuisines."""

    cuisines = Cuisine.query.all() # change this to an []

    return render_template("recipes/cuisines.html", cuisines=cuisines)

@app.route('/cuisine/<int:cuisine_id>', methods=['GET'])
def show_cuisine(cuisine_id):
    """Show recipes for certain cuisine"""

    return redirect(f'/cuisine/{cuisine_id}/page={1}')

@app.route('/cuisine/<int:cuisine_id>/page=<int:num>')
def cuisine_page(cuisine_id, num):
    """Determine what page user is going to view."""

    offset = 10 * num - 10
    next_page = num+1
    prev_page = num-1

    c_id = Cuisine.query.get_or_404(cuisine_id)

    cuisines = requests.get(f"https://api.spoonacular.com/recipes/complexSearch", params={"apiKey": key, "cuisine": c_id.name, "offset": offset }).json()

    return render_template("recipes/list.html", cuisines=cuisines, cuisine=c_id, next_page=next_page, prev_page=prev_page)

@app.route('/search', methods=['GET'])
def show_search():
    """Show recipes for certain cuisine"""

    query = request.args.get('q')
    return redirect(f'/search/{query}/page={1}')

@app.route('/search/<query>/page=<int:num>', methods=['GET', 'POST'])
def search(query, num):
    """Search for query."""

    offset = 10 * num - 10
    next_page = num+1
    prev_page = num-1

    res = requests.get(f"https://api.spoonacular.com/recipes/complexSearch", params={"apiKey": key, "query": query, "offset": offset }).json()

    return render_template("recipes/search.html", res=res, query=query, next_page=next_page, prev_page=prev_page)

@app.route('/search/strict/<int:user_id>', methods=['GET', 'POST'])
def strict_search(user_id):
    """Search using only the ingredients in a user's refrigerator."""

    testArray = []
    search = Shopping_Cart.query.filter_by(user_id=user_id).all()
    for index in search:
        testArray.append(index.title)
    res = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients", params={"apiKey": key, "ranking": 2, "ignorePantry": True, "ingredients": testArray}).json()
    return render_template("recipes/easy-search.html", res=res)


@app.route('/search/easy/<int:user_id>', methods=['GET', 'POST'])
def easy_search(user_id):
    """Search using the ingredients in a user's refrigerator."""

    testArray = []

    search = Shopping_Cart.query.filter_by(user_id=user_id).all()
    for index in search:
        testArray.append(index.title)

    res = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients", params={"apiKey": key, "ignorePantry": True, "ingredients": testArray}).json()

    return render_template("recipes/easy-search.html", res=res)


#############################################################################
# Refrigerator Routes

@app.route('/user/<int:user_id>/refrigerator', methods=['GET', 'POST'])
def user_refrigerator(user_id):
    """Shows what's in the User's refrigerator and uses this to search for recipes that include these items."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    refrigerator = Shopping_Cart.query.filter_by(user_id=user_id).all()

    return render_template("users/refrigerator.html", refrigerator=refrigerator)

@app.route('/user/<int:user_id>/refrigerator/add', methods=['GET', 'POST'])
def user_add_refrigerator(user_id):
    """Add items to the refrigerator."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = RefrigeratorForm()
    
    # this looks like i can only add stuff one at a time... which is bad...
    if form.validate_on_submit():
        res = requests.get(f"https://api.spoonacular.com/food/ingredients/search", params={"apiKey": key, "query":form.title.data, "number":1}).json()
        new_item = Shopping_Cart(
            user_id=user_id,
            title=res['results'][0]['name']
        )

        if Shopping_Cart.query.filter_by(title=new_item.title).first(): # check for this and if the recipe belongs to the user
            flash("You've already saved this recipe")
            return redirect(f"/user/{user_id}/refrigerator")
        
        db.session.add(new_item) # also need to catch an error in case there is a duplicate item
        db.session.commit()
        flash(f"{new_item.title} has been added to refrigerator.")
        return redirect(url_for('user_refrigerator', user_id=user_id))
    
    else:
        return render_template("users/add-refrigerator.html", form=form) 
    
@app.route('/user/<int:user_id>/refrigerator/<int:shopping_cart_id>/remove', methods=['GET', 'POST'])
def remove_refrigerator_ingredient(user_id, shopping_cart_id):
    """Remove an ingredient in the user's refrigerator."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    refrigerator = Shopping_Cart.query.get_or_404(shopping_cart_id)

    db.session.delete(refrigerator)
    db.session.commit()
    flash(f"Removed {refrigerator.title}", "info")
    return redirect(f'/user/{user_id}/refrigerator')
