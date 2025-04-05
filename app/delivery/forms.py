from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

class DeliveryRecordForm(FlaskForm):
    time = StringField('Время (HH:MM)', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    amount = FloatField('Сумма', validators=[DataRequired(), NumberRange(min=0)])
    payment_type = SelectField('Тип оплаты',
                             choices=[('', 'Не выбран'), ('нал', 'Наличные'), ('перевод', 'Перевод')],
                             validators=[DataRequired()])
    submit = SubmitField('Сохранить')
