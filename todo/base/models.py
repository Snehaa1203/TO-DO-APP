from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)#user can have many tasks ; User is table provided by Django
	title=models.CharField(max_length=50)
	Description=models.TextField(null=True,blank=True)
	Completed=models.BooleanField(default=False)
	Created=models.DateTimeField(auto_now_add=True) #the date is set up automatically everytime we set a task
	
	def __str__(self):
		return self.title
	class Meta:
		ordering =['Completed'] #to display in order such that incompleted tasks are on the top


    	

