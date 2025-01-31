# -*- coding: utf-8 -*-
"""Black Friday.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T-72JkVjdWFPbxitLF_RwQ9k87UYWH2K
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

"""## Loading the data."""

df=pd.read_csv('/content/train.csv')

df.head(5)

df.shape

df.describe()

df.info()

df.isnull().sum()

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Gender', palette='mako')
## The count of Male gender is higher as compared to the female.

plt.figure(figsize=(10, 6))
sns.barplot(x='Gender',y='Marital_Status',data=df)
## The below visualization shows us that the female gender is slightly higher compared to the male gender.

plt.figure(figsize=(10, 6))
sns.barplot(x='Gender',y='Purchase',data=df)
## Higher purchases have been done by the male gender as compared to the female.

plt.figure(figsize=(10, 6))
sns.barplot(x='Occupation',y='Purchase',data=df);
## Occupation has a direct effect on the purchases done by the customer and the occupation codes 12,15,17 have higher purchases.

plt.figure(figsize=(10, 6))
sns.barplot(x='Occupation',y='Purchase',hue='Gender',data=df)
## In this graph it can be seen that the female gender in the occupation 18 with higher purchases compared to others.

"""Checking the presence of outliers using BoxPlot."""

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Gender", y="Purchase")
## Using boxplot we can detect the presence of outliers in the data.

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Occupation", y="Purchase")
## The purchase column has outliers which may effect the performance of the machine learning models.

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Age", y="Purchase")
## We can see below that the Age with Purchases again have some outliers present in them.

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Product_Category_1", y="Purchase")
## There are outliers present in the Product category as well.

## Data preprocessing is a data mining technique which is used to transform the raw data in a useful and efficient format.

df['Product_ID'] = df['Product_ID'].str.replace('P00', '')
ss = StandardScaler()
df['Product_ID'] = ss.fit_transform(df['Product_ID'].values.reshape(-1, 1))
## Replacing ''P00'' with no value and scaling the ProductID column.

df.drop(['Product_Category_3'],axis=1,inplace=True)
## There are more than 50 percent missing values present in the Product_category_column so we will drop that column.

df['Product_Category_2']=df['Product_Category_2'].fillna(df['Product_Category_2'].mean())
## The missing data in the product category 2 column have been imputed using mean.

df.isnull().sum()

"""Label Encoding is a technique used to turn categorical variables to numeric values."""

cat_cols=['Gender','City_Category','Age']
le=LabelEncoder()
for i in cat_cols:
    df[i]=le.fit_transform(df[i])
df.dtypes
## The label encoding technique will now replace all the categorical variables to numeric for easier computation.

df['Stay_In_Current_City_Years']=df['Stay_In_Current_City_Years'].replace('4+','4')
## Values in the Stay_In_Current_City_Years column has been changed from 4+ to 4

df['Gender']=df['Gender'].astype(int)
df['Age']=df['Age'].astype(int)
df['Stay_In_Current_City_Years']=df['Stay_In_Current_City_Years'].astype(int)
## The gender, Age and Stay_In_Current_City_Years values are changed to integer types.

df['City_Category']=df['City_Category'].astype('category')
## The type of city_category has been changed from int to category.

df

"""# Distribution plot

### The distribution plot shows us how the overall data is distributed in the dataframe.

In probability theory and statistics, skewness is a measure of the asymmetry of the probability distribution of a real-valued random variable about its mean. The skewness value can be positive, zero, negative, or undefined.

For a unimodal distribution, negative skew commonly indicates that the tail is on the left side of the distribution, and positive skew indicates that the tail is on the right. In cases where one tail is long but the other tail is fat, skewness does not obey a simple rule. For example, a zero value means that the tails on both sides of the mean balance out overall; this is the case for a symmetric distribution, but can also be true for an asymmetric distribution where one tail is long and thin, and the other is short but fat.
"""

rows=3
cols=3
fig, ax=plt.subplots(nrows=rows,ncols=cols,figsize=(10,4))
col=df.columns
index=2
for i in range(rows):
    for j in range(cols):
        sns.distplot(df[col[index]],ax=ax[i][j])
        index=index+1

plt.tight_layout()
## The distribution plot helps us to detect the skewness of the data.Below as it can be seen that the purchase column

"""# Log transformation

The log transformation is, arguably, the most popular among the different types of transformations used to transform skewed data to approximately conform to normality. If the original data follows a log-normal distribution or approximately so, then the log-transformed data follows a normal or near normal distribution.
"""

df['Purchase']=np.log(df['Purchase'])
## The log transformation will help us transform the data and change the data to normal distribution

df= pd.get_dummies(df)
df.head()
## The get_dummies() function is used to convert categorical variable into dummy/indicator variables.

"""# Train test split."""

X=df.drop(labels=['Purchase'],axis=1)
Y=df['Purchase']
X.head()
## The data is split into X and Y where independent and dependent variables have been separated.

# Target column.
Y

"""## 80 percent data is used for training purpose and 20 percent is used for testing."""

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)
print(X_train.shape,X_test.shape,Y_train.shape,Y_test.shape)
## The data has been split into Train and test.

"""## Scaling the data"""

scaled=StandardScaler()
X_train=scaled.fit_transform(X_train)
X_test=scaled.transform(X_test)
## StandardScaler standardizes a feature by subtracting the mean and then scaling to unit variance.

"""# Machine Learning.

## Linear Regression
"""

model=LinearRegression()
model.fit(X_train,Y_train)

