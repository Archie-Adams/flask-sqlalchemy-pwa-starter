# A generic Flask/PWA web app starting template

MIT Licence yada yada
## File explanation

## Setup

step1 Run `python3 db_create.py`.
- This creates the database and tables.
- It will work for any Flask-SQLAlchemy project.


## Some Flask views examples

```python
# r = models.  // models is a class of tables.

# r = models.Recipe. // Recipe is a table name

# r = models.Recipe.query.all() // r is now an array containing the table rows

# r = models.Recipe.query.filter_by(id=1).all()  // example of a filter by ID field



# This is all the code needed for a static page at 'sitename/help'
@app.route('/help')
def help(): # the function name is arbitrary, best practice to use a name like the URL
    # All that you need to return is a HTML string, e.g: return "<h1>Heading</h1>"
    # here we return the result of the function render_template().
    # render_template() takes a html template and fills in the blanks with its input,
    # here it fills in the title of the help.html page.
    # This looks kinda useless, but the help.html is itself put into a template
    # which consists of things like the sites header and footer, that should be the
    # same on every page. This reduces HTML writing by a lot.
    return render_template(
        'help.html',
        title = 'Recipe Manager - Help',
    )

# THIS IS WHAT help.html is. {% extends "base.html" %} means place this inside
# the block content in base.html. base.html just has a generic head, header and footer.


# {% extends "base.html" %}
# {% block content %}

# <body>
#   <div class="container mt-3">

#     <h1>Common FAQs:</h1>
#     <ul>
#       <li>
#         <h2>How do I book a scooter?</h2>
#         <p>Click on the scooter on the list, select a time span, pay.</p>
#       </li>
#     </ul>
#   </div>

# </body>

# {% endblock %}




# ------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def logIn():
    form = LogInForm() # A class defined in the Forms. This is generic, once
    # you have seen one, the process is the same for all.
    # We do forms like this to easily send data back to here.
    if form.validate_on_submit(): # If the forms validators (see below) are true
        user = User.query.filter_by(username=form.username.data).all()
        # above line means user variable is equal to a query on the User table filtered
        # by the user name inputted on the form.
        if user != []: # If the query was not empty
            login_user(user[0]) # built in login user function.
            return redirect("home", code=307) # redirect the user to the /home page.
    return render_template( # if the username was not in the database, or on first time load, sow the page.
        'login-signup.html',
        title = 'Recipe Manager - Log-In',
        form=form,
        login=True
    )

# THIS IS WHAT LOGINFORM ABOVE LOOKS LIKE
# class LogInForm(Form):
#     username = TextField('username', validators=[DataRequired()])
#     password = PasswordField('password', validators=[DataRequired()])
#     rememberMe = BooleanField('rememberMe')


@app.route('/logout')
@login_required # This /logout route will only be accessible to users who have done
# above login_user function. This and the logout_user() function is not coded by us.
def logout():
    logout_user()
    return redirect("/")


# ------------------------------------------------------------------------

# AJAX REQUESTS

@app.route('/respond_add-edit_recipe', methods=['POST', 'GET'])
@login_required
def respondAddEditRecipe():
    data = json.loads(request.data) # Data is being sent from the web page by Javascript

    user_id = current_user.id # The cuttent_user variable is handled by Flask automatically.

    # Add the data to a new record if no recipe id was provided.
    if (data.get('id')) == None:
        # Do some database query to add a new record.

        return json.dumps({
            'status': 'OK',
            'response': "Added recipe with id " + "420",
        })

    # Update an already existing record.
    else:
        # Do some database query to update a record.

        return json.dumps({
            'status': 'OK',
            'response': "Updated recipe with id " + "69",
        })
```