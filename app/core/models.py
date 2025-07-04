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
from sklearn.preprocessing import OneHotEncoder

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_TYPE = [
        ('Client','Client'),
        ('Artisan','Artisan'),
        ('Manager','Manager'),
        ('Admin','Admin')
    ]
    ARTISAN_ROLE_TYPE = [
        ('Construction','Construction'),
        ('Electricity','Electricity'),
        ('Painting','Painting'),
        ('Flooring','Flooring'),
        ('Hvac','Hvac'),
        ('Plumbing','Plumbing'),
        ('Carpentary','Carpentary'),
        ('Roofing','Roofing'),
        ('Facade','Facade'),
    ]
    LOCATION = [
        ('Constantine','Constantine'),
        ('Algier','Algier'),
        ('Annaba','Annaba'),
        ('Jijel','Jijel'),
        ('Setif','Setif')
    ]
    email = models.EmailField(_("email address"), unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phoneNumber = models.IntegerField()
    role = models.CharField(
        max_length=100,
        choices= ROLE_TYPE,
        default= 'Client'
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='profile_images/',blank=True,null=True)
    location = models.CharField(
        max_length=100,
        choices=LOCATION,
        default='Constantine',
        null=True
    )
    # Artisan Options
    roleArtisan = models.CharField(
        max_length=100,
        null=True,
        choices= ARTISAN_ROLE_TYPE
    )
    diplomDocument = models.FileField(upload_to='artisan_documents/',null=True)
    rating = models.FloatField(default=5.0,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['firstName','lastName','phoneNumber','role']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
QUALITY_CHOICES = [
        ('POOR','Poor'),
        ('NORMAL','Normal'),
        ('HIGH','High'),
    ]

STATUS_CHOICES = [
    ('Selected','Selected'),
    ('NonSelected','NonSelected')
]

class ProgressChoices(models.IntegerChoices):
    NOT_STARTED = 0, '0%'
    TEN = 10, '10%'
    TWENTY = 20, '20%'
    THIRTY = 30, '30%'
    FORTY = 40, '40%'
    FIFTY = 50, '50%'
    SIXTY = 60, '60%'
    SEVENTY = 70, '70%'
    EIGHTY = 80, '80%'
    NINETY = 90, '90%'
    HUNDRED = 100, '100%'


class ElectricalService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='electrical_services_requested')  

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
    time = models.FloatField(null=True, editable=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True,
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Electricity'},
                                related_name='electrical_services_assigned')


    def save(self, *args, **kwargs):
        self.cableLength = self.calculate_cable_length()
        # Predict cost before saving
        self.cost, self.time = self.predict_cost_and_time()
        super().save(*args, **kwargs)

    def calculate_cable_length(self):
        return round((self.rooms * 10), 2)    

    def predict_cost_and_time(self):
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'electrical_model.pkl')
        model = joblib.load(model_path)

        # Prepare the input
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
        predictions = model.predict(df)[0]  # returns [cost, time]
        return round(predictions[0], 0), round(predictions[1], 0)


    def _encode_quality(self, value):
        encoding = {'POOR': 0, 'NORMAL': 1, 'HIGH': 2}
        return encoding.get(value.upper(), 1)

    def _encode_panel(self, value):
        encoding = {'SMALL': 0, 'MEDUIM': 1, 'BIG': 2}
        return encoding.get(value.upper(), 1)
    

class PaintingService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES,
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='painting_services_requested')  
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
    time = models.FloatField(null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Painting'},
                                related_name='painting_services_assigned')


    def save(self, *args, **kwargs):
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'painting_model.pkl')
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

        prediction = model.predict(input_data)[0]  # [cost, time]
        self.cost = round(prediction[0], 0)
        self.time = prediction[1]
        super().save(*args, **kwargs)


