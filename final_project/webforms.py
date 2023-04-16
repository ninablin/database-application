from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.widgets import TextArea

class SearchForm(FlaskForm):
     searched = StringField("Searched")
     submit = SubmitField("Submit")