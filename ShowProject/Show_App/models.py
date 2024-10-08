from django.db import models
import re
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        # First and Last Name validation
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name should be at least 3 characters long."
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name should be at least 3 characters long."
            
        # Email validation    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"   
        if len(postData['email']) < 10:
            errors['email'] = "Email should be at least 10 characters long."
            
        # Password validation    
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 4 characters long."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match!"
            
        return errors 
    
class ShowManager(models.Manager):
    def show_validator(self, postData, show_id=None):
        errors = {}
        
        # Title validation
        if len(postData['title']) < 3: 
            errors['title'] = "Show title should be more than 2 characters."
        elif show_id and Show.objects.exclude(id=show_id).filter(title=postData['title']).exists():
            errors['title'] = "Show title must be unique."

        # Network validation
        if len(postData['network']) < 3:
            errors['network'] = "Show network should be more than 2 characters."

        # Release date validation
        try:
            release_date = postData['release_date']
            if not release_date:
                errors['release_date'] = "Release date is required."
            else:
                release_date_obj = date.fromisoformat(release_date)
                if release_date_obj > date.today():
                    errors['release_date'] = "Release date cannot be in the future."
        except ValueError:
            errors['release_date'] = "Invalid date format. Please use YYYY-MM-DD."

        # Comment validation
        if len(postData['comment']) < 10: 
            errors['comment'] = "Comment should be at least 10 characters long."

        return errors          

#-- User Model     
class User(models.Model):
    first_name = models.CharField(max_length=50)    
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()

    
    def __str__(self):
        return f"{self.first_name} { self.last_name}" 

#-- Show Model    
class Show(models.Model):
    title = models.CharField(max_length=100, unique=True)
    network = models.CharField(max_length=50)
    comment = models.TextField()
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()
    # recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    users = models.ManyToManyField(User, related_name='shows')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_shows', null=True, blank=True)  



    def __str__(self):
        return f"{self.title} ({self.network}) -created by {self.created_by}"
    
#-- Show Comments' Model    
class ShowComment(models.Model):
    content = models.CharField(max_length=255)  # Changed from context to content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        user_display = self.user.first_name if self.user else "Anonymous"
        show_display = self.show.title if self.show else "No Show"
        return f"{user_display} on {show_display}: {self.content[:20]}"
    
    
    


    
        
    
        