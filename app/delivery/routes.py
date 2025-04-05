from flask import render_template, redirect, url_for, flash, request, jsonify, abort, make_response
from flask_login import login_required, current_user
from datetime import datetime, date
from app import db
from app.delivery.forms import DeliveryRecordForm, NoteForm
from app.models import DeliveryRecord
from app.delivery import bp
import pdfkit  # Добавлен новый импорт
import os

# Конфигурация PDF (укажите правильный путь к wkhtmltopdf)
PDF_CONFIG = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

@bp.route('/')
@login_required
def list_records():
    selected_date = request.args.get('date', date.today().isoformat())
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        date_obj = date.today()

    records = DeliveryRecord.query.filter_by(
        date=date_obj,
        user_id=current_user.id
    ).order_by(DeliveryRecord.time).all()

    totals = {
        'cash': sum(r.amount or 0 for r in records if r.payment_type == 'нал'),
        'cashless': sum(r.amount or 0 for r in records if r.payment_type == 'перевод'),
        'quantity': sum(r.quantity or 0 for r in records),
        'all': sum(r.amount or 0 for r in records)
    }

    return render_template('delivery/list.html',
                         records=records,
                         selected_date=selected_date,
                         totals=totals)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_record():
    form = DeliveryRecordForm()

    if form.validate_on_submit():
        try:
            record = DeliveryRecord(
                time=form.time.data,
                description=form.description.data,
                quantity=form.quantity.data,
                amount=form.amount.data,
                payment_type=form.payment_type.data,
                user_id=current_user.id,
                date=date.today()
            )
            db.session.add(record)
            db.session.commit()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'success',
                    'message': 'Запись добавлена!',
                    'id': record.id
                }), 200

            flash('Запись добавлена!', 'success')
            return redirect(url_for('delivery.list_records'))

        except Exception as e:
            db.session.rollback()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 400

            flash(f'Ошибка: {str(e)}', 'danger')

    return render_template('delivery/add.html', form=form)

@bp.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    selected_date = request.args.get('date', date.today().isoformat())  # Берём дату из URL

    if form.validate_on_submit():
        try:
            record = DeliveryRecord(
                time=form.time.data,
                note=form.note.data,
                is_note=True,
                user_id=current_user.id,
                date=datetime.strptime(selected_date, '%Y-%m-%d').date()  # Используем дату из URL
            )
            db.session.add(record)
            db.session.commit()
            flash('Заметка добавлена!', 'success')
            return redirect(url_for('delivery.list_records', date=selected_date))  # Передаём дату
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'danger')

    return render_template('delivery/add_note.html', form=form, selected_date=selected_date)  # Передаём дату в шаблон

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    record = DeliveryRecord.query.get_or_404(id)
    if record.user_id != current_user.id:
        abort(403)

    # Выбираем форму в зависимости от типа записи
    if record.is_note:
        form = NoteForm(obj=record)
    else:
        form = DeliveryRecordForm(obj=record)

    if form.validate_on_submit():
        try:
            if record.is_note:
                # Для заметок обновляем только time и note
                record.time = form.time.data
                record.note = form.note.data
            else:
                # Для обычных записей обновляем все поля
                form.populate_obj(record)
            db.session.commit()
            flash('Запись успешно обновлена!', 'success')
            return redirect(url_for('delivery.list_records', date=record.date.isoformat()))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка обновления: {str(e)}', 'danger')

    return render_template('delivery/edit.html', form=form, record=record)

@bp.route('/delete/<int:id>', methods=['POST', 'DELETE'])
@login_required
def delete_record(id):
    record = DeliveryRecord.query.get_or_404(id)
    if record.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(record)
        db.session.commit()
        if request.headers.get('HX-Request'):
            return '', 200
        flash('Запись удалена!', 'success')
    except Exception as e:
        if request.headers.get('HX-Request'):
            return str(e), 400
        flash(f'Ошибка: {str(e)}', 'danger')

    return redirect(url_for('delivery.list_records'))



@bp.route('/generate_pdf')
@login_required
def generate_pdf():
    selected_date = request.args.get('date', date.today().isoformat())
    records = DeliveryRecord.query.filter_by(
        date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
        user_id=current_user.id
    ).order_by(DeliveryRecord.time).all()

    totals = {
        'cash': sum(r.amount or 0 for r in records if r.payment_type == 'нал'),
        'cashless': sum(r.amount or 0 for r in records if r.payment_type == 'перевод'),
        'quantity': sum(r.quantity or 0 for r in records),
        'all': sum(r.amount or 0 for r in records)
    }

    html = render_template(
        'delivery/pdf_template.html',
        records=records,
        selected_date=selected_date,
        totals=totals,
        current_date=datetime.now().strftime("%Y-%m-%d")
    )

    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        'enable-local-file-access': None
    }

    pdf = pdfkit.from_string(html, False, configuration=PDF_CONFIG, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=route_list_{selected_date}.pdf'
    return response
