from django.shortcuts import render,HttpResponse,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

class CustomLogin(LoginView):
    template_name = 'base/Login.html'
    fields='__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('tasklist')

class Register(FormView):
    template_name = 'base/Register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasklist')
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(Register,self).form_valid(form)
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(Register, self).get( request,*args, **kwargs)



class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'Tasks'
    template_name = 'base/TodoList.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['Tasks']=context['Tasks'].filter(user=self.request.user)
        context['count'] = context['Tasks'].filter(complete=False).count()
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['Tasks']=context['Tasks'].filter(title__startswith=search_input)
        context['search_input']=search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'Task'
    fields = ['title', 'description', 'complete']
    template_name = 'base/TodoDetail.html'

class TaskCreation(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'base/TodoCreate.html'
    fields = ['title','description','complete']
    success_url =reverse_lazy('tasklist')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreation,self).form_valid(form)
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    template_name = 'base/TodoCreate.html'
    success_url =reverse_lazy('tasklist')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    fields = ['title']
    context_object_name = 'Task'
    template_name = 'base/TodoConfirmation.html'
    success_url =reverse_lazy('tasklist')