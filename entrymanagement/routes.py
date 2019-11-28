from entrymanagement import app, db, bcrypt
from flask import render_template, flash, url_for, redirect, request
from datetime import datetime
from entrymanagement.forms import (
    LoginForm,
    RegistrationForm,
    CheckInForm,
    CheckOutForm,
    UpdateAccountForm,
    PasswordChangeForm,
)
from entrymanagement.models import Host, GuestCheckIn
from flask_login import login_user, current_user, logout_user, login_required
from entrymanagement.helpers import (
    send_mail_to_host,
    send_mail_to_guest,
    send_message,
    getdate,
    get_time_from_timestamp,
)

# from flask_admin.contrib.sqla import ModelView
# from entrymanagement import admin

# admin.add_view(ModelView(Host, db.session))
# admin.add_view(ModelView(GuestCheckIn, db.session))

app.jinja_env.filters["getdate"] = getdate
app.jinja_env.filters["get_time_from_timestamp"] = get_time_from_timestamp


@app.route("/")
def home():
    # return "hello world"
    return render_template("home.html")


@app.route("/about")
def about():
    # return "about page"
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # checking if the host with same username or email already exist.
        user = Host.query.filter(
            (Host.username == form.username.data.strip())
            | (Host.email == form.email.data.strip())
        ).first()
        # print(user)
        if user is not None:
            flash("Host with the same username or email already exist!", "danger")
            return redirect(url_for("register"))

        # otherwise, add the host to the database.
        user = Host(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            phone_no=form.phone_no.data,
            address=form.address.data.strip(),
            password_hash=bcrypt.generate_password_hash(
                form.password.data.strip()
            ).decode("utf-8"),
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Host.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("account", username=user.username))
        else:
            flash("Login Unsuccessful. Please check your credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account/<username>")
@login_required
def account(username):
    user = Host.query.filter_by(username=username).first()
    if not user:
        flash("The user does not exist", "info")
        return redirect(url_for("account", username=current_user.username))
    return render_template("account.html", user=user, username=username)


@app.route("/account/<username>/guests")
@login_required
def guests(username):
    host = Host.query.filter_by(username=username).first()
    if not host:
        flash("The user does not exist", "info")
        return redirect(url_for("account", username=current_user.username))
    # return render_template("guest.html", user=user, username=username)
    guests = GuestCheckIn.query.filter_by(host_id=host.id).all()
    guests.reverse()
    return render_template("guests.html", guests=guests)


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = CheckInForm()
    host_names = [(user.username, user.username) for user in Host.query.all()]
    form.host_name.choices = host_names
    if form.validate_on_submit():
        # checking for a guest with same email that may be already checked in
        host = Host.query.filter_by(username=form.host_name.data).first()
        guest = (
            GuestCheckIn.query.filter_by(email=form.email.data)
            .filter_by(host_id=host.id)
            .filter_by(status="checked_in")
            .first()
        )
        if guest is not None:
            # if guest already checked in, show error
            flash("The guest with this email has already checked in!", "danger")
            return redirect(url_for("checkin"))

        # adding the checkin detail in the database
        guest_check_in = GuestCheckIn(
            guestname=form.guestname.data,
            phone_no=form.phone_no.data,
            email=form.email.data,
            status="checked_in",
            host_id=host.id,
        )
        db.session.add(guest_check_in)
        db.session.commit()
        send_mail_to_host(host, guest_check_in)
        send_message(host, guest_check_in)
        flash(
            "You have successfully checked in. Notification mail and message sent to the host",
            "success",
        )
        return redirect(url_for("checkin"))

    return render_template("checkin.html", form=form)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = CheckOutForm()
    host_names = [(user.username, user.username) for user in Host.query.all()]
    form.host_name.choices = host_names
    if form.validate_on_submit():
        # checking if the guest had checkedin
        host = Host.query.filter_by(username=form.host_name.data).first()
        guest = (
            GuestCheckIn.query.filter_by(email=form.email.data)
            .filter_by(status="checked_in")
            .filter_by(host_id=host.id)
            .first()
        )
        if guest is None:
            # if guest had not checked in, show error
            flash(
                "There is no guest with this email that has checked in for this host!",
                "danger",
            )
            return redirect(url_for("checkout"))

        # updating the guest data with the checkout time.
        guest.status = "checked_out"
        guest.checkout_timestamp = datetime.utcnow()
        db.session.commit()
        send_mail_to_guest(host, guest)
        flash(
            "You have successfully checked out. Mail with details sent to you.",
            "success",
        )
        return render_template("checkout.html", form=form)

    return render_template("checkout.html", form=form)


@app.route("/account/update", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccountForm()
    user = current_user
    print(current_user)
    if form.validate_on_submit():
        user.username = form.username.data.strip()
        current_user.email = form.email.data.strip()
        user.phone_no = form.phone_no.data
        user.address = form.address.data.strip()
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_no.data = current_user.phone_no
        form.address.data = current_user.address
    return render_template(
        "update_account.html", title="Account", user=user, form=form,
    )


@app.route("/account/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        check_current_password = bcrypt.check_password_hash(
            current_user.password_hash, form.current_password.data
        )
        if not check_current_password:
            flash("Your current password does not match", "danger")
            return redirect(url_for("change_password"))
        current_user.password_hash = bcrypt.generate_password_hash(
            form.new_password.data
        ).decode("utf-8")
        db.session.commit()
        flash("Your Password Has Been changed!", "success")
        return redirect(url_for("change_password"))
    return render_template("change_password.html", form=form)
