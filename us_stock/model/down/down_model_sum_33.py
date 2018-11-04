import pandas as pd
import numpy as np 
import datetime
import time
import xarray as xr
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
from sqlalchemy import create_engine
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.linear_model import LassoCV 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from  sklearn.metrics  import  average_precision_score 
from sklearn.metrics import r2_score  
import csv
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
from sqlalchemy import create_engine
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from  sklearn.metrics  import  average_precision_score 
from sklearn.metrics import r2_score  
from xgboost import XGBRegressor
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_iris
from sklearn.svm import SVC
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras import callbacks
from keras import optimizers


def nptopd(x, y):
    test=x.tolist()
    predict=y.tolist()
    li=[]
    li.append(test)
    li.append(predict)
    #print(li)
    #lo=[i for i in map(list, zip(*li))]
    df=pd.DataFrame(li)
    df=df.T
    #df.dropna(axis = 1)
    return df

# def get_01(n):
#     if n>0:
#         return 1
#     else:
#         return 0

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

all=pd.read_csv(date+'down_analysis.csv')
all=all.drop(['code'], axis = 1)

all=all[all!=0]
# all=all.dropna(thresh=10)
all=all.dropna()
all=all.fillna(0)
# all.to_csv('tmp.csv')



all['li_123_tmp']=all['li_123_tmp']


print(abs(all.corr()).sort_values("li_123_tmp",ascending=False)["li_123_tmp"])




######################################################################
                            
                            # 分类

######################################################################

def get_01(n):
    if n<-0.05:
        return 1
    else:
        return 0


print('##########################分类#################################')
all['li_123_tmp_fenlei']=all['li_123_tmp'].apply(get_01)
# y=(all['li_123_tmp'].apply(np.log1p))
y=all['li_123_tmp_fenlei'].values
# y=(all['li_123_tmp'].apply(np.log1p))
X=all.drop(['li_123_tmp','li_123_tmp_fenlei'], axis = 1)
print(X.columns.values.tolist())
X=X.values
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

# X_trainval,X_test,y_trainval,y_test = train_test_split(X,y,random_state=0)
X_trainval,X_test,y_trainval,y_test = train_test_split(X,y,test_size = 0.2)
X_train,X_val,y_train,y_val = train_test_split(X_trainval,y_trainval,random_state=1)



######################         SVM         #################
######################        START        #################
best_score = 0.0
for gamma in [0.001,0.01,0.1,1,10,100]:
    for C in [0.001,0.01,0.1,1,10,100]:
        svm = SVC(gamma=gamma,C=C)
        svm.fit(X_train,y_train)
        score = svm.score(X_val,y_val)
        if score > best_score:
            best_score = score
            best_parameters = {'gamma':gamma,'C':C}
svm = SVC(**best_parameters) #使用最佳参数，构建新的模型
svm.fit(X_trainval,y_trainval) #使用训练集和验证集进行训练，more data always results in good performance.
y_predst=svm.predict(X_test)

joblib.dump(svm, date+'_down_model.joblib') 

predd=pd.DataFrame({'y_test':y_test,'y_pred':y_predst})
predd.to_csv('predd.csv')

test_score = svm.score(X_test,y_test) # evaluation模型评估
print("Best score on validation set:{:.2f}".format(best_score))
print("Best parameters:{}".format(best_parameters))
print("Best score on test set:{:.2f}".format(test_score))


# joblib.dump(clf, 'filename.joblib') 
# clf = joblib.load('filename.joblib') 


best_score = 0.0
for gamma in [0.001,0.01,0.1,1,10,100]:
    for C in [0.001,0.01,0.1,1,10,100]:
        svm = SVC(gamma=gamma,C=C)
        scores = cross_val_score(svm,X_trainval,y_trainval,cv=5) #5折交叉验证
        score = scores.mean() #取平均数
        if score > best_score:
            best_score = score
            best_parameters = {"gamma":gamma,"C":C}
svm = SVC(**best_parameters)
svm.fit(X_trainval,y_trainval)
test_score = svm.score(X_test,y_test)
print("Best score on validation set:{:.2f}".format(best_score))
print("Best parameters:{}".format(best_parameters))
print("Score on testing set:{:.2f}".format(test_score))



from sklearn.model_selection import cross_val_score

best_score = 0.0
for gamma in [0.001,0.01,0.1,1,10,100]:
    for C in [0.001,0.01,0.1,1,10,100]:
        svm = SVC(gamma=gamma,C=C)
        scores = cross_val_score(svm,X_trainval,y_trainval,cv=5) #5折交叉验证
        score = scores.mean() #取平均数
        if score > best_score:
            best_score = score
            best_parameters = {"gamma":gamma,"C":C}
