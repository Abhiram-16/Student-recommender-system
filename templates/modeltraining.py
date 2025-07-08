import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
data=pd.read_csv('dataset.csv')
data = data.fillna(data.median())
#data.describe()
x=data.drop(['Data Science','IOT','Machine Learning'],axis=1)
y1,y2,y3=data['Data Science'],data['IOT'],data['Machine Learning']

model1=RandomForestRegressor(n_estimators=30,random_state=0)
x_train,x_test,y_train,y_test=train_test_split(x,y1,test_size=0.20)
model1.fit(x_train,y_train)

model2=RandomForestRegressor(n_estimators=30,random_state=0)
x_train,x_test,y_train,y_test=train_test_split(x,y2,test_size=0.20)
model2.fit(x_train,y_train)

model3=RandomForestRegressor(n_estimators=30,random_state=0)
x_train,x_test,y_train,y_test=train_test_split(x,y3,test_size=0.20)
model3.fit(x_train,y_train)

pickle.dump(model1,open('model1.pkl','wb'))
pickle.dump(model2,open('model2.pkl','wb'))
pickle.dump(model3,open('model3.pkl','wb'))