class FlooringService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='flooring_services_requested')

    FLOORTYPE = [
        ('CARRELAGE', 'Carrelage'),
        ('PARQUETBOIS', 'ParquetBois'),
        ('VINYLEPVC', 'VinylePVC'),
        ('MOQUETTE', 'Moquette')
    ]

    surface = models.FloatField()
    floorType = models.CharField(max_length=100, choices=FLOORTYPE, default='CARRELAGE')
    quality = models.CharField(max_length=100, choices=QUALITY_CHOICES, default='POOR')
    
    cost = models.FloatField(editable=False)
    time = models.FloatField(editable=False,null=True,blank=True)  # in hours
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Flooring'},
                                related_name='flooring_services_assigned')


    def save(self, *args, **kwargs):
        # Load the trained model
        model_path = os.path.join(settings.BASE_DIR, 'ml_models' ,'flooring_cost_time_model.pkl')
        model = joblib.load(model_path)

        # Prepare input as DataFrame
        input_data = pd.DataFrame([{
            'surface': self.surface,
            'floorType': self.floorType,
            'quality': self.quality
        }])

        # Predict cost and time
        prediction = model.predict(input_data)[0]
        self.cost = round(prediction[0], 2)
        self.time = round(prediction[1], 2)

        super().save(*args, **kwargs)


class HvacService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='hvac_services_requested')        
    smallHvac = models.IntegerField()
    mediumHvac = models.IntegerField()
    bigHvac = models.IntegerField()
    cost = models.FloatField(editable=False)
    time = models.FloatField(editable=False,null=True,blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Hvac'},
                                related_name='hvac_services_assigned')


    def save(self, *args, **kwargs):
        # Load the model only when saving
        model_path = os.path.join(settings.BASE_DIR, 'ml_models/hvac_model.pkl')
        model = joblib.load(model_path)

        # Prepare input as [small, medium, big]
        input_data = [[self.smallHvac, self.mediumHvac, self.bigHvac]]
        predicted = model.predict(input_data)[0]  # [cost, time]

        # Assign predictions
        self.cost = round(predicted[0], 0)
        self.time = round(predicted[1], 0)

        super().save(*args, **kwargs)

