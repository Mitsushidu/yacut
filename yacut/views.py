from random import randrange

from flask import abort, flash, redirect, render_template, request

from yacut import app, db

from .forms import URLForm
from .models import URLMap

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def get_unique_short_id():
    unique_short_id = ''
    for i in range(6):
        unique_short_id += ALPHABET[randrange(0, len(ALPHABET) - 1)]
    print(unique_short_id)
    if URLMap.query.filter_by(short=unique_short_id).first():
        unique_short_id = get_unique_short_id()
    return unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    link = ''
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if short:
            short = short.replace(' ', '')
            if URLMap.query.filter_by(short=short).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form, link=link)
            if any(not c.isalnum() for c in short):
                flash('Предложенный вариант короткой ссылки содержит недопустимые символы.')
                return render_template('index.html', form=form, link=link)
            link = URLMap(
                original=original,
                short=short,
            )
        else:
            link = URLMap(
                original=original,
                short=get_unique_short_id(),
            )
        db.session.add(link)
        db.session.commit()
        short_link = request.url + link.short
        flash('Ваша новая ссылка готова:')
        flash(short_link, 'link')
        return render_template('index.html', form=form, link=link, short_link=short_link)
    return render_template('index.html', form=form, link=link)


@app.route('/<string:short_id>')
def redirect_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        abort(404)
    return redirect(link.original, code=302)