from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class BlogPostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            postId = request.data.get('post')
            text = request.data.get('text')
            post = Post.objects.get(id=postId)
            user = User.objects.get(id=request.user.id)
            comment = Comment.objects.create(post=post,user=user,text=text)
            return Response({'success':'comment created successfully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_404_NOT_FOUND)
        
        
       
        