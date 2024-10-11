from flask import render_template, url_for, flash, redirect, Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm, ProductForm
from app import db, bcrypt
from app.models import User, Product

bp = Blueprint('routes', __name__)


@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()  # Поиск по названию
    else:
        results = []
    return render_template('search_results.html', results=results, query=query)


@bp.route('/update_product/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.quantity = request.form.get('quantity', type=int)
    product.price = request.form.get('price', type=float)

    db.session.commit()
    flash('Информация о товаре обновлена!', 'success')
    return redirect(url_for('routes.home'))

@bp.route('/')
@bp.route('/home')
def home():
    products = Product.query.all()  # Получаем все продукты из базы данных
    return render_template('home.html', products=products)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверка, существует ли пользователь с таким именем или электронной почтой
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Пользователь с таким именем или электронной почтой уже существует.', 'danger')
            return redirect(url_for('routes.register'))

        # Создание нового пользователя
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Ваш аккаунт был создан! Вы можете войти.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Неверное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            price=form.price.data
        )
        db.session.add(product)
        db.session.commit()
        return 'Product added successfully!'  # Возвращаем сообщение
    return render_template('add_product.html', form=form)