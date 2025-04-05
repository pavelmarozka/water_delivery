from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Войти')

class DeliveryRecordForm(FlaskForm):
    time = StringField('Время', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[
        DataRequired(),
        NumberRange(min=1, message="Минимум 1 бутыль")
    ])
    amount = FloatField('Сумма', validators=[DataRequired()])
    payment_type = SelectField('Тип оплаты',
                             choices=[('нал', 'Наличные'), ('перевод', 'Перевод')],
                             validators=[DataRequired()])
