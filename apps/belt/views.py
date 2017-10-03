from django.shortcuts import render, redirect, HttpResponse,reverse
from django.contrib.messages import error
from django.contrib import messages
from models import *
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def index(request):
    return render(request, 'belt/index.html')


def create(request):
    print 
    errors = User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    
    messages.success(request, "Successfully registered!")
    if not errors:
        #make our new user hash password
        hashed = bcrypt.hashpw((request.POST['password'].encode()), bcrypt.gensalt(5))
        new_user = User.objects.create(
        name=request.POST['name'],
        email=request.POST['email'],
        password=hashed,
        dob = request.POST['date']

    )
    request.session['new_user_id'] = new_user.id    

    return redirect('/')
def process(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)

        return redirect('/')
    
    
    email = request.POST['email']    
    password = request.POST['password']
    user_email = User.objects.get(email = email)   
    request.session['user_id'] = user_email.id    

    if email == user_email.email and password == user_email.password:    
       
       return redirect('/main')
    else:
        return redirect('/')
    # return redirect('/main')
    


def main(request):   
    loged_user = User.objects.get(id=request.session['user_id'])    

    request.session['user_name'] = loged_user.name
    user_quotes = loged_user.favorites_quotes.all()
    print user_quotes
    

    context = {
        "user_quotes": loged_user.favorites_quotes.all(),
        "other_users": Quote.objects.all().exclude(users_favorites=loged_user)
        # "name": User.objects.get(id=request.session['user_id'])
    }

    # Quote.objects.all().exclude(users_favorites=loged_user)

       
    # return redirect('/home')

    return render(request, 'belt/main.html', context)



def add(request):
    errors = User.objects.validate_quote(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)

        return redirect('/main')
    loged_user = User.objects.get(id=request.session['user_id'])
    quoted_by = request.POST['quoted_by']
    quote = request.POST['new_quote']
    create_quote = loged_user.quotes.create(quote = quote, quoted_by = quoted_by)
    quote_id = create_quote.id
    new_quote = Quote.objects.get(id = quote_id)
    # loged_user.favorites_quotes.add(new_quote)
    return redirect('/main')


def list(request, id):
    loged_user = User.objects.get(id=request.session['user_id'])
    fev_quote = Quote.objects.get(id = id)
    loged_user.favorites_quotes.add(fev_quote)


    return redirect('/main')
def remove(request, id):
    loged_user = User.objects.get(id=request.session['user_id'])
    the_quote = Quote.objects.get(id=id)

    the_quote.users_favorites.remove(loged_user)    

    return redirect('/main')

def user(request, id):
    the_quote = Quote.objects.get(id=id)    
    request.session['quote_user_id'] = the_quote.user.id 
    context = {
    "selected_user": User.objects.get(id=request.session['quote_user_id']),
    "user_all_quotes": User.objects.get(id=request.session['quote_user_id']).quotes.all(),
    "num_quotes": User.objects.get(id=request.session['quote_user_id']).quotes.count()
    }
    # quoted_by = 

    
    

    return render(request, 'belt/display.html', context)