class PlumbingService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    SIZE_CATEGORIE = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('big', 'Big')
    ]
    RADIATOR_TYPE = [
        ('COPA_Aluminium', 'COPA Aluminium'),
        ('GLOBAL_ISEO_350', 'GLOBAL ISEO 350'),
        ('FONDITAL_ARDENTE_C2', 'FONDITAL ARDENTE C2'),
        ('Samochauf_SAHD', 'Samochauf SAHD'),
        ('Sira_Alice_Royal', 'Sira Alice Royal'),
        ('Helyos_Evo', 'Helyos Evo'),
        ('Primavera_H500', 'Primavera H500')
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='plumbing_services_requested') 

    # Central elements       
    boilerSize = models.CharField(
        max_length=100,
        choices=SIZE_CATEGORIE,
        default='medium'
    )
    radiatorType = models.CharField(
        max_length=100,
        choices= RADIATOR_TYPE,
        default= 'COPA_Aluminium'
    )
    radiator = models.IntegerField()

    # Sanitary elements inputs
    TOILET_CATEGORIES = [
        ('Basic-Ceramic','Basic Ceramic'),
        ('One-Piece','One-Piece'),
        ('Wall-Hung','Wall-Hung')
    ]     
    
    toilet = models.IntegerField()
    toileType = models.CharField(
        max_length=100,
        choices=TOILET_CATEGORIES,
        default='One-Piece'
    )
    
    # lavabo
    WASHBASIN_CATEGORIES = [
        ('Pedestal','Pedestal'),
        ('Wall-Mounted','Wall-Mounted'),
        ('Countertop','Countertop')
    ]
    washbasin = models.IntegerField()
    washbasinType = models.CharField(
        max_length=100,
        choices=WASHBASIN_CATEGORIES,
        default='Pedestal'
    )
    
    # baignoire
    Bathtub_CATEGORIES = [
        ('Standard','Standard'),
        ('Luxury','Luxury')
    ]
    bathhub = models.IntegerField()
    bathhubType = models.CharField(
        max_length=100,
        choices=Bathtub_CATEGORIES,
        default='Standard'
    )

    SHOWER_CABIN_CATEGORIES = [
    ('Basic_Enclosure', 'Basic Enclosure'),
    ('Luxury_Enclosure', 'Luxury Enclosure')
    ]

    # cabine de douche
    showerCabin = models.IntegerField()
    showerCabinType = models.CharField(
    max_length=100,
    choices=SHOWER_CABIN_CATEGORIES,
    default='Basic_Enclosure'
    )
    
    #Bidet lavabo
    BIDET_CATEGORIES = [
        ('Bidet-Ceramic','Bidet-Ceramic'),
        ('Bidet-Mixer-Tap','Bidet-Mixer-Tap'),
        ('Wall-Hung','Wall-Hung')
    ]
    Bidet = models.IntegerField()
    BidetType = models.CharField(
        max_length=100,
        choices=BIDET_CATEGORIES,
        default='Bidet-Ceramic'
    )
    
    # chauffe-eau
    WaterHeater_CATEGORIES = [
        ('Electric-30liters','Electric-30liters'),
        ('Electric-50liters','Electric-50liters'),
        ('GAS-6liters','GAS-6liters'),
        ('GAS-11liters','GAS-11liters')
    ]
    waterHeater = models.IntegerField()
    waterHeaterType = models.CharField(
        max_length=100,
        choices=WaterHeater_CATEGORIES,
        default='GAS-6liters'
    )

    # Kitchen Elements
    QualityChoices = [
        ('poor','poor'),
        ('high','high')
    ]
    CategorieSink_Choices = [
        ('single','single'),
        ('double','double')
    ]
    sinkTypeQuality = models.CharField(
        max_length=100,
        choices=QUALITY_CHOICES,
        default='poor'
    )
    sinkCategorie = models.CharField(
        max_length=100,
        choices=CategorieSink_Choices,
        default='single'
    )

    cost = models.FloatField()
    time = models.FloatField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Plumbing'},
                                related_name='plumbing_services_assigned')


    def load_model(self):
        """Load the trained RandomForest model using joblib"""
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'plumbing_service_model.pkl')
        return joblib.load(model_path)  # Loading the .pkl model

    def save(self, *args, **kwargs):
        """Override the save method to predict cost and time"""
        # Extract the features from the model fields
        features = {
        'boilerSize': self.boilerSize,
        'radiatorType': self.radiatorType,
        'radiator': self.radiator,
        'toilet': self.toilet,
        'toileType': self.toileType,
        'washbasin': self.washbasin,
        'washbasinType': self.washbasinType,
        'bathhub': self.bathhub,
        'bathhubType': self.bathhubType,
        'showerCabin': self.showerCabin,
        'showerCabinType': self.showerCabinType,
        'Bidet': self.Bidet,
        'BidetType': self.BidetType,
        'waterHeater': self.waterHeater,
        'waterHeaterType': self.waterHeaterType,
        'sinkTypeQuality': self.sinkTypeQuality,
        'sinkCategorie': self.sinkCategorie
    }

        # Convert features to a DataFrame and one-hot encode
        features_df = pd.DataFrame([features])
        features_encoded = pd.get_dummies(features_df)

        # Load the model
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'plumbing_service_model.pkl')
        model = joblib.load(model_path)

        # Load the training feature names
        features_path = os.path.join(settings.BASE_DIR, 'ml_models', 'plumbing_service_features.pkl')
        feature_names = joblib.load(features_path)

        # Make sure features match the training features
        for col in feature_names:
            if col not in features_encoded.columns:
                features_encoded[col] = 0  # add missing column with zeros

        features_encoded = features_encoded[feature_names]  # ensure correct column order

        # Predict
        prediction = model.predict(features_encoded)

        # Set the predicted cost and time
        self.cost = prediction[0][0]
        self.time = prediction[0][1]

        # Call the original save method
        super().save(*args, **kwargs)

# windows doors Service
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Validation for Windows Doors Service

def validate_window(value):
    if not (0 <= value <= 30):
        raise ValidationError(
            _("%(value)s is not a value between 0 and 30"),
            params={"value": value},
        )
    
