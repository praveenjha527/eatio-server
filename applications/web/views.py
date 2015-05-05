from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import Http404,HttpResponse

from applications.accounts.models import PasswordReset
from applications.web.form import PasswordForm
from applications.web.models import Contact
import json as json
from django.views.decorators.csrf import csrf_exempt
# Get logger
import logging
log = logging.getLogger("logentries")


class ContactUs(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ContactUs, self).dispatch(request, *args, **kwargs)


    def post(self,request):
         if request.method == 'POST':
             name = request.POST.get('name')
             email = request.POST.get('email')
             message = request.POST.get('message')

             response_data = {}

             post = Contact(name=name, email=email, message=message)
             post.save()
             return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

class PasswordResetView(View):
    template_name = "password_reset/password_reset.html"
    form_class = PasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class() 
        try:
            pass_obj = PasswordReset.objects.get(temp_key=kwargs['token'],reset=False)
        except PasswordReset.DoesNotExist:
            raise Http404
        return render(request, self.template_name, {'form': form})

    def post(self, request, ** kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                pass_obj = PasswordReset.objects.get(temp_key=kwargs['token'],reset=False)
                pass_obj.user.set_password(form.cleaned_data['password'])
                pass_obj.user.save()
                pass_obj.reset = True
                pass_obj.save()
                return render(request, self.template_name, {'form': form,"message":"Your password has been successfully changed"})
            except PasswordReset.DoesNotExist:
                raise Http404
        return render(request, self.template_name, {'form': form})


class HomePageView(View):
    template_name = "home.html"
    form_class = PasswordForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )





