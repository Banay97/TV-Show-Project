from django.shortcuts import render, redirect
from .models import User, Show
import bcrypt
from django.contrib import messages


# Create your views here.
def sign_up(request):

    return render(request, 'SignUpPage.html')
#--Sign in render page
def sign_in(request):
    return render(request, 'SignInPage.html')

def home_page(request):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    show = Show.objects.all()    
    return render(request, 'HomePage.html', {'user': user, 'shows':show} )

def create_account(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('sign_up')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            user = User.objects.create(first_name = first_name, last_name=last_name, email = email, password = hashed_password)
            request.session['user_id'] = user.id
            return redirect('home_page')
    return redirect('sign_up')  

#-- Entering your account function         
def enter_account(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email =email).first()
        
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['user_id'] = user.id
            messages.success(request, 'You successfully Sign in')
            return redirect('home_page')
        else:
            messages.error(request, "Invalid Email or Password!")
            redirect('sign_in')

    return redirect('sign_in')         
            
def sign_out(request):
    if request.method == 'POST':
        request.session.flush() 
        return redirect('sign_in') 
    return redirect('home_page')

def create_show_page(request):
    return render(request, 'CreateShowPage.html')

def create_show(request):
    if request.method == 'POST':
        errors = Show.objects.show_validator(request.POST)  
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('create_show')

        title = request.POST['title']
        network = request.POST['network']
        release_date = request.POST['release_date']
        comment = request.POST['comment']

        if Show.objects.filter(title=title).exists():
            messages.error(request, 'A show with the same title already exists!')
            return redirect('create_show')

        if 'user_id' not in request.session:
            messages.error(request, 'You must be logged in to create a show.')
            return redirect('sign_in')

        user = User.objects.get(id=request.session['user_id'])  
        
        show = Show.objects.create(
            title=title,
            network=network,
            release_date=release_date,
            comment=comment,
        )
        show.save() 
        messages.success(request, 'Show created successfully!')
        return redirect('home_page') 
    return render(request, 'HomePage.html', {'show': {}})

def update_show(request, show_id):
    show = Show.objects.filter(id=show_id).first()
    
    if not show:  # Check if the show exists
        messages.error(request, 'Show not found.')
        return redirect('home_page')

    user = None  # Initialize user variable

    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, 'You must be logged in to update a show.')
            return redirect('sign_in')

        user = User.objects.get(id=request.session['user_id']) 
        
        errors = Show.objects.show_validator(request.POST, show_id)

        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='update_show')
            return render(request, 'UpdateShowPage.html', {'user': user, 'show': show})

        show.title = request.POST['title']
        show.network = request.POST['network']
        show.release_date = request.POST['release_date']
        show.comment = request.POST['comment']
        show.save()
        
        messages.success(request, 'Show updated successfully!')
        return redirect('home_page')

    user = User.objects.get(id=request.session['user_id'])  

    return render(request, 'UpdateShowPage.html', {'user': user, 'show': show})
        
        
def show_details(request, show_id):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    show = Show.objects.get(id=show_id)
    return render(request, 'ShowDetailsPage.html', {'show': show , 'user':user})
        


def delete_show(request, show_id):
    if request.method == 'POST':
        show = Show.objects.filter(id=show_id).first()        
        show.delete()
        messages.success(request, 'Show deleted successfully!')
        return redirect('home_page')
    
    