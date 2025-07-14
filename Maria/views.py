from django.shortcuts import render,redirect

from django.views.generic import View

from Maria.models import User,Dress,DressVarient,Size,Cart,Color,OrderItem,Order

from Maria.forms import SignUpForm,SignInForm,OrderForm

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

from Maria.decorators import signin_required

from twilio.rest import Client




class SignUpView(View):

    template_name='register.html'

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        from django.contrib.auth import login

# Inside post()
        if form_instance.is_valid():
         user_inst = form_instance.save(commit=False)
         user_inst.is_active = True
         user_inst.save()
        login(request, user_inst)  # ✅ log them in directly
        return redirect("index")   # ✅ go to index



            

        
# class OtpVerifyView(View):

#    template_name='otp.html'

#    form_class=OtpVerifyForm

#    def get(self,request,args,*kwargs):

#         form_instance=self.form_class()

#         return render(request,self.template_name,{'form':form_instance})     
    
#    def post(self,request,args,*kwargs):  
       
#        otp=request.POST.get("otp")

    #    try:   

       
    #      user_object=User.objects.get(otp=otp)

    #      user_object.is_active=True

    #      user_object.is_verified=True

    #      user_object.otp=None

    #      user_object.save()

    #      return redirect("login")

    #    except:  

    #       return redirect("otp")     

# views.py
from django.contrib.auth import authenticate, login

class SignInView(View):
    template_name = 'signin.html'
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class()
        return render(request, self.template_name, {'form': form_instance})

    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():
            uname = form_instance.cleaned_data.get("username")
            pwd = form_instance.cleaned_data.get("password")

            print(f"Form Valid ✅ — Username: {uname}, Password: {pwd}")

            user_object = authenticate(request, username=uname, password=pwd)

            print(f"Authenticated User: {user_object}")

            if user_object is not None and user_object.is_active:  # ✅ safe check
                login(request, user_object)
                print("✅ Login successful. Redirecting to index.")
                return redirect('index')

        print("❌ Login failed. Either invalid form or incorrect credentials.")
        return render(request, self.template_name, {'form': form_instance})


           

@method_decorator(signin_required,name="dispatch")
class IndexView(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Dress.objects.all()

        return render(request,self.template_name,{'dresses':qs})
    
       
@method_decorator(signin_required,name="dispatch")    
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')   
     
@method_decorator(signin_required,name="dispatch")    
class DressDetailView(View):

    template_name="dressdetail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Dress.objects.get(id=id)

        return render(request,self.template_name,{'dress':qs})
    

    
@method_decorator(signin_required,name="dispatch")
class AddCartView(View):

    def post(self,request,*args,**kwargs):

        dress_varient_id=request.POST.get("varient")

        dress_varient_instance=DressVarient.objects.get(id=dress_varient_id)

        color_id=request.POST.get("color")

        color_instance=Color.objects.get(id=color_id)

        qty=request.POST.get("quantity")

        Cart.objects.create( dress_varient_object=dress_varient_instance,color_object=color_instance,quantity=qty,owner=request.user)

        return redirect("index")
    
@method_decorator(signin_required,name="dispatch")    
class CartSummaryView(View):

    template_name='cart_summary.html' 

    def get(self,request,*args,**kwargs):

        qs=Cart.objects.filter(owner=request.user,is_order_placed=False)   

        total_price=sum([c.item_total() for c in qs])

        return render(request,self.template_name,{"data":qs,"total_price":total_price})  
    
     
@method_decorator(signin_required,name="dispatch")
class CartItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Cart.objects.get(id=id).delete()

        return redirect("cart-summary")    
@method_decorator(signin_required,name="dispatch")
class PlaceOrderView(View):

    template_name="place_order.html"

    form_class=OrderForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        qs=Cart.objects.filter(owner=request.user,is_order_placed=False)

        total_price=sum([c.item_total() for c in qs])

        return render(request,self.template_name,{"form":form_instance,"cartitems":qs,"total":total_price})  
    
    def post(self,request,*args,**kwargs):

       form_instance=self.form_class(request.POST)

       form_instance.instance.customer=request.user

       order_object=form_instance.save()

       cart_items=Cart.objects.filter(owner=request.user,is_order_placed=False)

       for co in cart_items:
           
           OrderItem.objects.create(
               order_object=order_object,
               dress_varient_object=co.dress_varient_object,
               quantity=co.quantity,
               price=co.dress_varient_object.price
               
           )

           co.is_order_placed=True

           co.save()   

           return redirect("order-success")
@method_decorator(signin_required,name="dispatch")       
class PaymentSuccessView(View):

    template_name="payment_success.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)  

        return render(request,self.template_name) 
@method_decorator(signin_required,name="dispatch")    
class OrderSummaryView(View):
     
     template_name='order_summary.html'

     def get(self,request,*args,**kwargs):
         
         qs=Order.objects.filter(customer=request.user).order_by("-created_date")

         return render(request,self.template_name,{"orders":qs})