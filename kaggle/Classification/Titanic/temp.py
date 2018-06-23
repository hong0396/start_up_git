import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb

#input data
train = pd.read_csv('train_tan.csv', index = False )
test  = pd.read_csv('test_tan.csv',  index = False )

X_train = train.drop('Survived', axis=1)
y_train = train['Survived']

X_test = test
