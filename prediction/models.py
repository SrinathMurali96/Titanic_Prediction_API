from django.db import models, connections

YES_NO_CHOICES = (
    ('YES', 'YES'),
    ('NO', 'NO')
)

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('In-Active', 'In-Active')
)

class AlgorithmType(models.Model):
    algorithm_type = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'REF_ALGORITHM_TYPE'

    def __str__(self):
        return self.algorithm_type


class Algorithm(models.Model):
    algorithm_type = models.ForeignKey(AlgorithmType, on_delete=models.CASCADE)
    algorithm_name = models.CharField(max_length=100)
    algorithm_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    prediction_pattern = models.CharField('Predicted Column', db_column='PREDICTION_PATTERN', max_length=30,
                                          choices=YES_NO_CHOICES, default='NO')
    feature_contribution = models.CharField('Predicted Column', db_column='FEATURE_CONTRIBUTION', max_length=30,
                                            choices=YES_NO_CHOICES, default='NO')

    class Meta:
        managed = True
        db_table = 'REF_ALGORITHM'

    def __str__(self):
        return self.algorithm_name

class ModelDetail(models.Model):
    model_instance_id = models.AutoField('Model Instance ID', db_column='MODEL_INSTANCE_ID', primary_key=True)
    model_id = models.IntegerField('Model ID', db_column='MODEL_ID')
    model_name = models.CharField('Model Name', db_column='MODEL_NAME', max_length=35)
    model_version = models.IntegerField('Model Version', db_column='MODEL_VERSION', default=1)
    model_description = models.CharField('Model Description', db_column='MODEL_DESC', max_length=60, default='')
    model_type = models.CharField('Model Type', db_column='MODEL_TYPE', max_length=35)
    created_on = models.DateTimeField('Created On', db_column='CREATED_DATE')
    created_by = models.CharField('Created By', db_column='CREATED_BY', max_length=100)
    last_trained_on = models.DateTimeField('Last Trained On', db_column='LAST_TRAINED_DATE',null=True, blank=True)
    accuracy = models.IntegerField('Accuracy', db_column='MODEL_ACCURACY',default=0)
    predicted_column = models.CharField('Predicted Column', db_column='PREDICTED_COLUMN', max_length=200, default='')
    prediction_table = models.CharField('Prediction Table', db_column='PREDICTION_TABLE', max_length=30, default='')
    model_table = models.CharField('Model Table', db_column='MODEL_TABLE', max_length=100, default='')
    model_file_name = models.CharField('Model File Name', db_column='MODEL_FILE_NAME', max_length=45, default='')
    model_file_type = models.CharField('Model File Type', db_column='MODEL_FILE_TYPE', max_length=45, default='')
    algorithm_name = models.CharField('Algorithm Name', db_column='ALGORITHM_NAME', max_length=100, default='')
    split_ratio = models.CharField('Split Ratio', db_column='SPLIT_RATIO', max_length=100, default='')
    number_of_folds = models.IntegerField('Number of Folds', db_column='NUMBER_OF_FOLDS', default=0)
    available_versions = models.CharField('Available Versions', db_column='AVAILABLE_VERSIONS', max_length=100, default='1')
    train_type = models.CharField('Train Type', db_column='TRAIN_TYPE', max_length=15, default='')
    model_table_source = models.CharField('Model Table Source', db_column='MODEL_TABLE_SOURCE', max_length=100,
                                          default='')
    prediction_table_source = models.CharField('Prediction Table Source', db_column='PREDICTION_TABLE_SOURCE',
                                               max_length=100, default='')
    prediction_pattern = models.CharField('Prediction Pattern', db_column='PREDICTION_PATTERN', max_length=30,
                                          default='')
    feature_contribution = models.CharField('Feature Contribution', db_column='FEATURE_CONTRIBUTION', max_length=30,
                                            default='')
    model_train_time = models.IntegerField('Model Train Time', db_column='MODEL_TRAIN_TIME', default=0)
    model_status = models.CharField('Model Status', db_column='MODEL_STATUS', max_length=15, choices=STATUS_CHOICES,
                                    default='Active')
    model_metrics = models.CharField('Model Metrics', db_column='MODEL_METRICS', max_length=500, default='')
    preprocessed_data = models.CharField('Preprocessed Data', db_column='PREPROCESSED_DATA', max_length=5, default='NO')
    train_status = models.CharField('Train Status', db_column='TRAIN_STATUS', max_length=50, default='in-progress')
    final_status = models.CharField('Final Status', db_column='FINAL_STATUS', max_length=20, default='Yet to Save')
    storage = models.DecimalField('Storage', db_column='STORAGE',max_digits=10, decimal_places=5,blank=True, null=True)
    model_save = models.CharField('Model Save', db_column='MODEL_SAVE', max_length=5, default='N')
    number_of_dimensions = models.IntegerField('Number of Dimensions', db_column='NUMBER_OF_DIMENSIONS', default=0)
    feature_algorithm = models.CharField('Feature Algorithm', db_column='FEATURE_ALGORITHM', max_length=100, default='')
    algorithm_name_list = models.BinaryField('Algorithm Name List', db_column='ALGORITHM_NAME_LIST',blank=True)
    model_visibility = models.CharField('Model Visibility', db_column='MODEL_VISIBILITY', max_length=35, default='')
    feature_type = models.CharField('Feature Type', db_column='FEATURE_TYPE', max_length=35, default='')
    custom_derived_attribute = models.BinaryField('Custom Derived Attribute', db_column='CUSTOM_DERIVED_ATTRIBUTE',blank=True)
    hyperparameter_tuning = models.CharField('Hyperparameter Tuning', db_column='HYPERPARAMETER_TUNING', max_length=10, default='NO')
    hyperparameter_list = models.BinaryField('Hyperparameter List', db_column='HYPERPARAMETER_LIST',blank=True)
    job_training_status = models.CharField('Job Training Status', db_column='JOB_TRAINING_STATUS', max_length=50, default='Yet-to-start')
    rule_sequence = models.IntegerField('Rule Sequence', db_column='RULE_SEQUENCE', null=True)
    model_sequence = models.IntegerField('Model Sequence', db_column='MODEL_SEQUENCE', null=True)
    
    def save(self, **kwargs):
        if not self.model_id:
            self.model_id = get_sequence_id("sequence_model_id", "default")
        super().save(using='default', *kwargs)

    class Meta:
        managed = True
        db_table = 'MODEL_DETAILS'
        ordering = ['-model_instance_id']

    def as_json(self):
        return dict(
            model_instance_id=self.model_instance_id,
            model_id=self.model_id,
            model_name=self.model_name,
            model_type=self.model_type,
            created_on=self.created_on.strftime('%m/%d/%y %H:%M:%S'),
            created_by=self.created_by,
            updated_on=self.updated_on.strftime('%m/%d/%y %H:%M:%S'),
            last_trained_on=self.last_trained_on.strftime('%m/%d/%y %H:%M:%S'),
            accuracy=self.accuracy)


