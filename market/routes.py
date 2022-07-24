from market import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages,request
from market.models import CourseName,User
from market.forms import RegisterForm, LoginForm, CourseForm
from flask_login import login_user, logout_user, login_required, current_user
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/course_register',methods=['GET','POST'])
@login_required
def course_page():
    form = CourseForm()
    if request.method=="POST":
        if form.validate_on_submit():
            try:
                course_to_create = CourseName(batch=form.batch.data,
                                regulartype=form.regulartype.data,
                                cname=form.cname.data,
                                owner=current_user.id)
                db.session.add(course_to_create)
                db.session.commit()
                flash(f'Course Registered Successfully!!',category='success')
                
            except:
                 if form.errors != {}: #if there are no erro
                    for err_msg in form.errors.values():
                        flash(f' There was an error with registation { err_msg }',category='danger') 
       
        return render_template('home.html')  
    return render_template('course.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created Successfully!! You are now loggedin as: { user_to_create.username}',category='success')
            
        return redirect(url_for('course_page'))

    if form.errors != {}: #if there are no errors
        for err_msg in form.errors.values():
            flash(f' There was an error with creating a user { err_msg }',category='danger')   
        
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                    attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: { attempted_user.username}',category='success')
            return redirect(url_for('course_page'))
        else:
            flash('Username and password not match!! Try again!!',category='danger')

    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have loggedout!!',category='info')
    return redirect(url_for('home_page'))

@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_page(id):
    post = CourseName.query.get_or_404(id)
    form = CourseForm()
    if form.validate_on_submit():
        post.batch = form.batch.data
        post.regulartype = form.regulartype.data
        post.cname = form.cname.data
        db.session.add(post)
        db.session.commit()
        flash(f'Course Updated Successfully!!',category='success')
        
        # if form.errors != {}: #if there are no errors
        #     for err_msg in form.errors.values():
        #         flash(f' There was an error with creating a user { err_msg }',category='danger')   
        return redirect(url_for('course_view'))
    form.batch.data = post.batch
    form.regulartype.data = post.regulartype
    form.cname.data = post.cname
    return render_template('editcourse.html',form=form)

@app.route('/view',methods=['GET'])
@login_required
def course_view():
    post = CourseName.query.all()
    return render_template('viewcourses.html',post=post)

@app.route('/delete/<int:id>')
@login_required
def delete_item(id):
    post = CourseName.query.get_or_404(id)
    try:
        temp = post.id
        db.session.delete(post)
        db.session.commit()
        flash(f'Candidate with id={temp} is deleted!!',category='success')
        post = CourseName.query.all()
        if post:
            return render_template('viewcourses.html',post=post)
        return redirect(url_for('home_page'))

    except:
        db.session.rollback()
        flash(f'Whoops!! Problem with deletion Candidate with id{temp} !!',category='danger')
        post = CourseName.query.all()
        return render_template('viewcourses.html',post=post)



