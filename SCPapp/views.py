from rest_framework.parsers import FileUploadParser
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions, status
from django.http import Http404

from .models import File,Interview, User, CommentsPYQ, CommentsExp
from .serializers import FileSerializer, interviewSerializer, CommentsPYQSerializer, CommentsExpSerializer

import logging
logging.basicConfig(filename='pyq.log',format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

"""
USER VIEWS
"""

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    get the details of all the users
    """

    def get(self, request):
        
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

class loginDataId(APIView):
    """
    Retrieve, update or delete a snippet instance based on roll number
    """
    permission_classes = (permissions.AllowAny,)
    def get_object(self, rollNumber):
        try:
            return User.objects.get(rollNumber=rollNumber)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, rollNumber, format=None):
        user = self.get_object(rollNumber)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, rollNumber, format=None):
        user = self.get_object(rollNumber)
        serializer = UserSerializerWithToken(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
END OF USER VIEWS
"""

class interviewData(APIView):
    def get(self, request):
        logging.info('Trying: GET: Interview Exp Data')
        product1 = Interview.objects.filter(verified=True)
        serializer = interviewSerializer(product1, many=True)
        logging.info("Successful: GET: Interview Exp Data")
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logging.info('Trying: POST: Interview Exp Data')

        user=User.objects.get(rollNumber=request.user)
        serializer = UserSerializer(user)
        name=serializer.data.get('rollNumber')+"_"+serializer.data.get('username')
        request.data['name']=name

        file_serializer = interviewSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            logging.info("Successful: POST: Interview Exp Data, status %s" % status.HTTP_201_CREATED)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.warning("Bad Request: POST: Interview Exp Data, status %s" % status.HTTP_400_BAD_REQUEST)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class interviewDataId(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, id):
        logging.info('Trying: GET: Interview Exp by id %s' % id)
        try:
            return Interview.objects.get(id=id)
        except Interview.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user=User.objects.get(rollNumber=request.user)
        user_serializer = UserSerializer(user)

        role=user_serializer.data.get('role')

        product = self.get_object(id)
        serializer = interviewSerializer(product)
        verified=serializer.data.get('verified')
        # not returning anything if the page is not verified and user is a student
        if ((role == 'Student') and (verified == False)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        logging.info('Successful: GET: Interview Exp by id %s' % id)
        return Response(serializer.data)

    def patch(self, request, id):
        logging.info('Trying: PATCH: Interview Exp by id %s' % id)
        File = self.get_object(id)
        serializer = interviewSerializer(File, data=request.data,
                                         partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            logging.info('Successful: PATCH: Interview Exp by id %s, status %s' % (id,status.HTTP_201_CREATED))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id, format=None):
        logging.info('Trying: DELETE: Interview Exp by id %s' % id)
        Interview = self.get_object(id)
        Interview.delete()
        logging.info('Successful: DELETE: Interview Exp by id %s, status %s' % (id,status.HTTP_204_NO_CONTENT))
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
FOR ADMIN VIEWS
"""
@api_view(['GET'])
def interviewAdminView(request):
        user=User.objects.get(rollNumber=request.user)
        user_serializer = UserSerializer(user)

        role=user_serializer.data.get('role')
        if (role=='admin'):
            product1 = Interview.objects.filter(verified=False)
            serializer = interviewSerializer(product1, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def pyqAdminView(request):
        user=User.objects.get(rollNumber=request.user)
        user_serializer = UserSerializer(user)

        role=user_serializer.data.get('role')
        if (role=='admin'):
            product1 = File.objects.filter(verified=False)
            serializer = FileSerializer(product1, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

"""
END ADMIN VIEWS
"""

class getData(APIView):

    def get(self, request, *args, **kwargs):
        allFiles = File.objects.all()
        for key in request.data.keys():
            value = request.data.get(key)
            

from .models import File
from .serializers import serializers

from .serializers import FileSerializer

class getData(APIView):

    def get(self, request, *args, **kwargs):
        logging.info('Trying: GET: PYQ Data')
        allFiles = File.objects.filter(verified=True)

        for key in request.GET.keys():
            value = request.GET.get(key)
            if (key == 'resourceType'):
                allFiles = allFiles.filter(resourceType=value)
            elif (key == 'semester'):
                allFiles = allFiles.filter(semester=value)
            elif (key == 'subject'):
                allFiles = allFiles.filter(subject=value)
            elif (key == 'year'):
                allFiles = allFiles.filter(year=value)
            elif (key == 'id'):
                allFiles = allFiles.filter(id=value)
        
        serializer = FileSerializer(allFiles, many=True)
        logging.info('Successful: GET: PYQ Data')
        return Response(serializer.data)

class patchData(APIView):
    def get_object(self, id):
        logging.info('Trying: GET: PYQ by id %s' % id)
        try:
            return File.objects.get(id=id)
        except File.DoesNotExist:
            raise Http404

    def patch(self, request, id):
        logging.info('Trying: PATCH: PYQ by id %s' % id)
        File = self.get_object(id)
        serializer = FileSerializer(File, data=request.data,
                                         partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            logging.info('Successful: PATCH: PYQ by id %s, status %s' % (id,status.HTTP_201_CREATED))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    def get(self, request, id, format=None):
        user=User.objects.get(rollNumber=request.user)
        user_serializer = UserSerializer(user)

        role=user_serializer.data.get('role')

        File = self.get_object(id)
        serializer = FileSerializer(File)
        verified=serializer.data.get('verified')
        # not returning anything if the page is not verified and user is a student
        if ((role == 'Student') and (verified == False)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        logging.info('Successful: GET: PYQ by id %s' % id)
        return Response(serializer.data)

class postData(APIView):
    def post(self, request, *args, **kwargs):        
        logging.info('Trying: POST: PYQ')
        user=User.objects.get(rollNumber=request.user)
        serializer = UserSerializer(user)
        name=serializer.data.get('rollNumber')+"_"+serializer.data.get('username')
        request.data['author']=name

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            logging.info('Successful: POST: PYQ, status %s' % status.HTTP_201_CREATED)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.warning('Bad Request: POST: PYQ, status %s' % status.HTTP_400_BAD_REQUEST)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteData(APIView):
    def get_object(self, id):
        logging.info('Trying: GET: PYQ by id %s' % id)
        try:
            return File.objects.get(id=id)
        except File.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        logging.info('Trying: DELETE: PYQ by id %s' % id)
        File = self.get_object(id)
        File.delete()
        logging.info('Successful: DELETE: PYQ by id %s, status %s' % (id,status.HTTP_204_NO_CONTENT))
        return Response(status=status.HTTP_204_NO_CONTENT)

class getPostCommentsPYQ(APIView):
    def get(self, request, id):
        logging.info('Trying: GET: Comments for PYQ by id %s' % id)
        allComments = CommentsPYQ.objects.all().filter(pyq=id)

        commentsPYQSerializer = CommentsPYQSerializer(allComments, many=True)
        logging.info('Successful: GET: Comments for PYQ by id %s' % id)
        return Response(commentsPYQSerializer.data)

    def post(self, request, id):
        logging.info('Trying: POST: Comments for PYQ by id %s' % id)
        user=User.objects.get(rollNumber=request.user)
        serializer = UserSerializer(user)
        name=serializer.data.get('rollNumber')+"_"+serializer.data.get('username')
        request.data['author']=name
        
        commentsPYQSerializer = CommentsPYQSerializer(data=request.data)
        
        if commentsPYQSerializer.is_valid():
            commentsPYQSerializer.save()
            logging.info('Successful: POST: Comments for PYQ by id %s, status %s' % (id,status.HTTP_201_CREATED))
            return Response(commentsPYQSerializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.warning('Bad Request: POST: Comments for PYQ by id %s, status %s' % (id,status.HTTP_400_BAD_REQUEST))
            return Response(commentsPYQSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_comment(self, id):
        try:
            return CommentsPYQ.objects.get(id=id)
        except CommentsPYQ.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        CommentsPYQ = self.get_comment(id)
        CommentsPYQ.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class getPostCommentsExp(APIView):
    def get(self, request, id):
        logging.info('Trying: GET: Comments for Interview Exp by id %s' % id)
        allComments = CommentsExp.objects.all().filter(exp=id)

        commentsExpSerializer = CommentsExpSerializer(allComments, many=True)
        logging.info('Successful: GET: Comments for Interview Exp by id %s' % id)
        return Response(commentsExpSerializer.data)

    def post(self, request, id):
        logging.info('Trying: POST: Comments for Interview Exp by id %s' % id)
        user=User.objects.get(rollNumber=request.user)
        serializer = UserSerializer(user)
        name=serializer.data.get('rollNumber')+"_"+serializer.data.get('username')
        request.data['author']=name

        commentsExpSerializer = CommentsExpSerializer(data=request.data)
        
        if commentsExpSerializer.is_valid():
            commentsExpSerializer.save()
            logging.info('Successful: POST: Comments for Interview Exp by id %s, status %s' % (id,status.HTTP_201_CREATED))
            return Response(commentsExpSerializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.warning('Bad Request: POST: Comments for Interview Exp by id %s, status %s' % (id,status.HTTP_400_BAD_REQUEST))
            return Response(commentsExpSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_comment(self, id):
        try:
            return CommentsExp.objects.get(id=id)
        except CommentsExp.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        CommentsExp = self.get_comment(id)
        CommentsExp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
