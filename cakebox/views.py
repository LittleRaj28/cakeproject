from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator



from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,DeleteView,TemplateView
from cakebox.forms import RegistrationForm,LoginForm,CategoryAddForm,CakeAddForm,CakeVarientForm,OfferForm
from cakebox.models import User,Category,Cakes,CakeVarients,Offers,Reviews


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def is_admin(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,"permission denied for current user")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

            
decs=[signin_required,is_admin]

# Create your views here.

class SignupView(CreateView):
    template_name="cakebox/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"Account created")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Failed to create account")
        return super().form_invalid(form)
    

class SignInView(FormView):
    template_name="cakebox/login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully")
                return redirect("cake-list")
            else:
                messages.error(request,"Invalid credential")
        else:
            return render(request,"cakebox/login.html")
        
@method_decorator(decs,name="dispatch")
class CategoryCreateView(CreateView,ListView):
    template_name="cakebox/category_add.html"
    form_class=CategoryAddForm
    model=Category
    context_object_name="categories"
    success_url=reverse_lazy("category-add")

    def form_valid(self, form):
        messages.success(self.request,"Category added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Category added failed")
        return super().form_invalid(form)
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)
    

@signin_required
@is_admin
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"Category removed")
    return redirect("category-add")

@method_decorator(decs,name="dispatch")
class CakeCreateView(CreateView):
    template_name="cakebox/cake_add.html"
    form_class=CakeAddForm
    model=Cakes
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"Cake added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Cake added failed")
        return super().form_invalid(form)
    
@method_decorator(decs,name="dispatch")    
class CakeListView(ListView):
    template_name="cakebox/cake_list.html"
    model=Cakes
    context_object_name="cakes"

@method_decorator(decs,name="dispatch")
class CakeUpdateView(UpdateView):
    template_name="cakebox/cake_edit.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"Cake updated successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Cake updation failed")
        return super().form_invalid(form)
    
    
@signin_required
@is_admin
def remove_cakeview(request,*args,**kwargs):
    id=kwargs.get("pk")
    Cakes.objects.filter(id=id).delete()
    return redirect("cake-list")

@method_decorator(decs,name="dispatch")
class CakeVarientCreateView(CreateView):
    template_name="cakebox/cakevarient_add.html"
    model=CakeVarients
    form_class=CakeVarientForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=Cakes.objects.get(id=id)
        form.instance.cake=obj
        messages.success(self.request,"varient has been added")
        return super().form_valid(form)
    
@method_decorator(decs,name="dispatch")   
class CakeDetailView(DetailView):
    template_name="cakebox/cake_detail.html"
    model=Cakes
    context_object_name="cake"

@method_decorator(decs,name="dispatch")
class CakeVarientUpdateView(UpdateView):
    template_name="cakebox/cakevarient_edit.html"
    model=CakeVarients
    form_class=CakeVarientForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"Cake varient updated successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Cake varient updation failed")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_obj=CakeVarients.objects.get(id=id)
        cake_id=cake_varient_obj.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})
        
  
@signin_required
@is_admin
def remove_varient(request,*args,**kwargs):
    id=kwargs.get("pk")
    CakeVarients.objects.filter(id=id).delete()
    return redirect("cake-list")

@method_decorator(decs,name="dispatch")
class OfferCreateView(CreateView):
    template_name="cakebox/offer_add.html"
    form_class=OfferForm
    model=Offers
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=CakeVarients.objects.get(id=id)
        form.instance.cakevarient=obj
        messages.success(self.request,"offer added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"offer adding failed")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_obj=CakeVarients.objects.get(id=id)
        cake_id=cake_varient_obj.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})
    

@signin_required
@is_admin    
def offer_delete(request,*args,**kwargs):
    id=kwargs.get("pk")
    offer_obj=Offers.objects.get(id=id)
    cake_id=offer_obj.cakevarient.cake.id
    offer_obj.delete()
    return redirect("cake-detail",pk=cake_id)


@signin_required

def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class IndexView(TemplateView):
    template_name="cakebox/index.html"

@signin_required
@is_admin
def remove_review(request,*args,**kwargs):
    id = kwargs.get("pk")
    review_obj = Reviews.objects.get(id=id)
    cake_id = review_obj.cake.id
    review_obj.delete()
    return redirect("cake-detail",pk=cake_id)



      
    

    



    

    

    



    
