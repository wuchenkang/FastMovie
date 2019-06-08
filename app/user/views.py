from flask import render_template, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
from . import user
from .forms import EditProfileForm, EditProfileAdminForm, CreateMoneyForm
from .. import db
from ..models import Role, User, Voucher
from ..decorators import admin_required
import base64


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
    return render_template('subject/commodity.html', voucher=voucher)


@user.route('/refund/<string:order_identify>/', methods=['GET'])
@login_required
def refund(order_identify):
    voucher = Voucher.query.filter(Voucher.order_identify == order_identify).first()
    if voucher.is_refund:
        flash("该订单已经申请退款！")
    else:
        voucher.is_refund = True
        db.session.commit()
        flash("申请退款成功！")
    return render_template('subject/commodity.html', voucher=voucher)
