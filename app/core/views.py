# views.py
from rest_framework import viewsets,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (ElectricalService,
                     PaintingService,
                     FlooringService,
                     HvacService,
                     PlumbingService,
                     WindowsDoorsService,
                     RoofingService,
                     ConstructionHouseService,
                     FacadeService,
                     Project,
                     Planification)
from .serializers import (ElectricalServiceSerializer,
                          PaintingServiceSerializer,
                          FlooringServiceSerializer,
                          HvacServiceSerializer,
                          PlumbingServiceSerializer,
                          WindowsDoorsServiceSerializer,
                          RoofingServiceSerializer,
                          ConstructionHouseSerializer,
                          FacadeServiceSerializer,
                          ProjectSerializer,
                          ProjectListSerializer,
                          PlanificationSerializer,
                          PlanificationListSerializer,
                          UpdateProjectStatusSerializer,
                          ProjectPlanificationSerializer)

from .permissions import (
    IsAdmin,
    IsArtisan,
    IsClient,
    IsManager
)

class ElectricalServiceViewSet(viewsets.ModelViewSet):
    queryset = ElectricalService.objects.all()
    serializer_class = ElectricalServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ElectricalService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaintingServiceViewSet(viewsets.ModelViewSet):
    queryset = PaintingService.objects.all()
    serializer_class = PaintingServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaintingService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FlooringServiceViewSet(viewsets.ModelViewSet):
    queryset = FlooringService.objects.all()    
    serializer_class = FlooringServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FlooringService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HvacServiceViewSet(viewsets.ModelViewSet):
    queryset = HvacService.objects.all()
    serializer_class = HvacServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HvacService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class PlumbingServiceViewSet(viewsets.ModelViewSet):
    queryset = PlumbingService.objects.all()
    serializer_class = PlumbingServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PlumbingService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)          


class WindowsDoorsServiceViewSet(viewsets.ModelViewSet):
    queryset = WindowsDoorsService.objects.all()
    serializer_class = WindowsDoorsServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WindowsDoorsService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class RoofingServiceViewSet(viewsets.ModelViewSet):
    queryset = RoofingService.objects.all()
    serializer_class = RoofingServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoofingService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)        

class ConstructionHouseServiceViewSet(viewsets.ModelViewSet):
    queryset = ConstructionHouseService.objects.all()
    serializer_class = ConstructionHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ConstructionHouseService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)      

class FacadeServiceViewSet(viewsets.ModelViewSet):
    queryset = FacadeService.objects.all()
    serializer_class = FacadeServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FacadeService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)                                             

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 


class ProjectListView(APIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        instance = Project.objects.filter(user=request.user)
        serializer = ProjectListSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

# The Client can Access their Planification created by Manager
class PlanificationListView(APIView):
    serializer_class = PlanificationListSerializer
    permission_classes = [IsClient]

    def get(self,request):
        instance = Planification.objects.filter(user=request.user)
        serializer = PlanificationListSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)   
    
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
    