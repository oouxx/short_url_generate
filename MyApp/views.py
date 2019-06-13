from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response
from flask import request

from MyApp import db
from MyApp import redis_store
from MyApp.models import ShortCodes
from config.constant import HOST
from utils.convert import get_code

shorten = Blueprint('shorten', __name__, template_folder='templates', static_folder='static')


@shorten.route('/')
@shorten.route('/shorten', methods=['GET', 'POST'])
def get_short_url():
    """
    获取短链接
    :return:   {'status': 'success', 'code': code, 'host': HOST}
    """

    if request.method == 'GET':
        return render_template('index.html')
    else:
        long_url = request.get_json()
        url = long_url.get("long_url")
        if not url:
            return render_template('index.html')
        if not url.startswith('http://') or not url.startswith('https://'):
            url = 'http://' + url
        # 判断是否创建过
        # code 是 byte类型
        code_from_redis = redis_store.get(url)
        result = {'status': 'success', 'code': code_from_redis, 'host': HOST}
        if code_from_redis:
            result['code'] = result['code'].decode()
            return jsonify(result)
        short_code = ShortCodes.query.filter_by(url=url).first()
        if short_code:
            result['code'] = short_code
            return jsonify(result)

        short_url_id = redis_store.incr("short_url_id", amount=1)
        new_code = get_code(short_url_id)
        short_code = ShortCodes(redis_incr_id=short_url_id, url=url, code=new_code)
        try:
            db.session.add(short_code)
            db.session.commit()
        except Exception as e:
            print(e)
        try:
            redis_store.setex(url, 60 * 60 * 24, new_code)
            redis_store.setex(new_code, 60 * 60 * 24, url)
        except Exception as e:
            print(e)
        result['code'] = new_code
        return jsonify(result)


@shorten.route('/<code>')
def redirect_to_real_url(code):
    """
    重定向到真正的url
    :param code: 短链接关键字code
    :return: 302重定向到真正的url
    """
    if len(code) != 6:
        make_response()
        return redirect(url_for('shorten.get_short_url'))
    url = redis_store.get(code)
    if url:
        return redirect(url.decode('utf-8'))

    short_code = ShortCodes.query.filter_by(code=code).first()
    if short_code:
        url = short_code.get_url()
        try:
            redis_store.setex(url, 60 * 60 * 24, code)
            redis_store.setex(code, 60 * 60 * 24, url)
        except Exception as e:
            print(e)
        return redirect(url.decode('utf-8'))
    return redirect(url_for('shorten.get_short_url'))
