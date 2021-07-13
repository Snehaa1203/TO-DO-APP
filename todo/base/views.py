from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy #to redirect 
from django.contrib.auth.views import LoginView,LogoutView, redirect_to_login
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.
class CustomLoginView(LoginView):
	template_name='base/login.html'
	fields='__all__'
	redirect_authenticated_user=True
	def get_success_url(self):
		return reverse_lazy('tasks')
	
class RegisterPage(FormView): 
	template_name='base/register.html'
	form_class=UserCreationForm
	redirect_authenticated_user=True
	success_url=reverse_lazy('tasks')
	def form_valid(self,form):
		user=form.save()
		if user is not None:
			login(self.request,user)
		return super(RegisterPage,self).form_valid(form)
	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage,self).get(*args,**kwargs)


class TaskList(LoginRequiredMixin,ListView):
	 model=Task
	 context_object_name='tasks'
	 def get_context_data(self,**kwargs): #to get user specific data
		 context=super().get_context_data(**kwargs)
		 context['tasks']=context['tasks'].filter(user=self.request.user)
		  #filtering specific users task
		 context['count']=context['tasks'].filter(Completed=False).count()
		 search_input=self.request.GET.get('Search-Area')or ''
		 if search_input:
			 context['tasks']=context['tasks'].filter(title__icontains=search_input)
			 context['search_input']=search_input
		 return context

    

class TaskDetail(LoginRequiredMixin,DetailView):
	model=Task
	context_object_name='task'
	template_name="base/task.html" #overwriting inbuilt task_detail.html temp name

class TaskCreate(LoginRequiredMixin,CreateView):
   model=Task
   fields=['title','Description','Completed'] #all feilds in the modelform provided by createview.all feilds in model class are filled by default by using'_all_'now its changed to some specific feilds
   success_url=reverse_lazy('tasks') #redirect to main page
   def form_valid(self, form):
	   form.instance.user=self.request.user
	   return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView): 
	 model=Task    
	 fields=['title','Description','Completed']
	 success_url=reverse_lazy('tasks') #looks for same template name as createview

class TaskDelete(LoginRequiredMixin,DeleteView): 
	 model=Task    
	 context_object_name='task'
	 success_url=reverse_lazy('tasks')
