# -*- coding: utf-8 -*-
"""19BIS040-LAB-4-SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wVXu3316wE4amc_uXayAG1pRdORb77Wc

#  **GOKILA N M**
######  **19BIS040-ISE**

#  **SUPPORT VECTOR MACHINE**
##                                                  MACHINE LEARNING LAB
###   Predict whether a breast tumor is malignant or benign

#**Importing libraries and load the data**
"""

from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA 
from sklearn.svm import SVC 
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix, classification_report 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np

"""# **UPLOAD AND READ THE FILE**"""

from google.colab import files
uploaded = files.upload()
df = pd.read_csv('data.csv')

"""# **Print summary statistics of the dataset**"""

df.head(7)

df.info()

"""
#Statistical Summary"""

df.describe()

df[df.duplicated()].shape

"""#**Checking the data type of each attribute**"""

df.dtypes

"""#**Checking for missing data**"""

df.isnull().sum()

"""# **Checking if we have a balance dataset**"""

diagnosis = df.diagnosis.value_counts()
ax = sns.countplot(x='diagnosis', data=df)
plt.title('Class Distribution');
print(diagnosis)

"""# **Split attributes from the label and save them in two different variables.**"""

X = df.iloc[:, 2:31].values
Y = df.iloc[:,1].values

df.describe()

"""#**Correlation Between Attributes**"""

variables = df.iloc[:, 1:]
correlation = variables.corr('pearson')
plt.figure(figsize=(25,25), dpi= 100, facecolor='w', edgecolor='k')
ax = sns.heatmap(correlation.round(2), cmap='RdYlGn_r', linewidths=0.5, annot=True,
                 cbar=True, square=True, fmt='0.2f')
plt.yticks(rotation=0)
ax.tick_params(labelbottom=False, labeltop=True)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.title('Correlation matrix')

"""#**Skew of Univariate Distributions**"""

df.skew()

"""#**Univariate Plots**"""

df.hist(figsize=(20,15));

"""#**Pair Plot**

#**Splitting our data to training and testing set**

##### **One of the best plots to check the relationships between attributes and their distributions is pair plot.**
"""

data_visualization = df.iloc[:, [0, 1, 2, 3, 4, 14, 21, 22, 23, 24]]

sns.pairplot(data_visualization, hue='diagnosis')

"""### Summary

* Mean values of cell radius, perimeter, area, compactness, concavity
    and concave points can be used in classification of the cancer. Larger
    values of these parameters tends to show a correlation with malignant
    tumors.
* mean values of texture, smoothness, symmetry or fractual dimension
    does not show a particular preference of one diagnosis over the other. 
    
* In any of the histograms there are no noticeable large outliers that warrants further cleanup.

#PCA
####          In the ML area, data is the life-giving fuel of every model. Nowadays, we are dealing with some complex data, i.e. multi-dimensional data, which has lots of attributes and observations. In these kinds of data, there are too many variables to consider and it may affect the training of some ML models. Moreover, visualization and interpolation of these datasets are hard. To avoid these problems, it is better to use dimension reduction techniques before applying different ML models. Dimension reduction techniques reduce the feature space, so, it eases the processing time. Also, when we are dealing with fewer attributes, it is easier to make different plots and interpret them. There are many such techniques in the literature, but most of them fall in into two below categories:

####Feature selection: In which we reduce the feature space dimension by eliminating some attributes.
####Feature extraction: These techniques try to create new independent variables by combining old variables.

### SUPPORT VECTOR MACHINE(SVM)
"""

scaler = StandardScaler() 
X_scaled = pd.DataFrame(scaler.fit_transform(X))
X_scaled_drop = X_scaled.drop(X_scaled.columns[[2, 3, 12, 13, 22, 23]], axis=1)

pca = PCA(n_components=0.95) 
x_pca = pca.fit_transform(X_scaled_drop)
x_pca=pd.DataFrame(x_pca) 
print("Before PCA, X dataframe shape = ",X.shape,"\nAfter PCA, x_pca dataframe shape = ",x_pca.shape)

print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_.sum())

print(x_pca.shape)
print(Y.shape)

"""# We will split our data to training set(70%), testing set(30%). We need to split our data for model evaluation to know how good the model is."""

X_train, X_test, Y_train, Y_test = train_test_split(x_pca, Y, test_size=0.25, random_state=0)
svc = SVC()
svc.fit(X_train,Y_train)
y_pred =svc.predict(X_test)

print('X_train: ',X_train.shape)
print('X_test: ',X_test.shape)
print('y_train: ',Y_train.shape)
print('y_test: ',Y_test.shape)

"""#Metrics for Classification


1.  Accuracy 
2.  Confusion Matrix
3.  Classification Report
"""

cm = confusion_matrix(Y_test, y_pred) 
print("Confusion matrix:\n",cm) 
report = classification_report(Y_test, y_pred) 
print("Classification report:\n",report)

"""#**Classification Report**"""

plt.figure(figsize=(10,5))
sns.heatmap(confusion_matrix(Y_test, y_pred), annot=True, fmt='2.0f');

"""#CONCLUSION

**So finally we have built our classification model and we can see that SVM and kernal SVM gives the best results for our dataset.**
"""