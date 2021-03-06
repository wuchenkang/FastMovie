from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_required, current_user
from . import subject
from .. import db
from .forms import CreateCommentForm
from ..models import Movie, User, Comment, Voucher, Rating
import random
# from .myalipay import *
from alipay import AliPay


@subject.route('/movies')
def movies():
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.order_by(Movie.name).paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    movies = pagination.items

    return render_template('subject/movies.html', movies=movies, pagination=pagination)


@subject.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get_or_404(id)
    if request.method == 'POST':
        form = request.form
        rating = Rating()
        rating.user_id = current_user.id
        rating.movie_id = movie.id
        rating.score = float(form['rating'])
        record = Rating.query.filter(
            Rating.movie_id == movie.id).filter(
            Rating.user_id == current_user.id
        ).first()
        if record is None:
            movie.total_rating += 1
            movie.total_score += rating.score
        else:
            movie.total_score -= record.score
            movie.total_score += rating.score
            db.session.delete(record)
        db.session.add(rating)
        db.session.add(movie)
        db.session.commit()
        flash('评分成功')
    rating = round(movie.total_score / movie.total_rating, 1) if movie.total_rating > 0 else 2.5
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Comment.movie_id == movie.id).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENT_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('subject/movie.html', movie=movie, rating=rating, comments=comments, pagination=pagination)


@subject.route('/movie/comment/<int:id>/', methods=['GET', 'POST'])
@login_required
def comment(id):
    movie = Movie.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Comment.movie_id == movie.id).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENT_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    user = User.query.filter(User.id == current_user.id).first()
    form = CreateCommentForm()
    if form.validate_on_submit():
        if form.submit.data:
            cmt = Comment()
            cmt.title = form.title.data
            cmt.body = form.comment.data
            movie.comments.append(cmt)
            user.comments.append(cmt)
            db.session.commit()
            flash('评论成功')
        return redirect(url_for('subject.movie', id=id))
    return render_template('subject/comment.html', form=form, movie=movie, comments=comments, pagination=pagination)


@subject.route('/movie/comdel/<int:id>/', methods=['GET', 'POST'])
@login_required
def comdel(id):
    comment = Comment.query.get_or_404(id)
    movie = Movie.query.get_or_404(comment.movie_id)
    db.session.delete(comment)
    db.session.commit()
    flash("评论删除成功")
    return redirect(url_for('subject.movie', id=movie.id))


@subject.route('/movie/commodity/<int:id>/', methods=['GET', 'POST'])
@login_required
def buy(id):
    if current_user.is_administrator():
        flash("禁止购买自家产品！")
        return redirect(url_for('subject.movie', id=id))
    else:
        voucher = Voucher()
        while True:
            order_identify = ''
            order_identify += chr(random.randint(1, 9) + ord('0'))
            for i in range(17):
                order_identify += chr(random.randint(0, 9) + ord('0'))
            if not Voucher.query.filter(Voucher.order_identify == order_identify).first():
                break

        movie = Movie.query.get_or_404(id)
        voucher.movie = movie
        voucher.user = current_user
        voucher.is_pay = False
        voucher.multiply_commodities = False
        voucher.total_money = 0
        voucher.total_money += movie.price
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
            debug = True  # 默认False
        )
        query_params = myalipay.api_alipay_trade_page_pay(
            out_trade_no=order_identify,
            total_amount=float(movie.price),
            subject=movie.name,
            return_url="http://127.0.0.1:5000/subject/movie/commodity/result/"
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)

        return redirect(pay_url)


@subject.route('/movie/commodity/result/', methods=['GET'])
@login_required
def buy_result():
    out_trade_no = request.args.get('out_trade_no')
    id = int(out_trade_no[out_trade_no.find('x') + 1:])
    voucher = Voucher.query.filter(Voucher.id == id).first()
    voucher.is_pay = True
    db.session.commit()

    flash("支付成功！花费{}元".format(voucher.total_money))

    return render_template('subject/commodity.html', voucher=voucher)


@subject.route('/movie/commodity/notify/', methods=['POST', 'GET'])
def buy_notify():
    # 检测是否支付成功
    # 去请求体中获取所有返回的数据：状态/订单号
    from urllib.parse import parse_qs

    # body_str = request.body.decode('utf-8')
    # post_data = parse_qs(body_str)
    #
    # post_dict = {}
    # for k, v in post_data.items():
    #     post_dict[k] = v[0]
    # print(post_dict)

    # sign = post_dict.pop('sign', None)
    # status = alipay.verify(post_dict, sign)
    print('\n**************************POST验证\n', request.data, request.content_encoding)
    return 'success'
