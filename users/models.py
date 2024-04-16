from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import uuid

class  Profile(models.Model):
     user=models.OneToOneField( 
        User,on_delete=models.CASCADE,null=True,blank=True)
     name=models.CharField(max_length=200,null=True,blank=True)
     email=models.EmailField(max_length=200,null=True,blank=True)
     super=models.BooleanField(default=False)
     firstname=models.CharField(max_length=200,null=True,blank=True)
     secondname=models.CharField(max_length=200,null=True,blank=True)
     username=models.CharField(max_length=200,null=True,blank=True)
     image = models.ImageField(upload_to='images_profile/', null=True, blank=True)
     created=models.DateTimeField(auto_now_add=True)
     id = models.AutoField(primary_key=True, editable=False)
     def __str__(self):
        return str(self.user)  

class Session(models.Model):
    created_date = models.DateTimeField(null=True,blank=True)
    session_name = models.CharField(max_length=200)
    session_content=models.CharField(max_length=200)
    image_self = models.ImageField(upload_to='images_session/', null=True, blank=True)
    session_file= models.FileField(upload_to= 'session_file/' , null=True, blank=True)
    profile = models.ManyToManyField(Profile,blank=True,related_name='sessions')  
    def __str__(self):
        return str(self.session_name) 
             

class message (models.Model):
   sender=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
   recipient=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name='messages')
   name=models.CharField(max_length=200,null=True,blank=True) 
   email=models.EmailField(max_length=200,null=True,blank=True) 
   subject=models.CharField(max_length=200,null=True,blank=True) 
   body=models.TextField() 
   is_read=models.BooleanField(default=False,null=True) 
   created=models.DateTimeField(auto_now_add=True)
   id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False) 

   def __str__(self):
       return self.subject
   class Meta:
       ordering=['is_read','-created'] 
def get_profile_image_paths():
    profiles = Profile.objects.all()
    profile_images = {}
    for profile in profiles:
        profile_images[str(profile.id)] = profile.image.path
    return profile_images