import pandas as pd
from fraud_platform.data import prepare_features

def test_prepare_features_encodes_type():
    df=pd.DataFrame({'step':[1,2],'type':['PAYMENT','TRANSFER'],'amount':[10,20],'oldbalanceOrg':[100,50],'newbalanceOrig':[90,30],'oldbalanceDest':[0,0],'newbalanceDest':[10,20],'isFraud':[0,1]})
    X,y=prepare_features(df)
    assert 'type_PAYMENT' in X.columns and 'type_TRANSFER' in X.columns
    assert list(y)==[0,1]
