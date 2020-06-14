from django.core.management.base import BaseCommand, CommandError
from products_app import data, constant, api


class Command(BaseCommand):
    help = 'The command : request api openfoodfact' \
           '              get informations from json' \
           '              update info from database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            object_api = api.Api()
            object_data = data.Data()
            for category in constant.LIST_CATEGORIES:
                param = object_api.generate_parameters(category)  # api create parameter
                my_json = object_api.communication_api(constant.URL_OPENFOODFACT, param)  # api request
                object_data.get_info_from_json(my_json)  # get info from json
                object_data.update_data_product_into_bdd()
        except Exception as e:
            raise CommandError(e)
