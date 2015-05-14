from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions
from django.views.generic import TemplateView

from serializers import AppPreferencesSerializer
from models import AppPreferences


class AppPreferencesView(viewsets.ReadOnlyModelViewSet):
    """
    Allows a GET for the Eatio  app preferences which are same for all users, like after how many times to show the apptentive's comment on reward message box etc

    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = AppPreferencesSerializer
    queryset = AppPreferences.objects.all()

    def retrieve(self, request, *args, **kwargs):

        response = super(AppPreferencesView, self).retrieve(request, *args, **kwargs)

        #send_mixpanel_event(settings.FETCHED_GLOBALPREFS, request.user)
        return response


class TermsConditionsView(TemplateView):
    """
    Returns the Terms and Conditions
    """
    template_name = 'terms-conditions.html'
    def get_context_data(self, ** kwargs):

        context = super(TermsConditionsView, self).get_context_data(** kwargs)
        context['obj'] = AppPreferences.objects.get()
        return context


class PrivacyPolicyView(TemplateView):
    """
    Returns the Terms and Conditions
    """
    template_name = 'privacy-policy.html'
    def get_context_data(self, ** kwargs):

        context = super(PrivacyPolicyView, self).get_context_data(** kwargs)
        context['obj'] = AppPreferences.objects.get()
        return context


class FAQView(TemplateView):
    """
    Returns the Terms and Conditions
    """
    template_name = 'faq.html'
    def get_context_data(self, ** kwargs):

        context = super(FAQView, self).get_context_data(** kwargs)
        context['obj'] = AppPreferences.objects.get()
        return context

