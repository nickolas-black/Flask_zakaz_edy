from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()


order_meal_association = db.Table('order_meal',
                                  db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
                                  db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
                                  )


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    orders = db.relationship("Order", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User {}'.format(self.email)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, nullable=False)
    order_sum = db.Column(db.Float(8), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="orders")
    meals = db.relationship('Meal', secondary=order_meal_association, back_populates='orders')

    def __repr__(self):
        return 'Order {}'.format(self.phone)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(32), nullable=False)
    meals = db.relationship("Meal", back_populates="category")

    def __repr__(self):
        return 'Category {}'.format(self.title)


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    picture = db.Column(db.String(32), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="meals")
    orders = db.relationship('Order', secondary=order_meal_association, back_populates='meals')

    def __repr__(self):
        return 'Meal {}'.format(self.title)


class MyAdmin(ModelView):
    can_create = False
    can_edit = True
    can_delete = False
    column_exclude_list = ['password_hash', ]