def validate_door(value):
    if not (0 <= value <= 20):
        raise ValidationError(
            _("%(value)s is not a value between 0 and 20"),
            params={"value": value},
        )    

class WindowsDoorsService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    TYPES_WINDOWS_CHOICES = [
        ('PVC','Pvc'),
        ('Aluminum','Aluminum'),
        ('Wood','wood'),
    ]
    TYPES_DOORS_CHOICES = [
        ('PVC','PVC'),
        ('Aluminum','Aluminum'),
        ('StandardWood','StandardWood'),
        ('HighEndWood','HighEndWood'),
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='carpentary_services_requested')
    windows = models.IntegerField(validators=[validate_window])
    windowsTypes = models.CharField(
        max_length=100,
        choices= TYPES_WINDOWS_CHOICES,
        default='PVC'
    )
    doors = models.IntegerField(validators=[validate_door])
    doorsTypes = models.CharField(
        max_length=100,
        choices= TYPES_DOORS_CHOICES,
        default='pvc'
    )
    time = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Carpentary'},
                                related_name='carpentary_services_assigned')


    def load_model(self):
        """Load the trained RandomForest model using joblib"""
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'windows_doors_estimator_model.pkl')
        return joblib.load(model_path)  # Loading the .pkl model

    def save(self, *args, **kwargs):
        """Override the save method to predict cost and time"""
        # Extract the features from the model fields
        features = {
            'windows': self.windows,
            'windowsTypes_PVC': 1 if self.windowsTypes == 'PVC' else 0,
            'windowsTypes_Aluminum': 1 if self.windowsTypes == 'Aluminum' else 0,
            'windowsTypes_Wood': 1 if self.windowsTypes == 'Wood' else 0,
            'doors': self.doors,
            'doorsTypes_PVC': 1 if self.doorsTypes == 'PVC' else 0,
            'doorsTypes_Aluminum': 1 if self.doorsTypes == 'Aluminum' else 0,
            'doorsTypes_StandardWood': 1 if self.doorsTypes == 'StandardWood' else 0,
            'doorsTypes_HighEndWood': 1 if self.doorsTypes == 'HighEndWood' else 0
        }

        # Convert features to a DataFrame and one-hot encode
        features_df = pd.DataFrame([features])

        # Load the model
        model = self.load_model()

        # Load the training feature names
        features_path = os.path.join(settings.BASE_DIR, 'ml_models', 'model_features_windor.pkl')
        feature_names = joblib.load(features_path)

        # Make sure features match the training features
        for col in feature_names:
            if col not in features_df.columns:
                features_df[col] = 0  # Add missing column with zeros

        features_df = features_df[feature_names]  # Ensure correct column order

        # Predict
        prediction = model.predict(features_df)

        # Set the predicted cost and time
        self.cost = prediction[0][0]
        self.time = prediction[0][1]

        # Call the original save method
        super().save(*args, **kwargs)


# Roofing Service

def validate_roof_surface(value):
    if not (10 <= value <= 200):
        raise ValidationError(
            _("%(value)s is not a value between 10 and 200 m2"),
            params={"value": value},
        )    
    
class RoofingService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    ROOF_TYPES = [
        ('CanalTilesWithInsulation','Canal tiles with insulation'),
        ('CanalTilesWithMortar','Canal tiles with mortar'),
        ('RomanTiles','Roman tiles with waterproofing'),
        ('SlateRoof','Slate roof')
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='roofing_services_requested')
    surface = models.FloatField(validators=[validate_roof_surface])      
    roofType = models.CharField(
        max_length=100,
        choices=ROOF_TYPES,
        default='CanalTilesWithInsulation'
    )   
    time = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Roofing'},
                                related_name='roofing_services_assigned')


    def load_model(self):
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'roofing_models.pkl')
        model = joblib.load(model_path)
        return model

    def save(self,*args,**kwargs):
        # prepare the features
        input_data = pd.DataFrame([{
            'surface':self.surface,
            'roofType':self.roofType
        }])
        # load the trained model
        model = self.load_model()
        time_model = model['time_model']
        cost_model = model['cost_model']
        # predict time and cost
        self.time = round(float(time_model.predict(input_data)[0]),0)
        self.cost = float(cost_model.predict(input_data)[0])
        # save to DB
        super().save(*args,**kwargs)