svm = SVC(**best_parameters)
svm.fit(X_trainval,y_trainval)
test_score = svm.score(X_test,y_test)
print("Best score on validation set:{:.2f}".format(best_score))
print("Best parameters:{}".format(best_parameters))
print("Score on testing set:{:.2f}".format(test_score))



from sklearn.model_selection import GridSearchCV

#把要调整的参数以及其候选值 列出来；
param_grid = {"gamma":[0.001,0.01,0.1,1,10,100],
             "C":[0.001,0.01,0.1,1,10,100]}
print("Parameters:{}".format(param_grid))

grid_search = GridSearchCV(SVC(),param_grid,cv=5) #实例化一个GridSearchCV类

grid_search.fit(X_train,y_train) #训练，找到最优的参数，同时使用最优的参数实例化一个新的SVC estimator。
print("Test set score:{:.2f}".format(grid_search.score(X_test,y_test)))
print("Best parameters:{}".format(grid_search.best_params_))
print("Best score on train set:{:.2f}".format(grid_search.best_score_))




######################         END         #################
######################         SVM         #################




























# data_train =  xgb.DMatrix(val_X,label=val_y)
# data_test = xgb.DMatrix('Desktop/dataset/agaricus.txt.test')




















######################################################################
                            
                            # 回归

######################################################################

print('##########################回归#################################')

# all['li_123_tmp_fenlei']=all['li_123_tmp'].apply(get_01)
# y=(all['li_123_tmp'].apply(np.log1p))
# y=all['li_123_tmp'].values
# y=(all['li_123_tmp'].apply(np.log1p))


# all['li_123_tmp']= np.log1p(all['li_123_tmp'])
# all['li_123_tmp']=np.expm1(all['li_123_tmp'])
all=all.dropna()
all=all.fillna(0)
X=all.drop(['li_123_tmp'], axis = 1)
y=all['li_123_tmp'].values

mean = X.mean(axis=0)
X -= mean # 减去均值
std = X.std(axis=0) # 特征标准差
X /= std



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)



















# sns.distplot(all['li_123_tmp']);
# plt.show()


# col=['li_123_tmp','li_0grow_tmp','li_1grow_tmp','li_2grow_tmp','li_3grow_tmp','li_4grow_tmp','li_5grow_tmp']
# cols=['li_123_tmp','li_1up_tmp','li_2up_tmp','li_3up_tmp','li_4up_tmp','li_5up_tmp']
# sns.pairplot(all[cols], size = 2.5)
# plt.savefig('./ssss.png')


# plt.show()


print('-----------------------keras_start------------------------')
# model = Sequential()
# model.add(Dense(5, input_dim=X_train.shape[1], activation='relu'))
# model.add(Dense(3, activation='softmax'))

# model.add(Dense(1, activation='softmax'))

# model.compile(loss='mse', optimizer='sgd')

# print('Training -----------')
# for step in range(10000):
#     cost =model.train_on_batch(X_train, y_train)
#     if step % 50 == 0:
#         print("After %d trainings,the cost: %f" % (step, cost))

 

# # testing
# print('\nTesting ------------')
# cost = model.evaluate(X_test, y_test, batch_size=40)
# print('test cost:', cost)
# W, b = model.layers[0].get_weights()
# print('Weights=', W, '\nbiases=', b)

 

# # predict
# y_pred = model.predict(X_test)
# r2_score_enet = r2_score(y_test, y_pred)
# print('R2='+str(r2_score_enet))




print('-----------------------keras_end------------------------')














var = ['li_0grow_tmp','li_1grow_tmp','li_2grow_tmp','li_3grow_tmp','li_4grow_tmp','li_5grow_tmp','li_1up_tmp','li_2up_tmp','li_3up_tmp','li_4up_tmp','li_5up_tmp']
for i in var:
    data = pd.concat([all['li_123_tmp'], all[i]], axis=1)
    data.plot.scatter(x=i, y='li_123_tmp', ylim=(-4,4));
    plt.savefig(r'./down_'+i+'.png')















max_features=[.1 ,.3 ,.5 ,.7 ,.9 ,.99]
test_scores_li=[]
for max_feat in max_features:
    clf = RandomForestRegressor(n_estimators=200,max_features=max_feat)
    #n_estimators 代表要多少棵树
    test_scores=np.sqrt(-cross_val_score(clf,X_train,y_train,cv=5,scoring='neg_mean_squared_error'))
    test_scores_li.append(np.mean(test_scores))
