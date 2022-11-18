++++Tests+++++

### This Document Contains a bunch of things I learnt while building this project and some jokes 🤡🤝🏾
### C'est mon bebe 😂

ko need - Input a block of html in description and see if it displays a html, if it does then add escape(variable_name) in jinja..... althogh, `{{variable_name}}` wouldn't display html unless you say `{{variable_name|safe}}` - Dr Chuck

slug vs str in py/django ---incase you're confused mf 
```py
path('listing/<int:listing_id>', views.listing, name='listing_by_id')
```
`int` can be `slug` or `str`

we could also do `{{ variable_name|length }}` to get the length of the item(s) in the variable eg `{{ letter|length }}` will give us two if 'letters' : ['A', 'B']

we could also do `{{ outer.inner }}` if outer is pointing to a dictionary that has a key of inner 
```py
'outer' : {'inner' : 2}
```

in urls.py we can add the app name before the urlpattern like this
```py
app_name = 'yourapp'
```
---
```py
urlpatterns = [
    path('', yadiyadiyada, name='test' )
]
```

this makes it possible for us to link one application to each other e.g in `myapp/index.html`
```html
<a href="{% url 'yourapp:test' %}">
```

in the urls.py of your project(the oga patapata i.e the boss) you can add a namespace attribute to give you refrence options e.g.
```py
urlpatterns = [
    path('yourapp/', include('yourapp.urls', namespace='strangerapp'))
]
```

now I can say
```html
<a href="{% url 'strangerapp:test' %}">
```
which is still the same as
```html
<a href="{% url 'yourapp:test' %}">
```

we can also do 
```py
response.set_cookie('var', value)
```
expires when browser closes and
```py
response.set_cookie('var', value, max_age=1000)
```
1000 seconds until expire - cookies can be used to store data in browser..... like in a cbt, when connection is lost, answers and questions might be in the cookies.... Basically allows you to continue from where you stop, the server sends the cookie to the browser... each session have their own cookie

`del(dict['key'])` is a standard point on syntax to remove an entry from a dictionary

django sessions is encoded with base 64, if you want to look at the data... you can open a shell
```py
import base64
x = base64.b64decode('datastring')
#you can print x but there will still be some jargons in the code

import json
data = json.loads(x[41:])
# 41 is the count of jargon before the column starting from 0... you can do .length() 
print(data)
```
You can write a script to load a bunch of data (e.g csv file) into the db. You'll do
```py
pip install django-extensions
```
then add `django_extensions` to installed apps. Your csv file will look something like this:
```
Name, Title, Age
Yusuf, Engineer, 20
Bill, Founder, 65
David, Professor, 50
Brian, Professor, 40
```
in the scripts folder we'll add `__init__.py`. It can be empty, it's just there to tell us that the folder contains files that can be imported into the python application.... Just to be clear, the script folder is the one incharge of `.py` files you are using to perform magic on the db and csv file.

`example_script.py`

```py
import csv
from app.model import Model1, Model2

def run():
    f = open('app/file.csv')
    reader = csv.reader(f)
    next(reader) #Move past the header

    # you can do as you like 👻
    Model1.objects.all()
    Model2.objects.all().delete()

    for row in reader:
        print(row)

        # This if for a one to many relationship. It checks if the title exist, if it doesn't, it creates it. 'b' is the actual variable... created returns boolean.
        b, created = Model2.objects.get_or_create(title=row[1])

        c = Model1(name=row[0], title=b, age=row[2])
        c.save()
```
bienvenue 🤝🏾

So after everything, you'll do
```
python manage.py runscript example_script
```

### Login and Logout
- `Reverse` gets the route 
- `"next="` parameter tells login/logout where to redirect user after login/logout e.g. `{% url 'logout' %}?next={% url 'authz:open' %}`
- We can use`{% if user.is_authenticated %}` in the html and `if request.user.is_authenticated` in views.py, to filter what to show to user that are logged in or not
- `{% url 'login' %}?next={{ 'request.path' }}` returns user to where they were after they login
- `LoginRequiredMixin` allows our view if and only if the user is logged in.
```py
# example
from django.contrib.auth.mixins import LoginRequiredMixin
class ProtectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/main.html')
```
- 
# H<sub>2</sub>O
## H<sub>2</sub>O
### H<sub>2</sub>O
#### H<sub>2</sub>O
##### H<sub>2</sub>O
---
<b>more or less</b> 5H<sub>2</sub>O and we can decide to do 2H<sub>2</sub>O + 3H<sub>2</sub> + O<sub>2</sub>

H<sub>2</sub>O


<marquee class='mad'>😏👻🤝🏾 #Yusuf 🤡🧑🏾‍💻🚀</marquee>
<style>
    .mad{
        color: orange;
        outline: 2px green solid;
        margin: 10px;
        padding: 10px;
        border-radius: 5px;
    }
</style>
You still don't know how to do this 😏, steal the code 👇🏾
```html
<marquee class='mad'>😏👻🤝🏾 #Yusuf 🤡🧑🏾‍💻🚀</marquee>
<style>
    .mad{
        color: orange;
        outline: 2px green solid;
        margin: 10px;
        padding: 5px;
        border-radius: 5px;
    }
</style>
```
Signed </br>
Yuskhosmith