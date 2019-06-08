from flask import render_template, request, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import and_, or_
from . import trolley
from ..models import Trolley, Movie, Voucher
from .. import db
from alipay import AliPay
import random


@trolley.route('/')
@login_required
def view_trolley():
    page = request.args.get('page', 1, type=int)
    pagination = Trolley.query.filter(Trolley.user_id == current_user.id).order_by(Trolley.movie_id).paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    items = pagination.items
    return render_template('trolley/trolley.html', items=items, pagination=pagination)


@trolley.route('/add/<int:id>-<string:name>-<float:price>')
def add_trolley(id, name, price):
    if len(Trolley.query.filter(and_(Trolley.user_id == current_user.id, Trolley.movie_id == id)).all()) == 0:
        new_item = Trolley()
        new_item.user_id = current_user.id
        new_item.movie_id = id
        new_item.movie_name = name.strip()
        new_item.movie_price = price
        new_item.movie_count = 1
        db.session.add(new_item)
    else:
        old_item = Trolley.query.filter(and_(Trolley.user_id == current_user.id, Trolley.movie_id == id)).first()
        old_item.movie_count += 1
        db.session.add(old_item)
    db.session.commit()
    return redirect(url_for('trolley.view_trolley'))


@trolley.route('/commodities', methods=['post'])
@login_required
def submit():
    old_items = Trolley.query.filter(Trolley.user_id == current_user.id).all()
    for item in old_items:
        db.session.delete(item)
    for i in range(len(request.form)):
        new_item = Trolley()
        args = request.form[str(i)].split('|')
        new_item.user_id = int(current_user.id)
        new_item.movie_id = int(args[0])
        new_item.movie_name = args[1]
        new_item.movie_price = float(args[2])
        new_item.movie_count = int(args[3])
        new_item.multiply_commodities = True
        movie = Movie.query.filter(Movie.id == int(args[0])).first()
        new_item.movie = movie
        db.session.add(new_item)
    db.session.commit()

    current_items = Trolley.query.filter(Trolley.user_id == current_user.id).all()
    money = 0
    name = ''
    movie_ids = ''
    for item in current_items:
        money += item.movie_price * item.movie_count
        name += " " + item.movie.name.strip()
        movie_ids += " " + str(item.id)
    name = name.strip()
    movie_ids = movie_ids.strip()
    # return render_template('trolley/commodities.html', money=money, current_items=current_items)
    while True:
        order_identify = ''
        order_identify += chr(random.randint(1, 9) + ord('0'))
        for i in range(17):
            order_identify += chr(random.randint(0, 9) + ord('0'))
        if not Voucher.query.filter(Voucher.order_identify == order_identify).first():
            break

    voucher = Voucher()
    voucher.user = current_user
    voucher.is_pay = False
    voucher.total_money = money
    voucher.name = movie_ids
    db.session.add(voucher)
    db.session.commit()
    order_identify += 'x' + str(voucher.id)
    voucher.order_identify = order_identify
    db.session.commit()

    app_private_key_string = open(r"app/subject/app_private_2048.txt").read()
    alipay_public_key_string = open(r"app/subject/alipay_public_2048.txt").read()
    myalipay = AliPay(
        appid="2016093000629449",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    query_params = myalipay.api_alipay_trade_page_pay(
        out_trade_no=order_identify,
        total_amount=float(money),
        subject=name,
        return_url="http://127.0.0.1:5000/trolley/commodities/result/"
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)

    return redirect(pay_url)


@trolley.route('/commodities/result/', methods=['GET'])
@login_required
def buy_result():
    out_trade_no = request.args.get('out_trade_no')
    id = int(out_trade_no[out_trade_no.find('x') + 1:])
    voucher = Voucher.query.filter(Voucher.id == id).first()
    voucher.is_pay = True
    db.session.commit()

    current_items = []
    movie_count = []
    ids = list(map(lambda x: int(x), voucher.name.split()))
    for id in ids:
        item = Trolley.query.filter(Trolley.id == id).first()
        current_items.append(item.movie)
        movie_count.append(item.movie_count)
    flash("支付成功！花费{}元".format(voucher.total_money))

    tro = Trolley.query.filter(Trolley.user_id == current_user.id).all()
    for item in tro:
        db.session.delete(item)
    db.session.commit()

    return render_template('trolley/commodities.html', current_items=current_items, voucher=voucher, movie_count=movie_count)
