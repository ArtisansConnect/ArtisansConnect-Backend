from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import os
import joblib
import pandas as pd
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phoneNumber = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['firstName','lastName','phoneNumber']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
QUALITY_CHOICES = [
        ('POOR','Poor'),
        ('NORMAL','Normal'),
        ('HIGH','High'),
    ]


class ElectricalService(models.Model):

    PANEL_CHOICES = [
        ('BIG','Big'),
        ('MEDUIM','Meduim'),
        ('SMALL','Small')
    ]
    # WORK COST INFOS

    # General infos
    rooms = models.IntegerField()
    surface = models.FloatField()
    # Light infos
    smallSpotlight = models.IntegerField(default=0)    
    bigSpotlight = models.IntegerField(default=0)   
    spotlightQuality = models.CharField(
        max_length=100,
        choices=QUALITY_CHOICES,
        default='NORMAL'
    )
    chandelier = models.IntegerField(default=0)    
    chandelierQuality = models.CharField(
        max_length=100,
        choices=QUALITY_CHOICES,
        default='NORMAL'
    )
    # Sockets infos
    simpleSocket = models.IntegerField(default=0)
    groundSocket = models.IntegerField(default=0)
    socketQuality = models.CharField(
        max_length=100,
        choices=QUALITY_CHOICES,
        default='NORMAL'
    )
    # Electrical Panel infos (tableaux)
    elecPanel = models.IntegerField(default=0)
    elecPanelQuality = models.CharField(
        max_length=100,
        choices= PANEL_CHOICES,
        default='NORMAL'
    )
    # Switch infos
    simpleSwitch = models.IntegerField(default=0)
    buttonpsSwitch = models.IntegerField(default=0)
    doubleSwitch = models.IntegerField(default=0)
    switchQuality = models.CharField(
        max_length=100,
        choices=QUALITY_CHOICES,
        default='NORMAL'
    )
    # more infos
    cableLength = models.FloatField(editable=False,null=True)
    marqueur = models.BooleanField(default=False)
    cost = models.FloatField()

    def save(self, *args, **kwargs):
        self.cableLength = self.calculate_cable_length()
        # Predict cost before saving
        self.cost = self.predict_cost()
        super().save(*args, **kwargs)

    def calculate_cable_length(self):
        return round((self.surface * 1.5) + (self.rooms * 10), 2)    

    def predict_cost(self):
        # Path to the model file
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'electrical_cost_model.pkl')
        model = joblib.load(model_path)

        # Prepare the input data
        data = {
            'rooms': self.rooms,
            'surface': self.surface,
            'smallSpotlight': self.smallSpotlight,
            'bigSpotlight': self.bigSpotlight,
            'spotlightQuality': self._encode_quality(self.spotlightQuality),
            'chandelier': self.chandelier,
            'chandelierQuality': self._encode_quality(self.chandelierQuality),
            'simpleSocket': self.simpleSocket,
            'groundSocket': self.groundSocket,
            'socketQuality': self._encode_quality(self.socketQuality),
            'elecPanel': self.elecPanel,
            'elecPanelQuality': self._encode_panel(self.elecPanelQuality),
            'simpleSwitch': self.simpleSwitch,
            'buttonpsSwitch': self.buttonpsSwitch,
            'doubleSwitch': self.doubleSwitch,
            'switchQuality': self._encode_quality(self.switchQuality),
            'cableLength': self.cableLength or 0,
            'marqueur': int(self.marqueur),
        }

        df = pd.DataFrame([data])
        predicted_cost = model.predict(df)[0]
        return round(predicted_cost, 2)

    def _encode_quality(self, value):
        encoding = {'POOR': 0, 'NORMAL': 1, 'HIGH': 2}
        return encoding.get(value.upper(), 1)

    def _encode_panel(self, value):
        encoding = {'SMALL': 0, 'MEDUIM': 1, 'BIG': 2}
        return encoding.get(value.upper(), 1)