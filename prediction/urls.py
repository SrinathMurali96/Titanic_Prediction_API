from django.conf.urls import url

from prediction.views import model_training,prediction_service

urlpatterns = [
    # url(r'^centuryai/services/getBatchresults', get_database_search_results, name='getBatchresults'),
    url(r'^services/predictionService/$', prediction_service, name='predictionService'),
    url(r'^services/modelTraining' ,model_training , name='model_training'),
]
