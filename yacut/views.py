from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    link = ''
    if not form.validate_on_submit():
        return render_template('index.html', form=form, link=link)
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


@app.route('/<string:short_id>')
def redirect_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)
