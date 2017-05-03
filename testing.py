import copy

features = ['COP','SHC','IMON','R6','CUST','DUP']

def categories(pk,*args, **kwargs):
    features_in_job = Features.objects.filter(info_id = pk)
    job = Info.objects.get(pk = pk)
    job_type = job.job_type
    m2000_dict = {
        'level_2': ['REAR', 'DUP', 'MOD', '2STARTERS', 'SHC', 'EMCO', 'R6'],
        'level_3': ['mView', 'iMon', 'LOC'],
        'level_4': ['MANUAL', 'OVL'],
        'level_5': ['CUST', 'MRL'],
        'level_6': ['TSSA']}
    m4000_dict = {
        'level_2': ['REAR', 'DUP', 'MOD', '2STARTERS'],
        'level_3': ['mView', 'iMon', 'LOC', 'SHORTF'],
        'level_4': ['MANUAL', 'OVL'],
        'level_5': ['CUST'],
        'level_6': ['TSSA']}
    if job_type == '2000':
        dict = copy.deepcopy(m2000_dict)
    elif job_type == '4000':
        dict = copy.deepcopy(m4000_dict)
    else:
        pass
    if any(feature.features in dict['level_6'] for feature in features_in_job):
        category = 6
    elif any(feature.features in dict['level_5'] for feature in features_in_job):
        category = 5
    elif any(feature.features in dict['level_4'] for feature in features_in_job):
        category = 4
    elif any(feature.features in dict['level_3'] for feature in features_in_job):
        category = 3
    elif any(feature.features in dict['level_2'] for feature in features_in_job):
        category = 2
    else:
        category = 1
    return category

categories(['REAR','OVL','MANUAL','DUP','CUST'])

#def categories(pk,*args, **kwargs):
#    features_in_job = features
#    level_2 = ['REAR','DUP','MOD','2STARTERS']
#    level_3 = ['mView','iMon','LOC','SHORTF']
#    level_4 = ['MANUAL','OVL']
#    level_5 = ['CUST']
#    level_6 = ['TSSA']
#    if any(feature.features in level_6 for feature in features_in_job):
#        category = 6
#    elif any(feature.features in level_5 for feature in features_in_job):
#        category = 5
#    elif any(feature.features in level_4 for feature in features_in_job):
#        category = 4
#    elif any(feature.features in level_3 for feature in features_in_job):
#        category = 3
#    elif any(feature.features in level_2 for feature in features_in_job):
#        category = 2
#    else:
#        category = 1
#    print(category)