class ConstructionHouseService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='construction_services_requested')
    wallConstructionSurface = models.FloatField(null=True)
    wallDestructionSurface = models.FloatField(null=True)
    cost = models.FloatField(null=True)
    time = models.FloatField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Construction'},
                                related_name='construction_services_assigned')


    def save(self, *args, **kwargs):
        # Constants
        CONSTRUCTION_COST_PER_M2 = 11567  # DZD
        DESTRUCTION_COST_PER_M2 = 159     # DZD
        CONSTRUCTION_TIME_PER_M2 = 1      # hours
        DESTRUCTION_TIME_PER_M2 = 0.2     # hours

        # Calculate total cost
        self.cost = (
            self.wallConstructionSurface * CONSTRUCTION_COST_PER_M2 +
            self.wallDestructionSurface * DESTRUCTION_COST_PER_M2
        )

        # Calculate total time
        self.time = (
            self.wallConstructionSurface * CONSTRUCTION_TIME_PER_M2 +
            self.wallDestructionSurface * DESTRUCTION_TIME_PER_M2
        )

        super().save(*args, **kwargs)


class FacadeService(models.Model):
    status = models.CharField(
        max_length=100,
        default='NonSelected',
        choices=STATUS_CHOICES
    )
    rank = models.PositiveIntegerField(default=0,null=True)
    LAYER_TYPE = [
        ('Enduit Monocouche', 'Enduit Monocouche'),
        ('Acrylic Mortar Coating', 'Acrylic Mortar Coating'),
        ('Lime Plaster', 'Lime Plaster'),
        ('Ventilated Facade(Porcelain)', 'Ventilated Facade(Porcelain)'),
        ('Ventilated Facade(Terracotta)', 'Ventilated Facade(Terracotta)'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='facade_services_requested')
    surface = models.FloatField()
    finishing_layer = models.CharField(
        max_length=100,
        choices=LAYER_TYPE,
        default='Enduit Monocouche'
    )
    ITE = models.BooleanField(default=False)
    Hydrofuge = models.BooleanField(default=False)
    cost = models.FloatField(blank=True, null=True)
    time = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    progress = models.IntegerField(
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
        null=True
    )
    artisan = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                null=True, blank=True, 
                                limit_choices_to={'role': 'Artisan', 'roleArtisan': 'Facade'},
                                related_name='facade_services_assigned')

    def save(self, *args, **kwargs):
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'facade_model.pkl')
            model = joblib.load(model_path)

            features = pd.DataFrame([{
                'surface': self.surface,
                'finishing_layer': self.finishing_layer,
                'ITE': int(self.ITE),  # convert boolean to int if necessary
                'Hydrofuge': int(self.Hydrofuge)
            }])

            prediction = model.predict(features)[0]
            self.cost = round(prediction[0], 0)
            self.time = round(prediction[1], 2)
        except Exception as e:
            # Log or handle error gracefully
            print(f"Model prediction failed: {e}")
            self.cost = None
            self.time = None

        super().save(*args, **kwargs)


