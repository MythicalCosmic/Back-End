from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import LoginSerializer
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'success': 'You have successfully logged out!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def allProducts(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createProduct(request):
    print("Request Data:", request.data)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        print("Instance Saved:", instance)
        return Response(Product(instance).data, status=201)
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=400)



@api_view(['DELETE'])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'success': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def updateProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def allCategory(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createCategory(request):
    print("Request Data:", request.data)
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        print("Instance Saved:", instance)
        return Response(Category(instance).data, status=201)
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def deleteCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response({'success': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def updateCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)