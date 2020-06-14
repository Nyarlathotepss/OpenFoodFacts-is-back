from products_app import constant
from products_app.models import Product, Category


class Data:
    """ Data from json to database """
    def __init__(self):
        self.info_products = []  # a list of product from json

    def get_info_from_json(self, json):
        """ Get informations from json """
        k = 0
        list_names_products = []
        while k < constant.LIMIT_PRODUCTS:
            try:
                if json['products'][k]['product_name'].lower().strip() in list_names_products:
                    k += 1
                else:
                    self.info_products.append(
                        (json['products'][k]['product_name'],
                         json['products'][k]['ingredients_text_fr'],
                         json['products'][k]['nutrition_grade_fr'],
                         json['products'][k]['purchase_places'],
                         json['products'][k]['url'],
                         json['products'][k]['image_url'],
                         json['products'][k]['nutriments']['fat_100g'],
                         json['products'][k]['nutriments']['saturated-fat_100g'],
                         json['products'][k]['nutriments']['salt_100g'],
                         json['products'][k]['nutriments']['sugars_100g']))
                    list_names_products.append(self.info_products[-1][0].lower().strip())
                    k += 1
            except KeyError as error:
                print(error)
                k += 1
                continue

    def insert_data_category_into_bdd(self):
        """ Create categories from constant.LIST_CATEGORIES in database """
        for category in constant.LIST_CATEGORIES:
            data = Category(name=category)
            data.save()
            print("the category " + str(category) + " has been created")

    def insert_data_product_into_bdd(self, id_category):
        """ Create products from self.info_products in database """
        for product in self.info_products:
            try:
                data = Product(
                    name=product[0],
                    ingredient=product[1],
                    nutriscore=product[2],
                    store=product[3],
                    url=product[4],
                    category_id=id_category,
                    image_url=product[5],
                    fat_100g=product[6],
                    saturated_fat_100g=product[7],
                    salt_100g=product[8],
                    sugars_100g=product[9]
                    )
                data.save()
                print("the informations product for " + product[0] + " has been added ")
            except Exception as error:
                print("a problem has occurs with the product " + product[0] + ":", error)

    def update_data_product_into_bdd(self):
        for product in self.info_products:
            product_name = str(product[0])
            try:
                p = Product.objects.get(name=product_name)
                p.ingredient = product[1],
                p.store = product[3],
                p.url = product[4],
                p.image_url = product[5],
                p.fat_100g = product[6],
                p.saturated_fat_100g = product[7],
                p.salt_100g = product[8],
                p.sugars_100g = product[9]
                p.save()
                print("Update of product"+p.name)
            except Exception as error:
                print("a problem has occurs with the product " + product[0] + ":", error)