class ModelMeta(models.Model):
    DATA_TYPE_CHOICES = (
        ('Text', 'Text'),
        ('Date', 'Date'),
        ('Dropdown', 'Dropdown'),
    )
    SEARCH_TYPE_CHOICES = (
        ('B', 'Basic'),
        ('A', 'Advanced'),
    )
    VIEW_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    model_id =  models.IntegerField('Model ID', db_column='MODEL_ID')
    model_instance = models.ForeignKey(ModelDetail, on_delete=models.CASCADE)
    attribute_type = models.CharField('Attribute Type', db_column='ATTRIBUTE_TYPE', max_length=100, blank=True)
    attribute_name = models.CharField('Attribute Name', db_column='ATTRIBUTE_NAME', max_length=1000)
    attribute_label = models.CharField('Attribute Label', db_column='ATTRIBUTE_LABEL', max_length=100)
    attribute_data_type = models.CharField('Attribute Data type', db_column='ATTRIBUTE_DATA_TYPE', max_length=35,
                                           blank=True, choices=DATA_TYPE_CHOICES)
    basic_search_type = models.CharField('Basic Search Type', db_column='BASIC_SEARCH_TYPE', max_length=10,
                                         blank=True, choices=VIEW_CHOICES, default='N')
    adv_search_type = models.CharField('Advanced Search Type', db_column='ADV_SEARCH_TYPE', max_length=10,
                                       blank=True, choices=VIEW_CHOICES)
    result_view = models.CharField('Result View', db_column='RESULT_VIEW', max_length=10,
                                   blank=True, choices=VIEW_CHOICES)
    value_replace = models.CharField('Value Replace', db_column='VALUE_REPLACE', max_length=1000, blank=True,
                                     default='')

    class Meta:
        managed = True
        db_table = 'MODEL_META'


