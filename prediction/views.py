import logging
import os
import pickle
import traceback
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
LOGGER = logging.getLogger(__name__)
NUMERIC_TYPES = ['int32', 'int64', 'float32', 'float64']
default_data_frame =  {"pclass":"1","sex":"female","age":"29","sibsp":"0","parch":"0","ticket":"24160","fare":"211.3375","cabin":"B5","embarked":"S","boat":"2","home.dest":"St Louis, MO"}
from django.views.decorators.csrf import csrf_exempt
from prediction.exceptions import NewLabelsError,InAdequateNumberOfFeaturesError
from project.settings import PICKLE_PATH
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

"""
API:Predictiong the results based on requested model and providing the result for the data requested
"""
@csrf_exempt
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def prediction_service(request):
    LOGGER.info('Inside the Method prediction_service')
    data = {'message': 'Success'}
    try:
        # Getting the input from the user
        user_input = request.GET
        user_input = dict(user_input)
        user_input = dict((k,v[0]) if type(v)==list else (k, v) for k, v in user_input.items())
        prediction_data_frame = default_data_frame
        user_input = {key.strip():value.strip() for key, value in user_input.items()}
 
        prediction_data_frame.update(user_input)
        prediction_data_frame = pd.DataFrame.from_records([prediction_data_frame])
        LOGGER.info("Received Data: {}".format(prediction_data_frame))
        
        # Fetching the trained model from the pickle file
        pickle_name = os.path.join(PICKLE_PATH, 'titanic_model.pkl')
        load_pickle_object = open(pickle_name, "rb")
        pickle_object_list = pickle.load(load_pickle_object)  
        model = pickle_object_list[0]
        label_encoder = pickle_object_list[1]

        # Applying the encoding for the values
        for en_col in label_encoder:
            prediction_data_frame[en_col] = label_encoder[en_col].transform(prediction_data_frame[en_col])

        # Predicting the target survived
        predicted_value = model.predict(prediction_data_frame)
                
        confidence = (model.predict_proba(prediction_data_frame)).tolist()
        confidence_list = []
        
        # Fetching the confidence value
        for i in confidence:
            probability = max(i)
            probability = float(probability) * 100
            probability = '%.2f' % probability
            confident = str(probability + "%")
            confidence_list.append(confident)
            
        data['survived'] = predicted_value[0]
        data['confidence'] = confidence_list[0]
        
    except NewLabelsError:
        LOGGER.error(traceback.format_exc())
        data['message'] = 'Data set Contains New Labels'
    except InAdequateNumberOfFeaturesError:   
        LOGGER.error(traceback.format_exc())
        data['message'] = 'In adequate number of features'
    except TypeError:
        LOGGER.error(traceback.format_exc())
        data['message'] = 'New labels found.Please check the featureList Numerical values'
    except Exception:
        LOGGER.error(traceback.format_exc())
        data['message'] = 'Failure, Please check the column list'

    LOGGER.info("Sent data: {}".format(data))
    return Response(data)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def model_training(request):
    LOGGER.info('Model Training Method Starts')
    data = {'message': 'Success'}
    try:
        df = pd.read_csv(r'E:\Application\titanic_prediction\titanic_dataset.csv')
                
        # Number of rows and columns in the dataset
        LOGGER.info('Shape of the Dataframe is')
        LOGGER.info(df.shape)
        
        print(df.columns.values)
        # Removing all the missing/null values
        df.dropna(how='all', axis=1, inplace=True)
        
        target_df = df.loc[:, 'survived']
        significant_attributes =['pclass','sex','age','sibsp','parch','ticket','fare','cabin','embarked','boat','home.dest']
        significant_attributes_df = df[significant_attributes]
        
        # Applying the encoding to the attributes
        label_encoder_dict = {}
        for en_col in significant_attributes_df:
            if significant_attributes_df[en_col].dtype not in NUMERIC_TYPES:
                LOGGER.info('Applying encoder for {}'.format(en_col))
                le = LabelEncoder()
                significant_attributes_df[en_col] = significant_attributes_df[en_col].astype(str)
                le_obj = le.fit(significant_attributes_df[en_col])
                label_encoder_dict[en_col] = le_obj
                significant_attributes_df[en_col] = le_obj.transform(significant_attributes_df[en_col])
        
        x_train, x_test, y_train, y_test = train_test_split(significant_attributes_df, target_df,test_size = 0.1,random_state=6)
        
        # Training the model
        model = RandomForestClassifier()
        model = model.fit(x_train,y_train)
        accuracy = accuracy_score(y_test,model.predict(x_test))
        LOGGER.info("Model accuracy is ",accuracy)
        pickle_object_list = [model,label_encoder_dict]
        pickle_name = os.path.join(PICKLE_PATH,'titanic_model.pkl')
        pickle_out = open(pickle_name, "wb")
        pickle.dump(pickle_object_list, pickle_out, protocol=4)
        pickle_out.close()
        
    except Exception:
        LOGGER.error(traceback.format_exc())
        data['message'] = 'Model Training Failed'

    LOGGER.info("Sent data: {}".format(data))
    return Response(data)