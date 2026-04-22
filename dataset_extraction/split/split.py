'''
This file was made to preform quick split from contest data
currently configured for contest combining and splitting contest494,495,496
See into /Notebooks/split.ipynb for detailed overview
Make sure all necessary files are present before running this file

command to run this file from project root : python -m  dataset_extraction.split.split
'''
import config
import pandas as pd
pd.set_option('display.max_columns', None)
path_494= config.ROOT_DIR / "dataset"/ 'contest_494' /'weekly_contest494.csv'
path_495= config.ROOT_DIR / "dataset"/ 'contest_495' /'weekly_contest495.csv'
path_496= config.ROOT_DIR / "dataset"/ 'contest_496' /'weekly_contest496.csv'

df_494=pd.read_csv(path_494)
df_495=pd.read_csv(path_495)
df_496=pd.read_csv(path_496)
# print('OK')

df1=df_494.copy()
df2=df_495.copy()
df3=df_496.copy()
for i in range(1,5):
    df1[f'Q{i}FailCnt'] = df1[f'Q{i}FailCnt'].fillna(0).astype('int64')
    df1[f'Q{i}TimeStamp'] = df1[f'Q{i}TimeStamp'].fillna(0).astype('int64')
    df2[f'Q{i}FailCnt'] = df2[f'Q{i}FailCnt'].fillna(0).astype('int64')
    df2[f'Q{i}TimeStamp'] = df2[f'Q{i}TimeStamp'].fillna(0).astype('int64')
    df3[f'Q{i}FailCnt'] = df3[f'Q{i}FailCnt'].fillna(0).astype('int64')
    df3[f'Q{i}TimeStamp'] = df3[f'Q{i}TimeStamp'].fillna(0).astype('int64')

df1['CurrRating'] = df1['CurrRating'].astype('int64')
df2['CurrRating'] = df2['CurrRating'].astype('int64')
df3['CurrRating'] = df3['CurrRating'].astype('int64')

from sklearn.model_selection import train_test_split

# 60 row from each contest should be used
X1_train, X1_test = train_test_split(
    df1,
    test_size=0.0065, #will give 60 rows
    random_state=41
)

X2_train, X2_test = train_test_split(
    df2,
    test_size=0.0063, #will give 60 rows
    random_state=41
)

X3_train, X3_test = train_test_split(
    df3,
    test_size=0.0063, #will give 60 rows
    random_state=41
)

X1_test['contest_id']=1
X2_test['contest_id']=2
X3_test['contest_id']=3
X_test=pd.concat([X1_test,X2_test,X3_test],ignore_index=True) #combine all test dataset into 1

import csv
X_test.to_csv(config.ROOT_DIR/'dataset'/'testing_data.csv',index=False,quoting=csv.QUOTE_ALL)

X1_train['contest_id']=1
X2_train['contest_id']=2
X3_train['contest_id']=3
X_train=pd.concat([X1_train,X2_train,X3_train],ignore_index=True) #combine all test dataset into 1
X_train_copy=X_train.copy()
dups = X_train_copy[X_train_copy.duplicated(subset='User_slug', keep=False)].sort_values(by='User_slug')
X_train_clean=X_train.drop_duplicates(subset='User_slug', keep='last') #new dataframe will be creater by drop_duplicates unlike df2= df which creates new reference only not object

X_train_clean = X_train_clean[~X_train_clean['User_slug'].isin(X_test['User_slug'])] #removed overlap of training people which were present in testing via other contest
X_train_clean.to_csv(config.ROOT_DIR/'dataset'/'training_data_final.csv',index=False,quoting=csv.QUOTE_ALL) 