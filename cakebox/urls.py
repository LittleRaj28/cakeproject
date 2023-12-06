from django.urls import path
from cakebox.views import SignupView,SignInView,CategoryCreateView,remove_category,CakeCreateView,\
    CakeListView,CakeUpdateView,remove_cakeview,CakeVarientCreateView,CakeDetailView,\
    CakeVarientUpdateView,remove_varient,OfferCreateView,offer_delete,sign_out_view,IndexView,remove_review


urlpatterns=[
    path("register/",SignupView.as_view(),name="signup"),
    path("",SignInView.as_view(),name="signin"),
    path("category/add",CategoryCreateView.as_view(),name="category-add"),
    path("category/<int:pk>/remove",remove_category,name="category-remove"),
    path("cake/add",CakeCreateView.as_view(),name="cake-add"),
    path("cakes/all",CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/change",CakeUpdateView.as_view(),name="cake-change"),
    path("cakes/<int:pk>/remove",remove_cakeview,name="cake-remove"),
    path("cakes/<int:pk>/review/remove",remove_review,name="review-remove"),
    path("cakes/<int:pk>/vcarients/add",CakeVarientCreateView.as_view(),name="add-varient"),
    path("cakes/<int:pk>/",CakeDetailView.as_view(),name="cake-detail"),
    path("varients/<int:pk>/change/",CakeVarientUpdateView.as_view(),name="update-varient"),
    path("varients/<int:pk>/remove/",remove_varient,name="remove-varient"),
    path("varients/<int:pk>/offers/add",OfferCreateView.as_view(),name="offers-add"),
    path("offers/<int:pk>/remove",offer_delete,name="delete-offer"),
    path("logout/",sign_out_view,name="signout"),
    path("index/",IndexView.as_view(),name="index"),


]