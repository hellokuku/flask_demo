


from flask import render_template

from . import auth
from flask import redirect, request, url_for, flash
from flask.ext.login import login_user
from flask.ext.login import logout_user, login_required
from .. import db
from ..models import User
from .forms import LoginForm, \
	RegistrationForm, ChangePasswordForm, \
	PasswordResetForm, PasswordResetRequestForm, ChangeEmailForm
from ..email import send_email
from flask.ext.login import current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)



@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email = form.email.data,
		            username = form.username.data,
		            password = form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account', 'auth/mail/confirm', user=user, token=token)
		flash('A Confirmation email has been sent to you by email.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():

	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5] !='auth.':
			return redirect(url_for('auth.unconfirmed'))


	# below are before chapter-10
	# if current_user.is_authenticated \
	# 	and not current_user.confirmed \
	# 	and request.endpoint[:5] !='auth.' \
	# 	and request.endpoint !='static':
	#
	# 	return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm your account', 'auth/mail/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to your by eamil.')
	return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			db.session.commit()
			flash('Your password has been updated!')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid password.')
	return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET','POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(form.email.data,
			           'Reset your password',
			           'auth/mail/reset_password',
			           user=user,
			           token=token,
			           next=request.args.get('next'))
		flash('An email with instructions to reset your password has been set to you.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET','POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash('Your password has been updated!')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET','POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email,
			           'confirm your email',
			           'auth/mail/change_email',
			           user=current_user,
			           token=token)
			flash('An email with instructions to confirm your new email addr to you by email ')
		else:
			flash('Invalid email or password.')
	return render_template('auth/change_email.html', user=current_user,form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('you email addr has been updated')
	else:
		flash('Invaild requests')

	return redirect(url_for('main.index'))
