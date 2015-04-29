from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions



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


