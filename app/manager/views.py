from rest_framework.views import APIView
from core.serializers import (
    PlanificationSerializer,
    PlanificationListSerializer,
    UpdateProjectStatusSerializer,
    ProjectPlanificationSerializer
)
from core.models import (
    Planification,
    Project
)
from rest_framework.response import Response
from rest_framework import status,permissions

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