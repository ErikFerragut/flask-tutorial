from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange, Length
from wtforms import StringField, IntegerField, SelectMultipleField, \
     RadioField, TextAreaField, PasswordField, SubmitField, HiddenField



class RequestForm(FlaskForm):
    '''Form to allow users to request an animal to be added to the site.'''
    name  = StringField('Requested animal', [InputRequired()])

    scale = IntegerField('Awesomeness on a scale of 1-10',
        [NumberRange(min=1, max=10)] )

    power = SelectMultipleField("Animal's special power", choices = [
        ("speed", "Speed"), ("str", "Strength"), ("regen", "Regeneration"),
        ("invis", "Invisibility"), ("other", "Something Else") ])

    first = RadioField('Is this your first request?',
        [InputRequired(message="Law of Excluded Middle Violated")],
        choices = [ ('yes', 'Yes'), ('no', 'No') ])

    reason = TextAreaField('Why is this animal interesting? (100 characters max)',
        [Length(min=0,max=100)])

    submit = SubmitField()

class LoginForm(FlaskForm):
    '''A very basic login form.'''
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField()

    
class LogoutForm(FlaskForm):
    '''Just a submit button that says Log Out'''
    logout = SubmitField("Log Out")


class NewAnimalForm(FlaskForm):
    '''Create a new animal entry in the repository'''
    name = StringField('Animal Name', [InputRequired()])
    source_url = StringField('Source URL', [InputRequired()])
    image_url = StringField('Image URL', [InputRequired()])
    image_desc = StringField('Image Description', [InputRequired()])
    funfact1 = StringField('Fun Fact 1',
        [InputRequired(message="Must provide at least one fact.")])
    funfact2 = StringField('Fun Fact 2')
    funfact3 = StringField('Fun Fact 3')
    funfact4 = StringField('Fun Fact 4')
    funfact5 = StringField('Fun Fact 5')
    funfact6 = StringField('Fun Fact 6')
    submit = SubmitField()
    action = HiddenField()
