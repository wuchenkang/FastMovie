from flask import render_template, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
from . import user
from .forms import EditProfileForm, EditProfileAdminForm, CreateMoneyForm
from .. import db
from ..models import Role, User, Voucher, Trolley
from ..decorators import admin_required
import base64
from alipay import AliPay


@user.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/profile.html', user=user, base64=base64)


@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        if form.picture.data:
            current_user.picture = request.files['picture'].read()
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('个人资料已更新!')
        return redirect(url_for('.profile', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', form=form, current_user=current_user, base64=base64)


@user.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('用户资料已更新!')
        return redirect(url_for('user.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('user/edit_profile.html', form=form, user=user)


@user.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = CreateMoneyForm()
    if form.validate_on_submit():
        money = form.money.data
        user = User.query.filter(User.id == current_user.id).first()
        user.money += money
        db.session.commit()
        flash("充值成功！")
        return redirect(url_for('.balance'))
    return render_template("user/balance.html", form=form)


@user.route('/order')
@login_required
def order():
    page = request.args.get('page', 1, type=int)
    if current_user.is_administrator():
        pagination = Voucher.query.paginate(
            page, per_page=current_app.config['ITEM_PER_PAGE'],
            error_out=False
        )
    else:
        pagination = Voucher.query.filter(Voucher.user_id == current_user.id).paginate(
            page, per_page=current_app.config['ITEM_PER_PAGE'],
            error_out=False
        )
    vouchers = pagination.items
    return render_template("user/order.html", vouchers=vouchers, pagination=pagination)


@user.route('/order_detail/<string:order_identify>/', methods=['GET'])
@login_required
def order_detail(order_identify):
    voucher = Voucher.query.filter(Voucher.order_identify == order_identify).first()
    if voucher.multiply_commodities:
        current_items = []
        movie_count = []
        ids = list(map(lambda x: int(x), voucher.name.split()))
        for id in ids:
            item = Trolley.query.filter(Trolley.id == id).first()
            current_items.append(item.movie)
            movie_count.append(item.movie_count)
        return render_template('trolley/commodities.html', current_items=current_items, voucher=voucher,
                               movie_count=movie_count, len=len, range=range)
    else:
        return render_template('subject/commodity.html', voucher=voucher)


@user.route('/refund/<string:order_identify>/', methods=['GET'])
@login_required
def refund(order_identify):
    voucher = Voucher.query.filter(Voucher.order_identify == order_identify).first()
    if voucher.is_send:
        flash("商家已发货，无法退款！")
    elif voucher.is_refund == 0:
        voucher.is_refund = 1
        db.session.commit()
        flash("申请退款成功！")
    elif voucher.is_refund == 1:
        flash("该订单已经申请退款！")
    elif voucher.is_refund == 2:
        flash("该订单已经退款！")
    if voucher.multiply_commodities:
        current_items = []
        movie_count = []
        ids = list(map(lambda x: int(x), voucher.name.split()))
        for id in ids:
            item = Trolley.query.filter(Trolley.id == id).first()
            current_items.append(item.movie)
            movie_count.append(item.movie_count)
        return render_template('trolley/commodities.html', current_items=current_items, voucher=voucher,
                               movie_count=movie_count, len=len, range=range)
    else:
        return render_template('subject/commodity.html', voucher=voucher)


@user.route('/admin_refund/<string:order_identify>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_refund(order_identify):
    voucher = Voucher.query.filter(Voucher.order_identify == order_identify).first()
    if voucher.is_send:
        flash("您已发货，无法退款！")
    elif voucher.is_refund == 2:
        flash("该订单已退款，无需再退款！")
    else:
        if voucher.is_refund == 0:
            flash("您已取消该订单，将向相应顾客退款！")

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

        result = myalipay.api_alipay_trade_refund(out_trade_no=order_identify, refund_amount=voucher.total_money)
        if result["code"] == "10000":
            voucher.is_refund = 2
            db.session.commit()
            flash("退款成功")
        else:
            flash("退款失败")
    if voucher.multiply_commodities:
        current_items = []
        movie_count = []
        ids = list(map(lambda x: int(x), voucher.name.split()))
        for id in ids:
            item = Trolley.query.filter(Trolley.id == id).first()
            current_items.append(item.movie)
            movie_count.append(item.movie_count)
        return render_template('trolley/commodities.html', current_items=current_items, voucher=voucher,
                               movie_count=movie_count, len=len, range=range)
    else:
        return render_template('subject/commodity.html', voucher=voucher)


@user.route('/admin_send/<string:order_identify>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_send(order_identify):
    voucher = Voucher.query.filter(Voucher.order_identify == order_identify).first()
    if not voucher.is_send and voucher.is_refund == 0:
        voucher.is_send = True
        db.session.commit()
        flash("确认发货！")
    if voucher.multiply_commodities:
        current_items = []
        movie_count = []
        ids = list(map(lambda x: int(x), voucher.name.split()))
        for id in ids:
            item = Trolley.query.filter(Trolley.id == id).first()
            current_items.append(item.movie)
            movie_count.append(item.movie_count)
        return render_template('trolley/commodities.html', current_items=current_items, voucher=voucher,
                               movie_count=movie_count, len=len, range=range)
    else:
        return render_template('subject/commodity.html', voucher=voucher)
