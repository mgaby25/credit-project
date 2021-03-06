from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class BaseAgencyForm(Form):
    name = StringField('Nume', validators=[DataRequired(), Length(1, 64)])
    address = StringField('Adresa', validators=[DataRequired(), Length(1, 64)])


class AddAgencyForm(BaseAgencyForm):
    submit = SubmitField('Adauga')


class EditAgencyForm(BaseAgencyForm):
    update = SubmitField('Salveaza')
    delete = SubmitField('Sterge')


class BaseCompanyForm(Form):
    cif = StringField('CIF', validators=[DataRequired(), Length(1, 64)])
    name = StringField('Nume', validators=[DataRequired(), Length(1, 64)])
    address = StringField('Adresa', validators=[DataRequired(), Length(1, 64)])
    city = StringField('Oras', validators=[DataRequired(), Length(1, 64)])
    state = StringField('Judet', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Telefon', validators=[DataRequired(), Length(1, 64)])
    registration_id = StringField('Nr. de inregistrare', validators=[DataRequired(), Length(1, 64)])


class AddCompanyForm(BaseCompanyForm):
    submit = SubmitField('Salveaza')


class EditCompanyForm(BaseCompanyForm):
    update = SubmitField('Salveaza')
    delete = SubmitField('Sterge')