# AIML1252
model_creation_error_msg = "Model creation is not completed, and the reasons might be not proper training data,Confusion matrix values are not valid"

model_validation_error_msg = "Model validation is not completed, and the reasons might be significant \
                        attribute mismatch,new labels found,other file has been uploaded"
batchpredsetup_error_msg = "Batch prediction setup is not performed, and the reasons\
                         might be same table and destination table are selected,all field values are not selected"
batchpred_error_msg = "Batch prediction is not performed, and the reasons might be significant \
                        attribute mismatch,new labels,other file has been uploaded"
real_time_pred_setup_error_msg = "Real time prediction is not performed, and the reasons might be all values are not provided \
                        ,new labels found"
datasource_error_msg = "Data source is not connected and the reasons might be connection details are not valid"

model_tuning_error_msg = "Model tuning is not performed, and reasons might be hyper parameters,selected ensemble algorithm"

model_training_error_msg = "Model training is not performed, and the reasons might be not proper training data, \
                        Selecting regression algorithm for classification type, Confusion matrix values are not valid"

incorrect_url_error_msg = "Please enter a Valid URL"

invalid_input_error = "Invalid Input"

# All the exceptions Base class
class CustomBaseException(Exception):
    pass

class DataSourceAvailableError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1004 -The specified schema details is already connected'

class OtherFileError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1005 -Other file has been uploaded,Please verify whether correct dataset has been uploaded'

class InAdequateNumberOfFeaturesError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1006 -Significant attribute mismatch, Please check view model info and re upload'

class NewLabelsError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1007 -The Dataset contains New Labels'


class NullValuesError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1008 -Please fill the null values and retry again'


class FileFormatError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1001 -Please upload the data in csv or excel format'


class AlgorithmTypeError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1002 -Chosen algorithm type is incorrect based on target attribute'


class ColumnNameSizeExceedsError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1003 -The column name size is exceeding the limit'


class AllValuesRequiredError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1009 -Please provide all the values to predict'


class AttributeNotSelectedError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1010 -Select the target attribute'


class NullFileError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1011 -Please fill the null values and retry again'


class MultipleWorksheetError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1012 -File contains Multiple worksheet'


class ColumnPreProcessError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1013 - Please preprocess the column names and then upload'

class EnsembleTypeError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1014 - The Selected model type is mismatch'

class NoTableError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1015 - URL Contains No Table'

class NoModelIdError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1016 - Sorry, Please select the model to proceed further'

class InvalidInputParameterError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1017 - Invalid Input'

class ModelNameError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1018 - Model Name already exists,Please contact admin for renaming the model'

class FileFormatDataError(CustomBaseException):
    def __init__(self):
        self.error = 'Error Code:1019 -Please upload the data in pickle or json format'
