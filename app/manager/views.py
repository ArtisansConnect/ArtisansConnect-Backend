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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# The Manager can Access their Planification created by Manager
class PlanificationListViewManager(APIView):
    serializer_class = PlanificationListSerializer

    def get(self,request):
        instance = Planification.objects.all()
        serializer = PlanificationListSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)       


# The manager can refuse the project request
class RefuseProject(APIView):
    serializer_class = UpdateProjectStatusSerializer
    # permission_classes = [IsManager]

    def put(self, request,pk=None):
        try:
            instance = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        serializer = UpdateProjectStatusSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# The Manager could see all the client projects
class ManagerListProject(APIView):
    serializer_class = ProjectPlanificationSerializer
    # permission_classes = [IsManager]

    def get(self,request):
        instance = Project.objects.all()
        serializer = ProjectPlanificationSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)