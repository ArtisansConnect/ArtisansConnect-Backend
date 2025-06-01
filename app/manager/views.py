from rest_framework.views import APIView
from core.serializers import (
    PlanificationSerializer,
    PlanificationListSerializer,
    UpdateProjectStatusSerializer,
    ProjectPlanificationSerializer,
)
from .serializers import (
    TagSerializer,
    BlogSerializer,
    AcceptRecrutementSerializer
)
from core.models import (
    Planification,
    Project,
    Tags,
    Blog,
    CustomUser
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from core.permissions import (IsManager)

# The Manager can create a new planification
class PlanificationView(APIView): 
    serializer_class = PlanificationSerializer

    def post(self,request):
        serializer = PlanificationSerializer(data=request.data)
        if serializer.is_valid():
            planification = serializer.save()
            project = planification.project
            if project.status == 'PENDING':
                project.status = 'ACCEPTED'
                project.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# The Manager can Access their Planification created by Manager
class PlanificationListViewManager(APIView):
    serializer_class = PlanificationListSerializer

    def get(self,request,pk=None):
        if pk:
            try:
                instance = Planification.objects.get(pk=pk)
                serializer = PlanificationListSerializer(instance,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Planification.DoesNotExist:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)  
        instance = Planification.objects.all()
        serializer = PlanificationListSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)       


# The manager can refuse the project request
class RefuseProject(APIView):
    serializer_class = UpdateProjectStatusSerializer
    # permission_classes = [IsManager]

    def patch(self, request, pk=None):
        try:
            instance = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        # Set status directly before saving
        serializer = UpdateProjectStatusSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if instance.status == 'ACCEPTED':
                return Response({"detail": "Accepted projects cannot be rejected."}, status=status.HTTP_400_BAD_REQUEST)

            instance.status = 'REJECTED'
            instance.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# The Manager could see all the client projects
class ManagerListProject(APIView):
    serializer_class = ProjectPlanificationSerializer
    # permission_classes = [IsManager]

    def get(self,request,pk=None):
        if pk:
            try:
                instance = Project.objects.get(pk=pk)
                serializer = ProjectPlanificationSerializer(instance) 
                return  Response(serializer.data,status=status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response({'detail':'Project not found'},status=status.HTTP_404_NOT_FOUND)
        instance = Project.objects.all()
        serializer = ProjectPlanificationSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

# The manager can create new tags for its blog
class TagView(APIView):
    serializer_class = TagSerializer
    permission_classes = [IsManager]    

    def get(self,request):
        instance = Tags.objects.all()
        serializer = TagSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# The manager can create a new blog 
class BlogView(APIView):
    serializer_class = BlogSerializer
    permission_classes = [IsManager]    

    def get(self,request):
        instance = Blog.objects.all()
        serializer = BlogSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    
# The manager can list a new blog 
class BlogListView(APIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]    

    def get(self,request):
        instance = Blog.objects.all()
        serializer = BlogSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)    
    

# Artisan Side
# The manager can accept the recrutement or reject it by updating is_active profile    
class AcceptRecrutement(APIView):
    serializer_class = AcceptRecrutementSerializer
    permission_classes = [IsManager]

    def patch(self,request,pk=None):
        try:
            user = get_object_or_404(CustomUser,pk=pk,role='Artisan')
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = AcceptRecrutementSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class RejectRecrutement(APIView):    
    permission_classes = [IsManager]  

    def delete(self, request, pk=None):
        # Find the artisan by ID and role
        artisan = get_object_or_404(CustomUser, pk=pk, role='Artisan')
        
        artisan.delete()
        return Response({"detail": "Recruitment rejected and user deleted."}, status=status.HTTP_204_NO_CONTENT)