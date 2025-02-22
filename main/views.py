from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from .decorators import *

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                raise AuthenticationFailed('Invalid credentials')
        else:
            raise AuthenticationFailed('Email and password are required')
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = request.data.get('refresh_token')
        token_obj = RefreshToken(token)
        token_obj.blacklist()
        logout(request)
        return Response({'success': 'You have successfully logged out!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def allProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def createProduct(request):
    print("Request data:", request.data)
    print("Files:", request.FILES)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(ProductSerializer(instance).data, status=status.HTTP_201_CREATED)
    print("Errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'success': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def restoreProduct(request, pk):
    try:
        deleted_product = DeletedProduct.objects.get(pk=pk)
    except DeletedProduct.DoesNotExist:
        return Response({'error': 'Deleted product not found'}, status=status.HTTP_404_NOT_FOUND)

    product = Product(
        id=deleted_product.original_id,
        name=deleted_product.name,
        description=deleted_product.description,
        price=deleted_product.price,
        quantity=deleted_product.quantity,
        category=deleted_product.category,
        photo=deleted_product.photo
    )
    product.save()
    deleted_product.delete()

    return Response({'success': 'Product restored successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def listDeletedProducts(request):
    deleted_products = DeletedProduct.objects.all()
    serializer = DeletedProductSerializer(deleted_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
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
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def allCategory(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def createCategory(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def deleteCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response({'success': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@has_role(['admin', 'editor'])
@permission_classes([IsAuthenticated])
def updateCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
