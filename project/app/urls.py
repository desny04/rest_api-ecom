from django.urls import path,include
from rest_framework.routers import SimpleRouter
from .views import AuthViewSet,ProductViewSet,CategoryViewSet,WishlistViewSet
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router=SimpleRouter()
router.register(r'auth',AuthViewSet,basename='auth')
router.register(r'products',ProductViewSet,basename='products')
router.register(r'categories',CategoryViewSet,basename='categories')
router.register(r'wishlist',WishlistViewSet,basename='wishlist')

urlpatterns=[
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('api/',include(router.urls)),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)