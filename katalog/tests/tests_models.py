from django.test import TestCase
from katalog.models import CatalogItem

class ModelsTest(TestCase):
    def create_test_model(self):
        return CatalogItem.objects.create(item_name = "Wooper Poke Plush",
                                          item_price = 14.99,
                                          item_stock = 0,
                                          description = "7.3 inches tall and 8.5 inches wide",
                                          rating = 5,
                                          item_url = "https://www.pokemoncenter.com/product/701-03021/wooper-poke-plush-8-in")
    
    def test_catalog_item(self):
        testItem = self.create_test_model()
        self.assertTrue(isinstance(testItem, CatalogItem))
        self.assertEqual(testItem.item_name, "Wooper Poke Plush")