from django.urls import path 
# from .views import GenerateSummary, SignIn, SignUp, signup
from .views import GenerateSummary,UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView, signup
urlpatterns = [
    
    path('api/sign-in/', UserLoginAPIView.as_view(), name='sign_in'),
    path('api/sign-up/', UserRegisterAPIView.as_view(), name= 'sign_up'),
    path('signup/', signup, name="signup"),
    path('api/logout/', UserLogoutAPIView.as_view(), name="log_out"),
    path('generate-summary/', GenerateSummary.as_view(), name="generate_summary"),
]