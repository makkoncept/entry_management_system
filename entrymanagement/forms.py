from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from entrymanagement.models import Host
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=20)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=5, max=120)]
    )
    phone_no = IntegerField(
        "Phone No.",
        validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)],
    )
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=5, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=5, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=5, max=120)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class CheckInForm(FlaskForm):
    choices = []
    guestname = StringField(
        "Guest Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=5, max=120)]
    )
    phone_no = IntegerField(
        "Phone No.",
        validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)],
    )
    host_name = SelectField("Host Name", choices=choices)
    submit = SubmitField("Check In")

    def validate_email(self, email):
        host = Host.query.filter_by(email=email.data).first()
        if host:
            raise ValidationError("This email is registered as host email.")


class CheckOutForm(FlaskForm):
    choices = []
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=5, max=120)]
    )
    host_name = SelectField("Host Name", choices=choices)
    submit = SubmitField("Check Out")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=5, max=120)]
    )
    phone_no = IntegerField(
        "Phone No.",
        validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)],
    )
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=5, max=100)]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            host = Host.query.filter_by(username=username.data).first()
            if host:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            host = Host.query.filter_by(email=email.data).first()
            if host:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField(
        "Current Password", validators=[DataRequired(), Length(min=5, max=20)]
    )
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=5, max=20)]
    )
    repeat_new_password = PasswordField(
        "Repeat New Password", validators=[DataRequired(), EqualTo("new_password")]
    )
