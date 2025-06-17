from rest_framework import generics
from .models import Product
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response



class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers

  def perform_create(self,serializer):
    print(serializer.validated_data)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = title
    serializer.save(content = content)
  
product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers

product_detail_view = ProductDetailAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializers
# product_list_view = ProductListAPIView.as_view()

"""

  DRF sees you're accessing /products/1/

RetrieveAPIView looks for Product.objects.get(pk=1)

It finds that product

It uses your ProductSerializers to turn it into JSON

It sends the JSON response back
  
  """

#Using function based views
@api_view(['POST','GET'])
def product_alt_view(request,pk = None,*args,**kwargs):
  method = request.method
  if method == "GET":
    #detail view
    if pk is not None:
      obj = get_object_or_404(Product,pk = pk)
      data = ProductSerializers(obj,many = False).data
      return Response(data)
    
    #list view
    query_set = Product.objects.all()
    data = ProductSerializers(query_set,many = True).data
    return Response(data)

  if method == "POST":
    #create an item
    serializers = ProductSerializers(data = request.data)
    if serializers.is_valid():
     title = serializers.validated_data.get('title')
     content = serializers.validated_data.get('content')
     if content is None:
      content = title
     serializers.save(content = content)
     return Response(serializers.data)
    return Response({"invalid":"Not good data"},
                    status=400)
