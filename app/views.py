from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import logging
logger = logging.getLogger(__name__)




# Create your views here.
def home(request):
    return render(request, 'home.html')
@csrf_exempt
def predict(request):
    logger.info('Predict view called')
    if request.method == 'POST':
        logger.info('POST request received')
        item_weight = float(request.POST['item_weight'])
        item_visibility = float(request.POST['item_visibility'])
        item_type = request.POST['item_type']
        item_fat_content = request.POST['item_fat_content']
        item_mrp = float(request.POST['item_mrp'])
        outlet_size = request.POST['outlet_size']
        outlet_location_type = request.POST['outlet_location_type']
        outlet_type = request.POST['outlet_type']
        outlet_estalishment_year = int(request.POST['outlet_establishment_year'])

        todays_date=date.today()

        Outlet_Years=todays_date.year-outlet_estalishment_year

        Item_Visibility_MeanRatio=1.06

        item_fat_content_0=0
        item_fat_content_1=0
        item_fat_content_2=0

        if item_fat_content=="Low Fat":
            item_fat_content_0=1
        elif item_fat_content=="Non-Edible":
            item_fat_content_1=1
        else:
            item_fat_content_2=1

        outlet_size_0=0
        outlet_size_1=0
        outlet_size_2=0

        if outlet_size=="High":
            outlet_size_0=1
        elif outlet_size=="Medium":
            outlet_size_1=1
        else:
            outlet_size_2=1

        outlet_location_type_0=0
        outlet_location_type_1=0
        outlet_location_type_2=0

        if outlet_location_type=="Tier 1":
            outlet_location_type_0=1
        elif outlet_location_type=="Tier 2":
            outlet_location_type_1=1
        else:
            outlet_location_type_2=1
        
        outlet_type_0=0
        outlet_type_1=0
        outlet_type_2=0
        outlet_type_3=0

        if outlet_type=="Grocery Store":
            outlet_type_0=1
        elif outlet_type=="Supermarket Type1":
            outlet_type_1=1
        elif outlet_type=="Supermarket Type1":
            outlet_type_2=1
        else:
            outlet_type_3=1

        item_type_0=0
        item_type_1=0
        item_type_2=0

        if item_type=="Drinks":
            item_type_0=1
        elif item_type=="Food":
            item_type_1=1
        else:
            item_type_2=1

        feature=[item_weight,item_visibility,item_mrp,Outlet_Years,
                 Item_Visibility_MeanRatio,item_fat_content_0,item_fat_content_1,
                 item_fat_content_2,outlet_size_0,outlet_size_1,outlet_size_2,
                 outlet_location_type_0,outlet_location_type_1,outlet_location_type_2,
                 outlet_type_0,outlet_type_1,outlet_type_2,outlet_type_3,item_type_0,
                 item_type_1,item_type_2]
        # Load the trained model and make a prediction
        with open(r'model\rf.pkl', 'rb') as f:
            model = pickle.load(f)
        prediction = model.predict([feature])
        logger.info('Prediction made: {}'.format(prediction))


        # Format the prediction as a string with 2 decimal places
        prediction_str = '{:.2f}'.format(prediction[0])
        
        return render(request, 'predict.html', {'prediction': prediction_str})
    else:
        logger.warning('Unexpected request method: {}'.format(request.method))
        return render(request, 'predict.html')