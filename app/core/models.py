from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import os
import joblib
import pandas as pd
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
import numpy as np

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
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'electrical_cost_esti_model.pkl')
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
    

class PaintingService(models.Model):
    PAINTING_TYPE = [
        ('BASIC','Basic'),
        ('COLORED','Colored'),
        ('DECORATIVE','Decorative')
    ]
    wallSurface = models.FloatField()    
    paintingType = models.CharField(
        max_length = 100,
        choices = PAINTING_TYPE,
        default = 'BASIC'
    )
    coats = models.IntegerField()
    IswallScrapping = models.BooleanField()
    IsPlastering = models.BooleanField()
    cost = models.FloatField()

    def save(self, *args, **kwargs):
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'painting_cost_model.pkl')
        model = joblib.load(model_path)

        # One-hot encode paintingType
        painting_type = self.paintingType
        painting_type_COLORED = 1 if painting_type == 'COLORED' else 0
        painting_type_DECORATIVE = 1 if painting_type == 'DECORATIVE' else 0

        input_data = [[
            self.wallSurface,
            self.coats,
            int(self.IswallScrapping),
            int(self.IsPlastering),
            painting_type_COLORED,
            painting_type_DECORATIVE
        ]]

        self.cost = model.predict(input_data)[0]
        super().save(*args, **kwargs)


class FlooringService(models.Model):
    FLOORTYPE = [
        ('CARRELAGE','Carrelage'),
        ('PARQUETBOIS','ParquetBois'),
        ('VINYLEPVC','VinylePVC'),
        ('MOQUETTE','Moquette')
    ]
    surface = models.FloatField() 
    floorType = models.CharField(
        max_length=100,
        choices=FLOORTYPE,
        default='CARRELAGE'
    )  
    quality = models.CharField(
        max_length=100,
        choices=QUALITY_CHOICES,
        default='POOR'
    )     
    cost = models.FloatField(editable=False)

    def save(self, *args, **kwargs):
        # Load model and encoders
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'flooring', 'flooring_cost_model.pkl')
        floor_encoder_path = os.path.join(settings.BASE_DIR, 'ml_models', 'flooring', 'floorType_encoder.pkl')
        quality_encoder_path = os.path.join(settings.BASE_DIR, 'ml_models', 'flooring', 'quality_encoder.pkl')

        model = joblib.load(model_path)
        le_floor = joblib.load(floor_encoder_path)
        le_quality = joblib.load(quality_encoder_path)

        # Encode inputs
        floor_type_encoded = le_floor.transform([self.floorType])[0]
        quality_encoded = le_quality.transform([self.quality])[0]

        input_data = [[self.surface, floor_type_encoded, quality_encoded]]

        # Predict cost
        self.cost = model.predict(input_data)[0]

        super().save(*args, **kwargs)