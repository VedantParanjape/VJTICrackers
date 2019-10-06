# Import the necessary libraries
import numpy
import matplotlib.pyplot as plot
import pandas
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import requests
import json

# Import the dataset
dataset = pandas.read_csv("app/dataset2.csv")
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 1].values

# print("x:       ")
# print(x)

# print("y:         ")
# print(y)
# Split the dataset into the training set and test set
# We're splitting the data in 1/3, so out of 30 rows, 20 rows will go into the training set,
# and 10 rows will go into the testing set.
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 1/3, random_state = 0)


# Creating a LinearRegression object and fitting it
# on our training set.
linearRegressor = LinearRegression()
# print("x:       ")
# print(xTest)
# print("y:       ")
# print(yTest)

xTest=xTest.reshape(-1, 1)
yTest=yTest.reshape(-1, 1)
xTrain=xTrain.reshape(-1, 1)
yTrain=yTrain.reshape(-1, 1)

linearRegressor.fit(xTrain, yTrain)

# print(xTest)
# Predicting the test set results
yPrediction = linearRegressor.predict(xTest)
print(linearRegressor.predict([[1.8]]))
# Saving model to disk
pickle.dump(linearRegressor, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load( open('model.pkl','rb'))
print(model.predict([[1.8]]))
# yNew = linearRegressor.predict([[15.17]])
# print(yNew)
# print(yPrediction)'
# xnew = 14.66
# ynew = linearRegressor.predict([xnew])
# print(ynew)
# print(len(xTrain))
# print(len(yTrain))
# Visualising the training set results
# plot.scatter(xTrain, yTrain, color = 'red')
# plot.plot(xTrain, linearRegressor.predict(xTrain), color = 'blue')
# plot.title('Deaths vs. PM2.5')
# plot.xlabel('PM2.5')
# plot.ylabel('Deaths')
# plot.show()

# Visualising the test set r
# plot.scatter(xTest, yTest, color = 'red')
# plot.plot(xTrain, linearRegressor.predict(xTrain), color = 'blue')
# plot.title('Deaths vs. PM2.5 (Test set)')
# plot.xlabel('PM2.5')
# plot.ylabel('Deaths(% of population)')
# plot.show()