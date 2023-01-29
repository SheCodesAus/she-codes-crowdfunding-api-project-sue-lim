from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .filters import DynamicSearchFilter
from .models import Project, Pledge, Comment, Category
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import ProjectSerializer
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CommentSerializer, CategorySerializer, CategoryDetailSerializer
from rest_framework.settings import api_settings


class ProjectList(APIView):
    # permission class to the project list so only logged in users can create new projects
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(instance=project,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        
    def delete(self, request, id=None):
        project = self.get_object(id=id)
        serializer = ProjectDetailSerializer(project)
        project.delete()
        return Response(ProjectDetailSerializer.data, status=status.HTTP_204_NO_CONTENT)
    
    

'''PROJECT LIST VIEW FOR PROJECTS & IF LOGGED IN YOU CAN DELETE PROJECTS'''
class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, id=None):
        project = self.get_object(id=id)
        # serializer = ProjectDetailSerializer(project)
        project.delete()
        return Response(ProjectDetailSerializer.data, status=status.HTTP_204_NO_CONTENT)
    

class PledgeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['supporter', 'project', 'anonymous']
        
    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)
        
    def delete(self, request, id=None):
        pledge = self.get_object(id=id)
        # serializer = ProjectDetailSerializer(project)
        pledge.delete()
        return Response(PledgeSerializer.data, status=status.HTTP_204_NO_CONTENT)


class CommentList(generics.ListAPIView):
    # permission class to the so only logged in users can create comments associated to a project
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'author']

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def delete(self, request, id=None):
        comment = self.get_object(id=id)
        comment.delete()
        return Response(CommentSerializer.data, status=status.HTTP_204_NO_CONTENT)

class CategoryList(generics.ListAPIView):
    """ url: categories/ """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    """ url: categories/<str:name>/"""
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'name'
        
    
'''BELOW TO CULL AS THEY DO NOT SEEM TO SERVE A PURPOSE'''
# class CommentDetail(generics.RetrieveAPIView):
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


    # def get_object(self, pk):
    #     try:
    #         comment = Comment.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, comment)
    #         return comment
    #     except Comment.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     comment = self.get_object(pk)
    #     serializer = CommentSerializer(comment)
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     comment = self.get_object(pk)
    #     data = request.data
    #     serializer = ProjectSerializer(
    #         instance=comment,
    #         data=data,
    #         partial=True
    #     )
    #     if serializer.is_valid():
    #         serializer.save()

# class PledgeDetail(generics.RetrieveAPIView):
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Pledge.objects.all()
#     serializer_class = PledgeSerializer


    
####################################################################################
# PAGEINATOR TO BE IMPLEMENTED
# class ProjectList(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         projects = Project.objects.all()

#         #filter for open projects only
#         is_open = request.query_params.get('is_open', None)
#         if is_open:
#             projects = projects.filter(is_open=is_open)

#         #order by date created
#         order_by = request.query_params.get('order_by', None)
#         if order_by == 'date_created':
#             projects = projects.order_by(order_by)

#         #order by the most recent pledges
#         if order_by == 'recent_pledges':
#             projects = Project.objects.annotate(
#                 pledge_date=Max('pledges_date_created')
#             ).order_by(
#                 '-pledge_date'
#             )

#         #order by the number of pledges
#         if order_by == 'num_pledges':
#             projects = Project.objects.annotate(
#                 pledge_count=Count('pledges')
#             ).order_by(
#                 '-pledge_count'
#             )

#         paginator = LimitOffsetPagination()
#         result_page = paginator.paginate_queryset(projects, request)

#         serializer = ProjectSerializer(result_page, many=True)
#         return Response(serializer.data)

