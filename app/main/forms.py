from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField, DecimalField
from wtforms.validators import Required, Length, Email, Regexp, NumberRange
from wtforms_components import IntegerField as Html5IntegerField, read_only
from wtforms import ValidationError
from ..models import Role, User, Agency


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Nume', validators=[Length(0, 64)])
    location = StringField('Locatie', validators=[Length(0, 64)])
    about_me = TextAreaField('Despre mine')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    agency = SelectField('Agency', validators=[Required()], coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(Role.AGENT, 'Agent'), (Role.ADMINISTRATOR, 'Administrator')]
        self.agency.choices = [(agency.id, agency.name)
                               for agency in Agency.query.order_by('name')]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class AppointmentForm(Form):
    name = StringField('Nume', validators=[Length(0, 64)])
    email = StringField('Email', validators=[Length(0, 64), Email()])
    phone = IntegerField('Telefon', validators=[Required()])
    details = TextAreaField('Detalii (optional)')
    agency = SelectField('Agentia', validators=[Required()], coerce=int)
    submit = SubmitField('Trimite')

    def __init__(self):
        super(AppointmentForm, self).__init__()
        self.agency.choices = [(agency.id, agency.name)
                               for agency in Agency.query.order_by('name')]


class CompanyAppointmentForm(Form):
    company_name = StringField('Compania', validators=[Length(0, 64)])
    company_cif = StringField('CIF', validators=[Required(), Length(0, 64)])
    company_email = StringField('Email', validators=[Length(0, 64), Email()])
    company_phone = IntegerField('Telefon', validators=[Required()])
    company_details = TextAreaField('Detalii (optional)')
    company_agency = SelectField('Agentia', validators=[Required()], coerce=int)
    company_submit = SubmitField('Trimite')

    def __init__(self):
        super(CompanyAppointmentForm, self).__init__()
        self.company_agency.choices = [(agency.id, agency.name)
                                       for agency in Agency.query.order_by('name')]


class CreditType:
    CREDIT_EXPRESSO = 1
    PRIMA_CASA = 2
    CREDIT_IMOBILIAR = 3
    CREDIT_REFINANTARE = 4


class CreditCurrency:
    RON = 1
    EUR = 2


class CreditSimulatorForm(Form):
    credit_type = SelectField('Tipul creditului', validators=[Required()],
                              choices=[(CreditType.CREDIT_EXPRESSO, 'Credit Expresso (nevoi personale)'),
                                       (CreditType.PRIMA_CASA, 'Prima Casa'),
                                       (CreditType.CREDIT_IMOBILIAR, 'Credit Imobiliar Ipotecar'),
                                       (CreditType.CREDIT_REFINANTARE, 'Credit Refinantare')], coerce=int)
    amount = IntegerField('Suma', validators=[Required()])
    currency = SelectField('Moneda', choices=[(CreditCurrency.RON, 'RON'),
                                              (CreditCurrency.EUR, 'EUR')], coerce=int)
    duration = Html5IntegerField('Durata in luni', validators=[Required(), NumberRange(6, 360)])
    submit = SubmitField('Submit')


class CreditSimulatorResult(Form):
    rate = StringField('Rata lunara')
    dobanda = StringField('Dobanda lunara')
    total_amount = StringField('Suma totala de plata')

    def __init__(self):
        super(CreditSimulatorResult, self).__init__()
        read_only(self.rate)
        read_only(self.dobanda)
        read_only(self.total_amount)