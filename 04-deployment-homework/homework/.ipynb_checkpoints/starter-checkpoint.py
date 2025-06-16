#!/usr/bin/env python
# coding: utf-8

# ## Homework
# 
# In this homework, we'll deploy the ride duration model in batch mode. Like in homework 1, we'll use the Yellow Taxi Trip Records dataset. 
# 
# You'll find the starter code in the [homework](homework) directory.

# In[1]:


get_ipython().system('pip freeze | grep scikit-learn')


# In[2]:


get_ipython().system('python -V')


# In[3]:


import pickle
import pandas as pd


# In[4]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[5]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[6]:


df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')


# In[7]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# ## Q1. Notebook
# 
# We'll start with the same notebook we ended up with in homework 1.
# We cleaned it a little bit and kept only the scoring part. You can find the initial notebook [here](homework/starter.ipynb).
# 
# Run this notebook for the March 2023 data.
# 
# What's the standard deviation of the predicted duration for this dataset?
# 
# * 1.24
# * **6.24**
# * 12.28
# * 18.28

# In[8]:


y_pred_std = round(y_pred.std(), 2)
print(f'the standard deviation of the predicted duration for this dataset is {y_pred_std}')


# ## Q2. Preparing the output
# 
# Like in the course videos, we want to prepare the dataframe with the output. 
# 
# First, let's create an artificial `ride_id` column:
# 
# ```python
# df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
# ```
# 
# Next, write the ride id and the predictions to a dataframe with results. 
# 
# Save it as parquet:
# 
# ```python
# df_result.to_parquet(
#     output_file,
#     engine='pyarrow',
#     compression=None,
#     index=False
# )
# ```
# 
# What's the size of the output file?
# 
# * 36M
# * 46M
# * 56M
# * 66M
# 
# __Note:__ Make sure you use the snippet above for saving the file. It should contain only these two columns. For this question, don't change the
# dtypes of the columns and use `pyarrow`, not `fastparquet`. 

# In[10]:


year = 2023
month = 3
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[11]:


df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred


# In[15]:


get_ipython().system('mkdir output')
output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'


# In[16]:


df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[17]:


get_ipython().system('ls -lh output')


# ## Q3. Creating the scoring script
# 
# Now let's turn the notebook into a script. 
# 
# Which command you need to execute for that?

# In[ ]:


get_ipython().system('jupyter nbconvert')

