**Titanic_Prediction_API**

Titanic Prediction is a Django based REST API which isused to predict whether survived or not.

**To run this application,**
    
    1. You can either download the sample as a ZIP file and extract it or clone the repository to your local machine:
       git clone https://github.com/SrinathMurali96/Titanic_Prediction_API.git
       
    2. Go to the directory that contains the sample code:
       cd python-docs-samples\appengine\standard_python3\titanic_prediction_api
      
    3. To run the Django app on your local computer, set up a Python development environment, including Python, pip, and virtualenv
        Reference : https://docs.djangoproject.com/en/3.2/topics/install/
        
    4. Create an isolated Python environment, and install dependencies:
       
       In Windows:
       
        virtualenv env
        env\scripts\activate
        pip install -r requirements.txt

    5. Start a local web server:
       python manage.py runserver 0.0.0.0:8003
    
    6. Hit the API with the parameters
       Eg: Eg: http://localhost:8003/services/predictionService?age=22&sex=male&sibsp=1
    
**Sample API Calls:**

![Sample_API_Call_1](https://user-images.githubusercontent.com/25709838/120756206-99881f80-c52c-11eb-83b6-2c8ea409e323.png)

![Sample_API_Call_2](https://user-images.githubusercontent.com/25709838/120756220-9db43d00-c52c-11eb-8007-fd42018125b2.png)


