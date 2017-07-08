# data preprocessing
# import libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import dataset
dataset = pd.read_csv('churn.csv')
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

# encode categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# encode countries
label_encoder_x_country = LabelEncoder()
X[:, 1] = label_encoder_x_country.fit_transform(X[:, 1])

# encode gender
label_encoder_x_gender = LabelEncoder()
X[:, 2] = label_encoder_x_gender.fit_transform(X[:, 2])

# dummy variables (binary one-hot encoding)
onehotencoder = OneHotEncoder(categorical_features=[1])
X = onehotencoder.fit_transform(X).toarray()

# avoid dummy variable trap (break multicollinearity between independent variables)
# remove column for first country from X 
X = X[:, 1:]

# split dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# scale features (standardize range of independent variables)
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

# build artificial neural network
import keras
from keras.models import Sequential # used to initialize neural network
from keras.layers import Dense # used to create layers in artificial neural network

# initialize neural network
classifier = Sequential()

# add layers
# units = average of input nodes and output nodes = (11 + 1)/2 = 6

# input layer and first hidden layer
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_shape=(11,)))

# second hidden layer
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))

# output layer
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))

# compile neural network
# stochastic gradient optimizer : adam
# loss function : binary crossentropy
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# fit neural network to training set
classifier.fit(x=X_train, y=y_train, batch_size=10, epochs=100)

# predict test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# create confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# predict a single new observation
'''
Geography: France
Credit Score: 600
Gender: Male
Age: 40 years old
Tenure: 3 years
Balance: $60000
Number of Products: 2
Does this customer have a credit card ? Yes
Is this customer an Active Member: Yes
Estimated Salary: $50000
'''

new_observation = np.array([[0.0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])

# scale new observation
new_observation = sc_X.transform(new_observation)

new_prediction = classifier.predict(new_observation)
new_prediction = (new_prediction > 0.5)