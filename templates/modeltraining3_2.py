import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np

data=pd.read_csv("New dataset.csv")
data = data.fillna(data.median())
data=data.drop(['Image Processing','Big Data','Cloud Computing','Distributed Systems',
                'Soft Computing','Data Science and Analytics','Internet of Things',
                'Software Testing Methodologies','Computer Graphics','CD','DWDM'],axis=1)

x=data.drop(['R Programming','Unix Programming','Object Oriented Analysis and Design','Machine Learning',
             'E-Commerce','Cyber Forensics','Mobile Computing','Advanced Databases','Human Computer Interaction'],axis=1)
y=np.array(data[['R Programming','Unix Programming','Object Oriented Analysis and Design','Machine Learning',
                 'E-Commerce','Cyber Forensics','Mobile Computing','Advanced Databases','Human Computer Interaction']])
x=np.array(x)

train_features, test_features, train_labels, test_labels = train_test_split(x, y, test_size = 0.25, random_state = 42)
rf = RandomForestRegressor(n_estimators = 30, random_state = 42)
rf.fit(train_features, train_labels)

pickle.dump(rf,open('modelfor3_2.pkl','wb'))
