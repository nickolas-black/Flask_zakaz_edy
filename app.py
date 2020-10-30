from datetime import datetime
from flask import Flask, render_template, session, redirect, request, flash, abort, url_for
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Order, Category, Meal, MyAdmin
from forms import LoginForm, RegisterForm, OrderForm
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/login/', methods=['GET', 'POST'])
def render_login():
    if session.get("user.id"):
        return redirect(url_for('render_index'))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                session["user"] = {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
                session["is_auth"] = True
                return redirect(url_for('render_account'))
            else:
                form.password.errors.append("Неверное имя или пароль")
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            new_user = User(email=form.email.data, role="user")
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('render_account'))
        else:
            flash('Пользователь с почтой {} уже зарегистрирован'.format(form.email.data))
    return render_template('login.html', form=form)


@app.route('/logout/')
def render_logout():
    if session.get("is_auth"):
        session.clear()
    return redirect(url_for('render_login'))


@app.route('/')
def render_index():
    meals = Category.query.all()
    return render_template('main.html', auth=session.get('is_auth'), meals=meals, cart_sum=session.get('cart_sum'),
                           cart=session.get('cart'))


@app.route('/add/<meal_id>/')
def add_to_cart(meal_id):
    cart = session.get("cart", [])
    cart_sum = session.get("cart_sum", [])
    meal = Meal.query.get(int(meal_id))
    if meal_id in cart:
        flash('К сожалению, мы создаем блюда в единственном эклемпляре, чтобы клиенты не переедали')
    else:
        cart_sum.append(meal.price)
        session['cart_sum'] = cart_sum
        cart.append(meal_id)
        session['cart'] = cart
        flash('Блюдо "{}" добавлено в корзину.'.format(meal.title))
    return redirect(url_for('render_index'))


@app.route('/remove/<meal_id>/')
def remove_from_cart(meal_id):
    cart = session.get("cart", [])
    cart_sum = session.get('cart_sum', [])
    meal_to_delete = Meal.query.get(int(meal_id))
    if meal_id in cart:
        cart.remove(meal_id)
        cart_sum.remove(meal_to_delete.price)
    session["cart"] = cart
    session["cart_sum"] = cart_sum
    flash('Блюдо "{}" удалено из корзины.'.format(meal_to_delete.title))
    return redirect(url_for('render_cart'))


@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    if session.get("cart") is None:
        abort(404, description="Ресурс не найден!")
    else:
        cart = session.get("cart", [])
        cart_meals = []
        for id_of_meal in cart:
            cart_meals.append(Meal.query.get(int(id_of_meal)))
        total_order_price = sum(session.get('cart_sum'))
        form = OrderForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=session.get('user').get('email')).first()
            order = Order(date=datetime.today(), order_sum=total_order_price, phone=form.phone.data,
                          address=form.address.data, name=form.name.data, user=user, meals=cart_meals)
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('render_ordered'))
        return render_template('cart.html', auth=session.get('is_auth'), cart_sum=session.get('cart_sum'),
                               cart=session.get('cart'), cart_meals=cart_meals, form=form)


@app.route('/account/')
def render_account():
    if session.get('is_auth'):
        account_order_info = User.query.filter_by(email=session.get('user').get('email')).first()
        return render_template('account.html', auth=session.get('is_auth'), cart_sum=session.get('cart_sum'),
                               cart=session.get('cart'), info=account_order_info)
    else:
        return render_template('auth_error.html')


@app.route('/ordered/')
def render_ordered():
    if session.get("cart") is None:
        abort(404, description="Ресурс не найден!")
    else:
        session.pop("cart")
        session.pop("cart_sum")
        return render_template('ordered.html')


admin = Admin(app)
admin.add_view(MyAdmin(User, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Order, db.session))


if __name__ == "__main__":
    app.run()
