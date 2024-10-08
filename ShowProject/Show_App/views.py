from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Show ,ShowComment
import bcrypt
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def sign_up(request):

    return render(request, 'SignUpPage.html')
#--Sign in render page
def sign_in(request):
    return render(request, 'SignInPage.html')

#--Home Page rendering and making sure the user info is sorted in the session and ensure that all the shows info will appear
def home_page(request):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    shows = Show.objects.all()    
    return render(request, 'HomePage.html', {'user': user, 'shows':shows} )

#-- Create account for any user 
def create_account(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='signup')
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
            messages.error(request, "Invalid Email or Password!", extra_tags='signin' )
            redirect('sign_in')

    return redirect('sign_in')         

#-- Sign out from you account and cleaning the session from all you data            
def sign_out(request):
    if request.method == 'POST':
        request.session.flush() 
        return redirect('sign_in') 
    return redirect('home_page')

#-- rendering function for create show page
def create_show_page(request):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    return render(request, 'CreateShowPage.html', {'user':user})

#-- Create Show Function according to the owner of the account 
def create_show(request):
    if request.method == 'POST':
        user = None 
        errors = Show.objects.show_validator(request.POST)  
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='create_show')
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
        
        show = Show.objects.create(title=title, network=network, release_date=release_date, comment=comment, created_by=user )
        show.save() 
        messages.success(request, 'Show created successfully!')
        return redirect('home_page')
    
    user = User.objects.get(id=request.session['user_id']) 
    return render(request, 'CreateShowPage.html', {'show': {}, 'user':user})


#--Update Show Function 
def update_show(request, show_id):
    show = Show.objects.filter(id=show_id).first()
    
    if not show:  
        messages.error(request, 'Show not found.' , extra_tags='update_show')
        return redirect('home_page')

    user = None 

    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, 'You must be logged in to update a show.', extra_tags='update_show')
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
        
        messages.success(request, 'Show updated successfully!', extra_tags='update_show')
        return redirect('home_page')

    user = User.objects.get(id=request.session['user_id'])  

    return render(request, 'UpdateShowPage.html', {'user': user, 'show': show})

# -- Show Details Function         
def show_details(request, show_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    show = Show.objects.filter(id=show_id).first()

    if not show:
        messages.error(request, 'Show not found.')
        return redirect('home_page')

    is_owner = (show.created_by == user) if user else False

    return render(request, 'ShowDetailsPage.html', {'show': show,'user': user,'is_owner': is_owner })
        

#-- Delete Show Function 
def delete_show(request, show_id):
    if request.method == 'POST':
        show = Show.objects.filter(id=show_id).first()        
        show.delete()
        messages.success(request, 'Show deleted successfully!')
        return redirect('home_page')
    return redirect('home_page')

# -- Create Comment Function
@login_required 
def create_comment(request, show_id):
    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, 'You must be logged in to comment.', extra_tags='comment')
            return redirect('sign_in')

        user = User.objects.get(id=request.session['user_id'])
        show = get_object_or_404(Show, id=show_id) 

        content = request.POST.get('content', '').strip()
        if content:
            ShowComment.objects.create(content=content, user=user, show=show)
            messages.success(request, 'Comment added successfully!',extra_tags='comment')
        else:
            messages.error(request, 'Comment cannot be empty.', extra_tags='comment')

        return redirect('show_details', show_id=show.id)  

    return redirect('show_details', show_id=show_id)

#-- Delete Comment Function
@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = ShowComment.objects.filter(id=comment_id).first()
        if comment:
            if request.user.id == comment.user.id:
                comment.delete()
                messages.success(request, 'Comment deleted successfully!', extra_tags='comment')
            else:
                messages.error(request, 'You do not have permission to delete this comment.', extra_tags='comment')
        else:
            messages.error(request, 'Comment not found.', extra_tags='comment')
        return redirect('show_details', show_id=comment.show.id)
    
    return redirect('show_details')     
                        
    
        
        
        
    