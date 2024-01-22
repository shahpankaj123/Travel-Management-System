from django.urls import path
from .views import Signup,Login,Logout,VerifyUser,ResetpasswordView,Verifytoken,Changepassword,MyOrder,Change_password,User_details,Edit_user


urlpatterns = [
    path('register/',Signup.as_view(),name='signup'),
    path('Login/',Login.as_view(),name='Login'),
    path('Logout/',Logout.as_view(),name='Logout'),
    path('verify/<id>/<token>/',VerifyUser.as_view(),name='activate'),
    path('reset/',ResetpasswordView.as_view(),name='reset'),
    path('confirmreset/<id>/',Verifytoken.as_view(),name='tokenverify'),
    path('changepassword/',Changepassword.as_view(),name='changepassword'),

    path('Order/',MyOrder.as_view(),name='order'),
    path('reset_password/',Change_password.as_view(),name='change_password'),
    path('user_details/',User_details.as_view(),name='user_details'),
    path('edit_user/',Edit_user.as_view(),name='edit_user'),
  
]