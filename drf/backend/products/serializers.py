from rest_framework import serializers
from .models import Product
class ProductSerializers(serializers.ModelSerializer):
  my_discount = serializers.SerializerMethodField(read_only = True)
  class Meta:
    model = Product
    fields = [
      'title',
      'content',
      'price',
      'sale_price',
      'my_discount'
    ]
  def get_my_discount(self,obj):
    if not hasattr(obj,'id'):
      return None
    if not isinstance(obj,Product):
      return None
    return obj.get_discount()
#explaination
"""
my_discount = serializers.SerializerMethodField()
field name is my_discount
Django thinks: "I need to find a method called 'get_' + 'my_discount'"
Django thinks: "So I'm looking for: get_my_discount"


"""