print(test_scores_li)



alphas = np.logspace(-3,2,50)
test_scores_li=[]
for alpha in alphas:
    clf = linear_model.Ridge(alpha)
    test_scores=np.sqrt(cross_val_score(clf,X_train,y_train,cv=10,scoring='neg_mean_squared_error'))
    test_scores_li.append(np.mean(test_scores))
print(test_scores_li)






print('#####################ElasticNet_START#################################')
ElasticNetCV = ElasticNetCV(cv=20)
ElasticNetCV.fit(X, y)
print(ElasticNetCV.alpha_)
alpha=ElasticNetCV.alpha_


clf = ElasticNet(alpha=alpha, l1_ratio=0.7, max_iter=80000)  
clf.fit(X_train, y_train)
print(clf.coef_)  # 系数
print(clf.intercept_)  # 常量
li=list(clf.coef_)
y_pred_enet=clf.predict(X_test)
r2_score_enet = r2_score(y_test, y_pred_enet)
print('R2='+str(r2_score_enet))



print('#####################ElasticNet_END#################################')









ridgecv = LassoCV(max_iter=80000)
#ridgecv = LassoCV(alphas=[0.008, 0.009, 0.01, 0.011, 0.012])
ridgecv.fit(X, y)
print(ridgecv.alpha_)
alpha=ridgecv.alpha_
clf = linear_model.Lasso(alpha=alpha, max_iter=80000)  
clf.fit(X_train, y_train)
clf_predict = clf.predict(X_test)

r2=r2_score(y_test, clf_predict)
df=nptopd(y_test, clf_predict)
# print(clf.coef_)  # 系数
# print(clf.intercept_)  # 常量
print('R2='+str(r2))




#ridgecv = RidgeCV(alphas=[0.01, 0.1, 0.5, 1, 3, 5, 7, 10, 20, 100])
ridgecv = RidgeCV(alphas=[0.008, 0.009, 0.01, 0.011, 0.012])
ridgecv.fit(X_train, y_train)
print(ridgecv.alpha_)
alpha=ridgecv.alpha_

clf = linear_model.Ridge(alpha=alpha)  
#第一种的
clf.fit(X_train, y_train)
clf_predict = clf.predict(X_test)
RMSE = np.sqrt(mean_squared_error(y_test,clf_predict))
print(RMSE)
MSE = mean_squared_error(y_test, clf_predict)
print(MSE)


#accuracy_score(y_test,clf_predict) #只能分类
#average_precision_score(y_test,clf_predict)




#loss  = make_scorer(my_custom_loss_func, greater_is_better=False)
#score = make_scorer(my_custom_loss_func, greater_is_better=True)
#print(loss(clf,X_test, y_test))
#print(score(clf,X_test, y_test))



#第二种
 
test_scores=cross_val_score(clf, X, y, cv=10, scoring='r2') 
#test_scores=cross_val_score(clf, X, y, cv=5, scoring='mean_absolute_error')
print(test_scores)
test_scores=cross_val_score(clf, X, y, cv=10) 
#scores = cross_val_score(clf, X, y, cv=10, scoring='neg_mean_squared_error') 
print(test_scores)



test_scores=[]
params = [1,2,3,4,5]
for param in params :
    clf = XGBRegressor(max_depth=param)

    test_score = np.sqrt(-cross_val_score(clf, X_train, y_train, cv=10, scoring='neg_mean_squared_error'))
    # test_score = cross_val_score(clf, X, y, cv=10)
    test_scores.append(test_score)


for score in test_scores:
	print(score)
	per=sum(score)/len(score)
	print(per)




regr = xgb.XGBRegressor(
                 colsample_bytree=0.2,
                 gamma=0.0,
                 learning_rate=0.05,
                 max_depth=6,
                 min_child_weight=1.5,
                 n_estimators=7200,                                                                  
                 reg_alpha=0.9,
                 reg_lambda=0.6,
                 subsample=0.2,
                 seed=42,
                 silent=1)

regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
r2=r2_score(y_test, y_pred)

print('R2='+str(r2))

print('------------------------------------------------')

from sklearn import linear_model
clf = linear_model.BayesianRidge()
clf.fit(X_train, y_train)
y_pred = regr.predict(X_test)
r2=r2_score(y_test, y_pred)

print('R2='+str(r2))





















# all.to_csv('tmp.csv')
# print(all)