class Project(models.Model):
    STATUS_TYPE = [
        ('PENDING','PENDING'),
        ('REJECTED','REJECTED'),
        ('ACCEPTED','ACCEPTED')
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    construction = models.ForeignKey(ConstructionHouseService,on_delete=models.CASCADE,blank=True,null=True)
    electrical = models.ForeignKey(ElectricalService,on_delete=models.CASCADE,blank=True,null=True)
    plumbing = models.ForeignKey(PlumbingService,on_delete=models.CASCADE,blank=True,null=True)
    hvac = models.ForeignKey(HvacService,on_delete=models.CASCADE,blank=True,null=True)
    painting = models.ForeignKey(PaintingService,on_delete=models.CASCADE,blank=True,null=True)
    flooring = models.ForeignKey(FlooringService,on_delete=models.CASCADE,blank=True,null=True)
    carpentary = models.ForeignKey(WindowsDoorsService,on_delete=models.CASCADE,blank=True,null=True)
    roofing = models.ForeignKey(RoofingService,on_delete=models.CASCADE,blank=True,null=True)
    facade = models.ForeignKey(FacadeService,on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(max_length=100,choices=STATUS_TYPE,default='PENDING')
    creation_date = models.DateField(null=True,auto_now_add=True,editable=False)

    def __str__(self):
        return f'{self.id} - {self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the project first

        gantt_rank_groups = [
            ['construction'],                      # Rank 1
            ['electrical', 'plumbing', 'hvac'],    # Rank 2
            ['painting'],                          # Rank 3
            ['flooring'],                          # Rank 4
            ['carpentary', 'facade', 'roofing'],   # Rank 5
        ]

        current_rank = 1
        for group in gantt_rank_groups:
            group_has_selected = any(getattr(self, service) is not None for service in group)
            if group_has_selected:
                for service in group:
                    service_instance = getattr(self, service)
                    if service_instance:
                        service_instance.status = 'Selected'
                        service_instance.rank = current_rank
                        service_instance.save()
                current_rank += 1  # Only increment if at least one service in the group was filled


from datetime import timedelta, datetime, time

WORK_START = time(8, 0)
LUNCH_START = time(12, 0)
LUNCH_END = time(13, 0)
WORK_END = time(17, 0)
HOURS_PER_DAY = 8

def add_working_hours(start_datetime, hours):
    current = start_datetime
    remaining_hours = hours

    while remaining_hours > 0:
        # Move to next working time if current is outside working hours
        if current.time() < WORK_START:
            current = current.replace(hour=8, minute=0)
        elif LUNCH_START <= current.time() < LUNCH_END:
            current = current.replace(hour=13, minute=0)
        elif current.time() >= WORK_END:
            current = (current + timedelta(days=1)).replace(hour=8, minute=0)

        # 🟡 Skip weekends
        while current.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            current += timedelta(days=1)
            current = current.replace(hour=8, minute=0)    

        # Determine available working time for the current slot
        if current.time() < LUNCH_START:
            available_until = current.replace(hour=12, minute=0)
        elif current.time() < WORK_END:
            available_until = current.replace(hour=17, minute=0)
        else:
            # Should not reach here
            continue

        delta = (available_until - current).total_seconds() / 3600.0
        working_hours = min(remaining_hours, delta)

        current += timedelta(hours=working_hours)
        remaining_hours -= working_hours

    return current

class Planification(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

    def save(self, *args, **kwargs):
        if self.start_date:
            self.start_date = self.start_date.replace(hour=8,minute=0,second=0,microsecond=0)
        if self.project:
            self.user = self.project.user
        service_fields = [
            'construction', 'electrical', 'plumbing', 'hvac',
            'painting', 'flooring', 'carpentary', 'roofing', 'facade'
        ]
        services = {
            name: getattr(self.project, name)
            for name in service_fields
            if getattr(self.project, name) is not None
        }

        # Group services by rank
        services_by_rank = {}
        for service in services.values():
            if service.rank not in services_by_rank:
                services_by_rank[service.rank] = []
            services_by_rank[service.rank].append(service)

        current_start = self.start_date
        max_rank = max(services_by_rank.keys())

        for rank in range(1, max_rank + 1):
            if rank not in services_by_rank:
                continue

            services_in_rank = services_by_rank[rank]
            max_end = current_start

            for service in services_in_rank:
                hours_needed = service.time or 0
                service.start_date = current_start
                service.end_date = add_working_hours(current_start, hours_needed)
                service.save()

                if service.end_date > max_end:
                    max_end = service.end_date

            current_start = max_end

        self.end_date = current_start

        if self.project.status == 'PENDING':
            self.project.status = 'ACCEPTED'
            self.project.save()
            
        super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,max_length=255,null=True)
    room_name = models.CharField(max_length=255,null=True)
    receiver = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.message}"

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return {self.name}

class Blog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)      
    tags = models.ManyToManyField(Tags)  
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()