class Test_Model_Config(models.Model):
    test_table_name = models.CharField('Test Table Name', db_column='TEST_TABLE_NAME', max_length=35)
    test_table_tcol = models.CharField('Test Table Tcol', db_column='TEST_TABLE_TCOL', max_length=35)

    class Meta:
        managed = True
        db_table = 'TEST_MODEL_CONFIG'


class Train_Model_Config(models.Model):
    DATA_SOURCE_CHOICES = (
        ('default', 'ML'),
        ('ML_CRPT', 'Eureka'),
    )
    train_table_name = models.CharField('Train Table Name', db_column='TRAIN_TABLE_NAME', max_length=35)
    train_table_source = models.CharField('Train Table Source', db_column='TRAIN_TABLE_SOURCE', max_length=35,
                                          choices=DATA_SOURCE_CHOICES)

    class Meta:
        managed = True
        db_table = 'TRAIN_MODEL_CONFIG'

    def __str__(self):
        return self.train_table_name


class SchedulerJobs(models.Model):
    job_id = models.CharField('Job ID', db_column='JOB_ID', max_length=50)
    model_instance_id = models.IntegerField('Model Instance Id', db_column='MODEL_INSTANCE_ID')
    model_name = models.CharField('Model Name', db_column='MODEL_NAME', max_length=35,default='')
    job_type = models.CharField('Job Type', db_column='JOB_TYPE', max_length=35)
    trigger_mail = models.CharField('Trigger Mail', db_column='TRIGGER_MAIL', max_length=10,
                                    choices=YES_NO_CHOICES, default='NO')
    created_by = models.CharField('Created By', db_column='CREATED_BY', max_length=100)
    class Meta:
        managed = True
        db_table = 'SCHEDULER_JOBS'


class DatabaseTypeDetails(models.Model):
    db_name = models.CharField('DB Name', db_column='DB_NAME', max_length=30)
    db_description = models.CharField('DB Description', db_column='DB_DESCRIPTION', max_length=30)
    db_source = models.CharField('DB Source', db_column='DB_SOURCE', max_length=30)

    class Meta:
        managed = True
        db_table = 'REF_DB_DETAILS'


