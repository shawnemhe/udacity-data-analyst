#!/usr/bin/python

import sys
import pickle
import pandas as pd
import numpy as np

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

# Task 1: Select what features you'll use.
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".

# Based on the result of the grid search performed below
features_list = ['poi',
                 'exercised_stock_options',
                 'bonus',
                 'salary',
                 'from_this_person_to_poi_ratio',
                 'bonus_ratio',
                 'long_term_incentive']

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Convert the data_dict into a dataframe for easier manipulation
df = pd.DataFrame(data_dict).T

# Drop the email_address field
df.drop('email_address', axis=1, inplace=True)

# Convert the data types to numeric
df = df.applymap(float)

# Task 2: Remove outliers
# Outliers identified by screening for zscores above 3
df.drop(['TOTAL', 'THE TRAVEL AGENCY IN THE PARK'], inplace=True)
# Task 3: Create new feature(s)
df['from_this_person_to_poi_ratio'] = df['from_this_person_to_poi'] / df['from_messages']
df['bonus_ratio'] = df['bonus'] / df['salary']

# remove NaN and infinite values from the dataset
df.replace(np.inf, 0, inplace=True)
df.fillna(0, inplace=True)
# Store to my_dataset for easy export below.
#
my_dataset = df.T.to_dict()

# Task 4: Try a variety of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

# This list was handcrafted, removing items with greater than 60% zero values and pvalues lower than .05
# as measured by the f_classif function
features_of_interest = ['poi',
                        'bonus',
                        'exercised_stock_options',
                        'expenses',
                        'from_poi_to_this_person',
                        'long_term_incentive',
                        'other',
                        'restricted_stock',
                        'salary',
                        'shared_receipt_with_poi',
                        'bonus_ratio',
                        'from_this_person_to_poi_ratio']

# Extract features of interest and labels from the dataset for feature and model selection
data = featureFormat(my_dataset, features_of_interest, sort_keys=True)
labels, features = targetFeatureSplit(data)

# Build the pipeline for the grid search
pipe = Pipeline([
    ('scale', MinMaxScaler()),
    ('reduce_dim', SelectKBest(f_classif)),
    ('classifier', LinearSVC())
])

# Create an array for all k possibilities
k_features = np.arange(1, len(features_of_interest))

param_grid = [
    {
        'reduce_dim__k': k_features,
        'classifier': [LinearSVC(), KNeighborsClassifier(),
                       DecisionTreeClassifier(), AdaBoostClassifier()],
    }
]

grid = GridSearchCV(pipe, cv=StratifiedShuffleSplit(n_splits=50, random_state=35),
                    param_grid=param_grid, scoring='f1')

# These lines can be uncommented to reproduce grid search
# The best result was achieved using the top 6 features and a DecisionTreeClassifier
# grid.fit(features, labels)
# print grid.best_estimator_



# Task 5: Tune your classifier to achieve better than .3 precision and recall 
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info: 
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

# Extract features and labels from dataset for feature and model selection
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

tuning_pipe = Pipeline([
    ('scale', MinMaxScaler()),
    ('classify', DecisionTreeClassifier())
])

tuning_param_grid = [
    {
        'classify__class_weight': [None, 'balanced'],
        'classify__criterion': ['gini', 'entropy'],
        'classify__splitter': ['best', 'random'],
        'classify__max_depth': [None, 7, 6, 5, 4]
    }
]

tuning_grid = GridSearchCV(tuning_pipe, cv=StratifiedShuffleSplit(n_splits=50, random_state=35),
                           param_grid=tuning_param_grid, scoring='f1')

# tuning_grid.fit(features, labels)
# print tuning_grid.best_estimator_
# The above lines can be uncommented to rerun the gridsearch. The clf classifier below
# has been initialized using the best results

clf = DecisionTreeClassifier(
    class_weight='balanced',
    criterion='entropy',
    splitter='best',
    max_depth=4
)

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list[:6])
