import csv
from models import Meal, db, Category


def import_csv_data():
    sushi = Category(title="Суши", id=1)
    street = Category(title="Стрит-фуд", id=2)
    pizza = Category(title="Пицца", id=3)
    pasta = Category(title="Паста", id=4)
    green = Category(title="Для веганов", id=5)
    db.session.add_all([sushi, street, pizza, pasta, green])
    with open('dishes.csv', mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            db.session.add(
                Meal(
                    title=row[1],
                    price=row[2],
                    description=row[3],
                    picture=row[4],
                    category_id=int(row[5])
                )
            )
        db.session.commit()


if __name__ =='__main__':
    from app import app
    with app.app_context():
        import_csv_data()