class ConnectionDetails(models.Model):
    db_name = models.ForeignKey(DatabaseTypeDetails, on_delete=models.CASCADE)
    user_name = models.CharField('Username', db_column='USER_NAME', max_length=50)
    password = models.CharField('Password', db_column='PASSWORD', max_length=50)
    server_host = models.CharField('Server Host', db_column='SERVER_HOST', max_length=50)
    port = models.IntegerField('Port', db_column='PORT', default="")
    service_name = models.CharField('Service Name', db_column='SERVICE_NAME', max_length=50)
    schema_keyspace_name = models.CharField('Schema Keyspace Name', db_column='SCHEMA_KEYSPACE_NAME', max_length=50)
    user_id = models.IntegerField('User ID', db_column='USER_ID')
    source_name = models.CharField('Source Name', db_column='SOURCE_NAME', max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'CONNECTION_DETAILS'


class SplitRatio(models.Model):
    split_ratio = models.CharField('Split Ratio', db_column='SPLIT_RATIO', max_length=10)
    ratio_sequence = models.CharField('Ratio Sequence', db_column='RATIO_SEQUENCE', max_length=10)
    split_ratio_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    class Meta:
        managed = True
        db_table = 'REF_SPLIT_RATIO'


class TrainGst(models.Model):
    model_instance = models.ForeignKey(ModelDetail, on_delete=models.CASCADE)
    data_frame = models.BinaryField('Data Frame', db_column='DATA_FRAME')

    class Meta:
        managed = True
        db_table = 'TRAIN_GST'


def get_sequence_id(sequence_name, db_name):
    with connections[db_name].cursor() as cursor:
        cursor.execute("SELECT " + sequence_name + ".nextval from dual")
        return cursor.fetchone()[0]


class DataLog(models.Model):
    log_id = models.CharField(db_column='log_id', primary_key=True, max_length=3000, null=False)
    log_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    log_description = models.CharField(max_length=3000, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    system_ip = models.CharField(max_length=100, blank=True, null=True)
    entity_type = models.CharField(max_length=200, blank=True, null=True)
    entity_id = models.CharField(max_length=50, blank=True, null=True)
    entity_old_val = models.CharField(max_length=300, blank=True, null=True)
    entity_new_val = models.CharField(max_length=300, blank=True, null=True)
    vendor_id = models.FloatField(blank=True, null=True)
    vendor_name = models.CharField(max_length=100, default='AIML')
    source = models.CharField(max_length=100, blank=True, null=True)
    application_id = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    def save(self, **kwargs):
        if not self.log_id:
            self.log_id = get_sequence_id("SEQ_DATA_LOG_ID", "audit_log")
        super().save(using='audit_log', *kwargs)

    class Meta:
        managed = False
        db_table = 'data_log'

    def as_json(self):
        return dict(
            log_id=self.log_id,
            vendor_name=self.vendor_name,
            log_description=self.log_description,
            log_time=self.log_time.strftime('%m/%d/%y %H:%M:%S'))


class HyperParametersList(models.Model):
    HYPER_PARAM_TYPE_CHOICES = (
        ('Text', 'Text'),
        ('Dropdown', 'Dropdown'),
    )
    INPUT_TYPE_CHOICES = (
        ('Int', 'Int'),
        ('Float', 'Float'),
        ('Char', 'Char'),
    )
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    label = models.CharField('Label', db_column='LABEL', max_length=500, null=True)
    hyper_param_name = models.CharField(max_length=500)
    hyper_param_input_type = models.CharField(max_length=500, blank=True, choices=HYPER_PARAM_TYPE_CHOICES)
    default_values = models.CharField(max_length=500, blank=True)
    parameter_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    input_type = models.CharField(max_length=500, blank=True, choices=INPUT_TYPE_CHOICES)


    def default_values_as_list(self):
        return self.default_values.split(',')

    class Meta:
        managed = True
        db_table = 'REF_HYPER_PARAMETERS'


class Report(models.Model):
    model_instance = models.ForeignKey(ModelDetail, on_delete=models.CASCADE)
    report_name = models.CharField('Report Name', db_column='REPORT_NAME', max_length=50)
    created_on = models.DateTimeField('Created On', db_column='CREATED_DATE')
    created_by = models.CharField('Created By', db_column='CREATED_BY', max_length=100)

    class Meta:
        managed = True
        db_table = 'REPORT_LOG'


class MenuDetail(models.Model):
    menu_reference = models.CharField('Menu Reference', db_column='MENU_REFERENCE', max_length=50)
    menu_title = models.CharField('Menu Title', db_column='MENU_TITLE', max_length=50)
    menu_icon_class = models.CharField('Menu Icon Class', db_column='MENU_ICON_CLASS', max_length=50)
    menu_status = models.CharField('Menu Status', db_column='MENU_STATUS', choices=STATUS_CHOICES, max_length=50)
    menu_sequence = models.IntegerField('Menu Sequence', db_column='MENU_SEQUENCE')
    user_name = models.CharField('User Name',db_column='USER_NAME',default='MLAdmin',max_length=50 )

    class Meta:
        managed = True
        db_table = 'MENU_DETAIL'
        ordering = ['id']

class BotDetail(models.Model):
    bot_id = models.AutoField('Bot ID', db_column='BOT_ID', primary_key=True)
    bot_name = models.CharField('Bot Name', db_column='BOT_NAME', max_length=35)
    model_name = models.CharField('Model Name', db_column='MODEL_NAME', max_length=35,default='Dummy_model')
    bot_description = models.CharField('Bot Description', db_column='BOT_DESC', max_length=60, default='')
    bot_status = models.CharField('Bot Status', db_column='BOT_STATUS', max_length=60, default='Active')
    created_on = models.DateTimeField('Created On', db_column='CREATED_DATE')
    created_by = models.CharField('Created By', db_column='CREATED_BY', max_length=100)
    intent = models.BinaryField('Intent', db_column='INTENT')
    customised_question = models.BinaryField('Customised Question', db_column='CUSTOMISED_QUESTION',null=True)
    greeting = models.CharField('Greeting',db_column='GREETING',max_length=500,default='Hi How can I help you')
    no_of_intents = models.IntegerField('Number Of Intents', db_column='NO_OF_INTENTS',default=0)
    bot_type = models.CharField('Bot Type', db_column='BOT_TYPE', max_length=60, default='Configured')
    new_utterance = models.CharField('New Utterance', db_column='NEW_UTTERANCE', max_length=100, default='')

    class Meta:
        managed = True
        db_table = 'BOT_DETAILS'
        ordering = ['-bot_id']

    def as_json(self):
        return dict(
            bot_id=self.bot_id,
            bot_name=self.bot_name,
            created_on=self.created_on.strftime('%m/%d/%y %H:%M:%S'),
            created_by=self.created_by)

class VoiceDetail(models.Model):
    voice_id = models.AutoField('Voice ID', db_column='VOICE_ID', primary_key=True)
    voice_name = models.CharField('Voice Name', db_column='VOICE_NAME', max_length=35)
    voice_description = models.CharField('Voice Description', db_column='VOICE_DESC', max_length=60, default='')
    voice_status = models.CharField('Voice Status', db_column='VOICE_STATUS', max_length=60, default='Active')
    created_on = models.DateTimeField('Created On', db_column='CREATED_DATE')
    created_by = models.CharField('Created By', db_column='CREATED_BY', max_length=100)
    intent = models.BinaryField('Intent', db_column='INTENT')

    class Meta:
        managed = True
        db_table = 'VOICE_DETAILS'
        ordering = ['-voice_id']

    def as_json(self):
        return dict(
            voice_id=self.voice_id,
            voice_name=self.voice_name,
            created_on=self.created_on.strftime('%m/%d/%y %H:%M:%S'),
            created_by=self.created_by)


class FileDetail(models.Model):
    file_id = models.AutoField('File ID', db_column='FILE_ID', primary_key=True)
    file_name = models.CharField('File Name', db_column='FILE_NAME', max_length=45, default='')
    uploaded_on = models.DateTimeField('Uploaded On', db_column='UPLOADED_ON')
    uploaded_by = models.CharField('Uploaded By', db_column='UPLOADED_BY', max_length=100)
    model_name = models.CharField('Model Name', db_column='MODEL_NAME', max_length=35)
    data_frame = models.BinaryField('Data Frame', db_column='DATA_FRAME')
    model_status = models.CharField('Model Status', db_column='MODEL_STATUS', max_length=15, choices=STATUS_CHOICES,
                                    default='Active')

    class Meta:
        managed = True
        db_table = 'FILE_DETAILS'
        ordering = ['-file_id']

    def as_json(self):
        return dict(
            file_id=self.file_id,
            file_name=self.file_name,
            uploaded_on=self.created_on.strftime('%m/%d/%y %H:%M:%S'),
            uploaded_by=self.created_by)

class Authentication(models.Model):
    authentication_system_name = models.CharField(max_length=100)
    authentication_system_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    class Meta:
        managed = True
        db_table = 'REF_AUTHENTICATION'

class CutomisedDerivedAttribute(models.Model):
    model_name = models.CharField('Model Name', db_column='MODEL_NAME', max_length=35)
    custom_derived_attribute = models.BinaryField('Custom Derived Attribute', db_column='CUSTOM_DERIVED_ATTRIBUTE',blank=True)
    class Meta:
        managed = True
        db_table = 'CUSTOM_DERIVED_ATTR'


class AlgorithmMeta(models.Model):
    model_instance = models.ForeignKey(ModelDetail, on_delete=models.CASCADE)
    model_id = models.IntegerField('Model ID', db_column='MODEL_ID')
    model_version = models.IntegerField('Model Version', db_column='MODEL_VERSION', default=1)
    alg_name = models.CharField('Algorithm Name', db_column='ALGORITHM_NAME', max_length=200)
    alg_status = models.CharField('Algorithm Status', db_column='ALGORITHM_STATUS', max_length=20)
    class Meta:
        managed = True
        db_table = 'ALGORITHM_META'
        
class ApiAggregation(models.Model):
    api_name = models.CharField('Api Name', db_column='API_NAME', max_length=50)
    aggregation_value = models.BinaryField('Aggregation Value', db_column='AGGREGATION_VALUE',blank=True)
    created_on = models.DateTimeField('Created On', db_column='CREATED_DATE')
    api_status = models.CharField('Api Status', db_column='API_STATUS', max_length=15, choices=STATUS_CHOICES,
                                    default='Active')
    class Meta:
        managed = True
        db_table = 'API_AGGREGATION'
        
class VisualizationRules(models.Model):
    rule_name = models.CharField('Rule Name', null=True, db_column='RULE_NAME', max_length=150)
    rule_id = models.IntegerField('Rule ID', db_column='RULE_ID', null=True)
    library_name = models.CharField('Library Name', null=True, db_column='LIBRARY_NAME', max_length=150)
    level_type = models.CharField('Level Type', null=True, db_column='LEVEL_TYPE', max_length=150)
    model_name = models.CharField('Model Name', null=True, db_column='MODEL_NAME', max_length=150)
    attribute_type = models.CharField('Attribute Type', null=True, db_column='ATTRIBUTE_TYPE', max_length=150)
    attribute_name = models.CharField('Attribute Name', null=True, db_column='ATTRIBUTE_NAME', max_length=150)
    method = models.CharField('Method', null=True, db_column='METHOD', max_length=150)
    operation = models.CharField('Operation', null=True, db_column='OPERATION', max_length=150)
    imputer_method = models.CharField('Imputer Method', null=True, db_column='IMPUTER_METHOD', max_length=150)
    values = models.CharField('Values', null=True, db_column='VALUES', max_length=150)
    delete_axis = models.CharField('Delete Axis', null=True, db_column='DELETE_AXIS', max_length=150)
    created_on = models.DateTimeField('Created On', null=True, db_column='CREATED_DATE')
    created_by = models.CharField('Created By', null=True, db_column='CREATED_BY', max_length=150)
    modified_on = models.DateTimeField('Modified On', null=True, db_column='MODIFIED_DATE')
    modified_by = models.CharField('Modified By', null=True, db_column='MODIFIED_BY', max_length=150)
    pair_id = models.IntegerField('Pair ID', db_column='PAIR_ID', null=True)
    
    class Meta:
        managed = True
        db_table = 'Rules'       

class RulesMeta(models.Model):
    rule_id = models.AutoField('Rule ID', db_column='RULE_ID', primary_key=True)
    file_name = models.CharField('File Name', null=True, db_column='FILE_NAME', max_length=150)
    model_name = models.CharField('Model Name', null=True, db_column='MODEL_NAME', max_length=150)
    model_id = models.IntegerField('Model ID', db_column='MODEL_ID', null=True)
    rule_name = models.CharField('Rule Name', null=True, db_column='RULE_NAME', max_length=150)
    comments = models.CharField('Comments', null=True, db_column='COMMENTS', max_length=1000)
    created_on = models.DateTimeField('Created On', null=True, db_column='CREATED_DATE')
    created_by = models.CharField('Created By', null=True, db_column='CREATED_BY', max_length=150)
    modified_on = models.DateTimeField('Modified On', null=True, db_column='MODIFIED_DATE')
    modified_by = models.CharField('Modified By', null=True, db_column='MODIFIED_BY', max_length=150)

    class Meta:
        managed = True
        db_table = 'RULES_META' 