from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_required, current_user
from . import subject
from .. import db
from .forms import CreateCommentForm, CreateVoucherForm
from ..models import Movie, User, Comment, Voucher
import random

@subject.route('/movies')
def movies():
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.order_by(Movie.name).paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    movies = pagination.items

    return render_template('subject/movies.html', movies=movies, pagination=pagination)


@subject.route('/movie/<int:id>')
def movie(id):
    movie = Movie.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Comment.movie_id == movie.id).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENT_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('subject/movie.html', movie=movie, comments=comments, pagination=pagination)


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


@subject.route('/movie/commodity/<int:id>/', methods=['GET', 'POST'])
@login_required
def buy(id):
    form = CreateVoucherForm()
    movie = Movie.query.get_or_404(id)
    voucher = Voucher()
    voucher.movie = movie
    voucher.user = current_user
    while True:
        order_identify = ''
        order_identify += chr(random.randint(1, 9) + ord('0'))
        for i in range(17):
            order_identify += chr(random.randint(0, 9) + ord('0'))
        if not Voucher.query.filter(Voucher.order_identify == order_identify).first():
            break
    session['order_identify'] = order_identify
    voucher.order_identify = order_identify
    if form.validate_on_submit():
        print(movie.price)
        print(current_user.money)
        if movie.price <= current_user.money:
            voucher.order_identify = session['order_identify']
            current_user.money -= movie.price
            db.session.add(voucher)
            db.session.commit()
            flash("支付成功！花费{}元".format(movie.price))
        else:
            flash("余额不足，请充值。")
        return redirect(url_for('subject.movie', id=id))
    return render_template('subject/commodity.html', voucher=voucher, form=form)
