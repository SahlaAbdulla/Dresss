from django.contrib import admin
from Maria.models import Category,Color,Dress,DressVarient,Size,User


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Dress)
admin.site.register(Color)
admin.site.register(DressVarient)


