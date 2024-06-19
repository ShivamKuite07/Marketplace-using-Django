<!-- All in CMD -->

<!-- for css use -->
 <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"> <!-- Use jsDelivr CDN for Tailwind CSS -->


<!-- To create project  called myblog-->
django-admin startproject puddle

<!-- root directory -->
the directory where manage.py is located.

in root directory create a app as core.
<!-- in root folder -->
python manage.py startapp core


add templates folder in core directory.

now.

setting.py
```py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR , 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {}
        ...
    }


INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'django.contrib.staticfiles',
    'core'
]
```

in puddle urls.py
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'))
]
```

in core urls.py
```py
from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

in views.py
```py
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

```

<!-- New stuff -->
<!-- incluing content like php -->
we create  templates folder in core, in which we create core folder again...
we got 2 files, index.html and base.html

we can include content from index.html to base.html.

base.html, it contains the entire html page.
here the word content is like name of include file. 
it could be {% block title %} etc
```html
    <div>
        {% block content %}
        {% endblock %}
    </div>
```

index.html
```html

{% extends 'core/base.html' %}
{% block content %}
<h1>
    THis is somethingnfnlrw.
</h1>
{% endblock %}

```
<!-- contact.html -->
add a contact.html with same principle.

we can use url for moving to that page

<li><a href="{% url 'contact' %}" >Contact</a></li>



<!-- Lets add another app for items -->
python manage.py startapp item

lets go to this item, and create model (table) Category

```py
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
```
we know that django adds "s" to name as default but to change that we add the meta class here. 

self.name helps in showing values name instead of objs in table.


Make migration:
python manage.py makemigrations
python manage.py migrate

we go to migration folder and 0001_intial.py file, there we can see that new table is created.

add it to admin now, for model to be visible.

<!-- Create user -->
user: admin
pass: admin123


We added another model: item

Dont forget to migrate.

for images, dont forget pillow lib and 
add this in setting.py for creating folders, it will create a new folder called media.

```py
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
in puddle urls.py import them, and modify this for displaying images
```py
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('core.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
```

Now lets add some items manully, ok done.

now lets display this items on index page.

import all models from items to core.
```py
from item.models import Category, Item

# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6] # top 6 items
    categories = Category.objects.all()
    
    context = {
        "items": items,
        "categories": categories
    }
    return render(request, 'core/index.html', context)
```

now call this in index page.


now lets add details page, lets add a new view in view.py in item folder.
```py
from django.shortcuts import get_object_or_404, render

from item.models import Item

# Create your views here.

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {
        'item': item
    }
    return render(request, 'item/detail.html', context )
```

create a folder calle templates/item/ in item folder, for detail.html

lets add urls.py in item folder.

dont forget to update the puddle.urls.py
```py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('item.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
```

lets add related items too.
```py
 related_items = Item.objects.filter(category=item.category, is_sold = False).exclude(pk=pk)[0:3]

    context = {
        'item': item,
        'related_items': related_items
    }
```


<!-- Lets add Signup 55:55-->

in core' folder, create a file called forms.py
```py


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter your name',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter your email address',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2 ' 
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password again',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))
```
now import this in views.
```py
from django.shortcuts import redirect, render, redirect
from item.models import Category, Item
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/') 
    else:
        form = SignupForm()
    context = {
        "form": form,
    }
    return render(request, 'core/signup.html', context)
```
add it in urls.py 
```py
from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'), 
]
```
add call it like, base page.
<a href="{% url 'signup' %}">Sign up</a>

signup page code:
```html
{% block content %}
    <div class="w-1/2 my-6 mx-auto p-6 bg-gray-100 rounded-xl" >
        <h1 class="mb-6 text-3xl">Sign up</h1>

        <form method="POST" action="">
            {% csrf_token %}

            {% comment %} {{ form.as_p }} {% endcomment %}

            

            <div class="mb-3">
                <label class="inline-block mb-2">Username</label><br>
                {{form.username}} <br>

                <label class="inline-block mb-2">Email</label><br>
                {{form.email}} <br>

                <label class="inline-block mb-2">Password</label><br>
                {{form.password1}} <br>

                <label class="inline-block mb-2">Repeat Password</label><br>
                {{form.password2}} <br>

                {% if form.errors or form.non_field_errors %}
                    <div class="mb-6 p-6 bg-red-100 rounded-xl">
                        
                        {% for field in form  %}
                            {{field.errors}}
                        {% endfor %}
                            
                        {{form.non_field_errors}}
                    </div>
                {% endif %}

            </div>

            <button class="py-4 px-8 text-lg bg-green-500 hover:bg-green-700 rounded-xl text-white">Submit</button>
        </form>
    </div> 
{% endblock content %}
    
```


this will save user when created.


<!-- Login  -->

we import this for authentication in forms.py 
```py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
```

urls.py
```py
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'), 
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form = LoginForm), name='login'),
]
```

now when we try to login django tries to send us to default loc.
so we modify that.  go to settings.py
```py
ALLOWED_HOSTS = []

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```



resume at 1:15:40 (Adding Items)

<!-- Lets add items now -->
lets create a forms.py in items folder.
```py
from django import forms
from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category','name','description','price','image')

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
             'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
            })
        }
```

now we'll add a view for it too.
we'll only allow to add items if user is logged in.
```py
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False) # commit=False allows us to leave few values that we havent passed.
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)

    else:
        form = NewItemForm()
    context = {
        'form': form,
        'title': 'New Item',
    }
    return render(request, 'item/form.html', context)
```
lets create a form in item/template/item/form.html
```html

{% extends 'core/base.html' %}
{% block title %} {{title}} {% endblock title %}
{% block content %}

<h1 class="mb-6 text-3xl">{{title}}</h1>

<form method="POST" action="" enctype="multipart/form-data">
    {% csrf_token %}

    <div class="space-y-4">
        {{form.as_p}}
    </div>

    {% comment %} if we got any error {% endcomment %}
    {% if form.errors or form.non_field_errors %}
        <div class="mb-6 p-6 bg-red-100 rounded-xl">
            
            {% for field in form  %}
                {{field.errors}}
            {% endfor %}
                
            {{form.non_field_errors}}
        </div>
    {% endif %}

    <button class="py-4 px-8 text-lg bg-green-500 hover:bg-green-700 rounded-xl text-white">Add Item</button>
  

</form>

{% endblock content %}
```
lets add this new, in urls.py too.

and now lets call it in base.html it will autocheck if user is authenticated.

 <a href="{% url 'item:new' %}" class = "">New Item</a>


 <!-- 1:28:30 -->
 <!-- Dashboard -->

lets add dashboard for editing, updating items that we have created.

create a new app: dashboard
add it to installed apps in settings.py
and also add it to main urls.py

now we dont want any models here, we'll just import the model:Item.
```py views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from item.models import Item

# Create your views here.

@login_required
def index(request):
    items = Item.objects.filter(created_by = request.user)

    context = {
        'items': items
    }
    return render(request, 'dashboard/index.html', context)
```

create a folder called templates/dashboard/index.html

we took the index file from core folder and pasted it here.
as we are alraedy filter out the data in views file. it can work.

lets create urls.py here.
```py
from django.urls import path
from  . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
]
```