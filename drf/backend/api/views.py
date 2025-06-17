from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from products.models import Product
from products.serializers import ProductSerializers
@api_view(['POST'])
def api_home(request, *args, **kwargs):
    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:
    #     # data = model_to_dict(model_data, fields=['id', 'title','price','sale_price'])
    #     data = ProductSerializers(instance).data
    serializer = ProductSerializers(data = request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        print(serializer.data)
    return Response(serializer.data)  