Y_predict=model.predict(X_test)
## Predicting on X_test

score=r2_score(Y_test,Y_predict)
mae=mean_absolute_error(Y_test,Y_predict)
mse=mean_squared_error(Y_test,Y_predict)
rmse=(np.sqrt(mean_squared_error(Y_test,Y_predict)))
print('r2_score: ',score)
print('mean_absolute_error: ',mae)
print('mean_squared_error: ',mse)
print('root_mean_squared_error: ',rmse)

"""### The above evaluation metrics help us to find how well our model is performing. As we can see the r2_score is only 0.20 and as the Root mean square error is high the model is not very accurate to predict the purchases or the target column.

## Decision Tree Regressor
"""

DT=DecisionTreeRegressor(max_depth=9)
DT.fit(X_train,Y_train)

#predicting train
train_preds=DT.predict(X_train)
#predicting on test
test_preds=DT.predict(X_test)

RMSE_train=(np.sqrt(metrics.mean_squared_error(Y_train,train_preds)))
RMSE_test=(np.sqrt(metrics.mean_squared_error(Y_test,test_preds)))
print("RMSE TrainingData = ",str(RMSE_train))
print("RMSE TestData = ",str(RMSE_test))
print('-'*50)
print('RSquared value on train:',DT.score(X_train, Y_train))
print('RSquared value on test:',DT.score(X_test, Y_test))

"""### The Decision Tree Regressor is better compared to Linear regression as it can be observed that the root mean square error is less as compared to the previous model and the RSuared value is higher in this model.

## Random Forest Regressor
"""

RF=RandomForestRegressor().fit(X_train,Y_train)

#predicting train
train_preds1=RF.predict(X_train)
#predicting on test
test_preds1=RF.predict(X_test)

RMSE_train=(np.sqrt(metrics.mean_squared_error(Y_train,train_preds1)))
RMSE_test=(np.sqrt(metrics.mean_squared_error(Y_test,test_preds1)))
print("RMSE TrainingData = ",str(RMSE_train))
print("RMSE TestData = ",str(RMSE_test))
print('-'*50)
print('RSquared value on train:',RF.score(X_train, Y_train))
print('RSquared value on test:',RF.score(X_test, Y_test))

"""### The Random Forest regressor model is again better than the previous model as we have a lower root mean square error value and the Rsquared value is higher than the previous model."""

df_test=pd.read_csv('/content/test.csv')

df_test.head(5)

df_test.isnull().sum()

"""## The null values in the test data have to be treated as well."""

df_test['Product_ID'] = df_test['Product_ID'].str.replace('P00', '')
ss = StandardScaler()
df_test['Product_ID'] = ss.fit_transform(df_test['Product_ID'].values.reshape(-1, 1))
## The 'P00' value has been replaced int he ProductId column and the column has been scaled.

df_test.drop(['Product_Category_3'],axis=1,inplace=True)
## As the Product_Category_3 column in the train set had been removed. Same has been done here aswell.

df_test['Product_Category_2']=df_test['Product_Category_2'].fillna(df_test['Product_Category_2'].mean())
## Product_Category_2 has been imputed with mean

df_test.isnull().sum()
## As we see there are no null values in the test dataframe as well.

df_test.head(5)

"""## Label Encoding categorical data"""

cat_cols=['Gender','City_Category','Age']
le=LabelEncoder()
for i in cat_cols:
    df_test[i]=le.fit_transform(df_test[i])
df_test.dtypes
## The label encoding technique will now replace all the categorical variables to numeric for easier computation.

"""## Categorical data in the test dataframe are converted to numeric values using label encoding."""

df_test['Stay_In_Current_City_Years']=df_test['Stay_In_Current_City_Years'].replace('4+','4')
## The 4+ value in the Stay_In_Current_City_Years have been replaced with only 4.

df_test['Gender']=df_test['Gender'].astype(int)
df_test['Age']=df_test['Age'].astype(int)
df_test['Stay_In_Current_City_Years'] = df_test['Stay_In_Current_City_Years'].fillna(0).astype(int)
df_test = df_test.dropna(subset=['Stay_In_Current_City_Years'])
df_test['Stay_In_Current_City_Years'] = df_test['Stay_In_Current_City_Years'].astype(int)

df_test['Stay_In_Current_City_Years']=df_test['Stay_In_Current_City_Years'].astype(int)
df_test['City_Category']=df_test['City_Category'].astype('category')
## The values in the test set have been converted to integer types as done in the train set.

df_test= pd.get_dummies(df_test)
## Dummies are created for the test set.

df_test.head()

"""### Shape of the train data."""

df.shape
# train data shape

"""### Shape of the test data."""

df_test.shape
# test data shape

df.head(5)

df_test.head(5)

# test_preds= RF.predict(df_test)
# len(test_preds)

"""## As random forest regressor performed very well compared to linear regression and decision tree regressor model. Random forest regressor model has been used to predict on our test dataset."""

id_frame=pd.read_csv('test.csv')

ID_info= id_frame[["User_ID","Product_ID"]]
ID_info.head()
## Using User_Id and Product_Id from the test set.

predictions= pd.DataFrame(test_preds, columns=["Purchase"])
predictions["User_ID"]= ID_info["User_ID"]
predictions["Product_ID"]= ID_info["Product_ID"]
predictions.head()
## Predictions have been save in the form of a dataframe

predictions.to_csv('BlackFridayPredictions.csv', index=False)
## Finally converted the prediction into csv format.