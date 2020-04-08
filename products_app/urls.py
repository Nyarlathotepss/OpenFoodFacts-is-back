from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^result/', views.search_products, name="result"),
    url(r'product_number/([0-9]{1,8})/', views.product_page, name="product_page"),
    url('product_save/', views.product_save, name="product_save"),
    url(r'favorites/', views.favorites, name="favorites"),
    url('law_mention/', views.law_mention, name="law_mention"),
    url('favorite_deleted', views.favorite_deleted, name="favorite_deleted")
]