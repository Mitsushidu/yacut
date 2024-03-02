from flask import jsonify, request

from yacut import app, db

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import ALPHABET, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    link = URLMap()
    if 'custom_id' in data and data['custom_id'] is not None:
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        if len(data['custom_id']) > 16 or any(sym not in ALPHABET for sym in data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
        link = URLMap(
            original=data['url'],
            short=data['custom_id'],
        )
    else:
        link = URLMap(
            original=data['url'],
            short=get_unique_short_id(),
        )
    db.session.add(link)
    db.session.commit()
    return jsonify({
        'url': link.original,
        'short_link': request.url_root + link.short,
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200