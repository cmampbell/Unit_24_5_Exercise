from flask import Flask, session, flash, jsonify, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback 
from forms import NewUserForm, LoginForm, FeedbackForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'AdoptDontShop'
app.config['DEBUG_TB_INTERCEPT-REDIRECTS'] = False
# app.run(debug=True)
debug = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_register():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    form = NewUserForm()

    if form.validate_on_submit():
        data = form.data
        new_user = User.register(data)

        db.session.add(new_user)
        db.session.commit()

        # session['current_user'] = new_user.serialize()
        session['current_user'] = new_user.username

        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.login(form.data)
        except:
            flash('Invalid username/password')
            return redirect('/login')
        
        if user != None:
            session['current_user'] = user.username
            return redirect(f'/users/{user.username}')

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user_details(username):
    user = User.query.get_or_404(username)
    if 'current_user' in session and session['current_user'] == username:
        return render_template('user_details.html', user=user)
    elif 'current_user' in session and session['current_user'] != username:
        flash("You don't have permission to view that user")
        return redirect(f"/users/{session['current_user']}")
    else:
        flash('Please log in')
        return redirect('/login')
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'current_user' in session and session['current_user'] == username:
        user = User.query.get_or_404(username)

        db.session.delete(user)
        db.session.commit()

        session.pop('current_user')

        flash(f"Deleted user {user.username}")

        return redirect('/login')
    elif 'current_user' in session and session['current_user'] != username:
        flash("You don't have permission to delete that user")
        return redirect(f"/users/{session['current_user']}")
    else:
        flash("You don't have permission to delete that user")
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'current_user' in session and session['current_user'] == username:
        form = FeedbackForm()

        if form.validate_on_submit():
            data = form.data
            new_feedback = Feedback.create_feedback(data, username)

            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{username}')

        return render_template('add_feedback.html', form=form, username=username)
    else:
        return redirect('/login')
    
@app.route('/logout')
def log_out_user():
    session.pop('current_user')
    return redirect('/login')
    
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    if 'current_user' in session:
        feedback = Feedback.query.get_or_404(feedback_id)

        if feedback.user.username == session['current_user']:
            form = FeedbackForm(obj=feedback)

            if form.validate_on_submit():
                data = form.data
                feedback.title = data['title']
                feedback.content = data['content']

                db.session.add(feedback)
                db.session.commit()

                return redirect(f'/users/{feedback.user.username}')

            return render_template('add_feedback.html', form=form, feedback=feedback)
        
        else:
            flash("You don't have permission to view that feedback")
            return redirect(f"/users/{session['current_user']}")
    else:
        return redirect('/login')
    
@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'current_user' in session:
        feedback = Feedback.query.get_or_404(feedback_id)

        if feedback.user.username == session['current_user']:
            db.session.delete(feedback)
            db.session.commit()

            flash("You have deleted the feedback")
            return redirect(f"/users/{session['current_user']}")
        else:
            flash("You don't have permission to delete that feeback")
            return redirect(f"/users/{session['current_user']}")
    else:
        return redirect('/login')