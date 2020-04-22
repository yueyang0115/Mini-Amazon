from django.apps import AppConfig
from django.db.models.signals import post_migrate


# This function will check whether there are default users, and will create two if not.
def default_users():
    from django.contrib.auth.models import User
    try:
        User.objects.get(username="mini_amazon")
    except User.DoesNotExist:
        mini_amazon = User.objects.create(
            username="mini_amazon",
            email="miniamazon@noreply.com",
            is_superuser=False
        )
        mini_amazon.set_password("amazon12345")
        mini_amazon.profile.is_seller = True
        mini_amazon.save()
    try:
        User.objects.get(username="xkw")
    except User.DoesNotExist:
        xkw = User.objects.create(
            username="xkw",
            email="xkw@noreply.com",
            is_superuser=False
        )
        xkw.set_password("xkw12345")
        xkw.profile.is_seller = True
        xkw.save()


# This function will check whether there are default category of products, and will create if not.
def default_category():
    from amazon.models import Category
    if Category.objects.all().count() == 0:
        Category.objects.create(category="fruit")
        Category.objects.create(category="food")
        Category.objects.create(category="electronic")


# This function will check whether there are default products, and will create if not.
def default_items():
    from django.contrib.auth.models import User
    from amazon.models import Item, Category
    if Item.objects.all().count() == 0:
        # at the first time, we should insert some default data
        amazon = User.objects.get(username="mini_amazon")
        xkw = User.objects.get(username="xkw")
        fruit = Category.objects.get(category="fruit")
        food = Category.objects.get(category="food")
        electronic = Category.objects.get(category="electronic")
        Item.objects.create(
            description="apple", price=1.99,
            img="/static/img/apple.jpg", category=fruit,
            seller=xkw
        )
        Item.objects.create(
            description="orange", price=0.99,
            img="/static/img/orange.jpg", category=fruit,
            seller=xkw
        )
        Item.objects.create(
            description="Fried Chicken", price=5.99,
            img="/static/img/fried_chicken.jpg", category=food,
            seller=xkw
        )
        Item.objects.create(
            description="iPad Mini", price=399.99,
            img="/static/img/ipad_mini.jpg", category=electronic,
            seller=amazon
        )
        Item.objects.create(
            description="iPad", price=429.99,
            img="/static/img/ipad.jpg", category=electronic,
            seller=amazon
        )
        Item.objects.create(
            description="iPad Pro", price=1099.99,
            img="/static/img/ipad_pro.jpg", category=electronic,
            seller=amazon
        )
        Item.objects.create(
            description="Magic Keyboard", price=129.99,
            img="/static/img/magic_keyboard.jpg", category=electronic,
            seller=amazon
        )


def default_warehouse():
    from amazon.models import WareHouse
    # create 10 warehouse
    for x, y in zip(range(10, 110, 10), range(10, 110, 10)):
        WareHouse.objects.create(x=x, y=y)


def migrate_callback(sender, **kwargs):
    default_users()
    default_category()
    default_items()
    default_warehouse()


class AmazonConfig(AppConfig):
    name = 'amazon'

    def ready(self):
        post_migrate.connect(migrate_callback, sender=self)
