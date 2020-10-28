from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers,models,permissions


class HelloApiView(APIView):
    """Test Api view"""
    serializer_class = serializers.HelloSerializer
    def get(self,request ,format = None):
        """returns list of api view features"""
        an_apiview = ['Uses HTTP methods as functions like get,patch,put,post,delete','Is similar to traditional django view','gives you most control over your application logic','Is mapped manually to URLs']
        return Response({'message':'Hello!','an_apiview': an_apiview})
    def post(self,request):
        """create hello msg with our name"""
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            name =serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,pk=None):
        """Handel updating an object"""
        return Response({'method':'PUT'})
    def patch(self,request,pk=None):
        """handel a partial updating of an object"""
        return Response({'method':'PATCH'})
    def delete(self,request,pk=None):
        """delete an object"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API viewset"""
    serializer_class = serializers.HelloSerializer
    def list(self,request):
        """return a hello message"""
        a_viewset=['uses actions like create,update, partially update,destroy,list,retrieve','automatically maps to URLs using routers','provide more funtionality with less code']
        return Response({'message':'Hello!','a_viewset':a_viewset})
    def create(self,request):
        """create a new Hello message"""
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            name =serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        """Handel getting an object by its id"""
        return Response({'method':'RETRIEVE'})
    def update(self,request,pk=None):
        """handel updating an object"""
        return Response({'method':'UPDATE'})
    def partial_update(self,request,pk=None):
        """partially updating an object"""
        return Response({'method':'PARTIAL UPDATE'})
    def destroy(self,request,pk=None):
        """delete an object"""
        return Response({'method':'DESTROY'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """handel creating , updating and destroying an profiles"""
    serializer_class=serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """handel creating user authencation"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """handling creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated)

    def perform_create(self, serializer):
        """set user profile to logged in user"""
        serializer.save(user_profile = self.request.user)