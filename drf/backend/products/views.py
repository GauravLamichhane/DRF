from rest_framework import generics,mixins, permissions, authentication
from .models import Product
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .permissions import IsStaffEditorPermission

#list and create api
class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers
  authentication_classes = [authentication.SessionAuthentication]
  permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]
  

  def perform_create(self,serializer):
    print(serializer.validated_data)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = title
    serializer.save(content = content)
  
product_list_create_view = ProductListCreateAPIView.as_view()

#Detail api view
class ProductDetailAPIView(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers

product_detail_view = ProductDetailAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializers
# product_list_view = ProductListAPIView.as_view()

class ProductUpdateAPIView(generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers
  lookup_field = 'pk'

  def perform_update(self, serializer):
    instance = serializer.save()
    if not instance.content:
      instance.content = instance.title
product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers
  lookup_field = 'pk'

  def perform_destroy(self, instance):
    super().perform_destroy(instance)
product_destroy_view = ProductDestroyAPIView.as_view()

class CreateAPIView(mixins.CreateModelMixin,generics.GenericAPIView):
  pass
########
#mixins

class ProductMixinView(generics.GenericAPIView,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin):
  queryset = Product.objects.all()
  serializer_class = ProductSerializers
  lookup_field = 'pk'
  def get(self,request,*args,**kwargs):
    print(args,kwargs)
    pk = kwargs.get('pk')
    if pk is not None:
      return self.retrieve(request,*args,**kwargs)
    return self.list(request,*args,**kwargs)
  

  def post(self,request,*args,**kwargs):
    return self.create(request, *args,**kwargs)
  
  def perform_create(self,serializer):
    print(serializer.validated_data)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = "This is a single view doing cool stuff"
    serializer.save(content = content)
  

product_mixin_view = ProductMixinView.as_view()

"""
The difference between the class based view and function based view is that in function based view we write condtion where as in class based we write functions
"""


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
