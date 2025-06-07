## Homework

The goal of this homework is to create a simple training pipeline, use mlflow to track experiments and register best model, but use Mage for it.

We'll use [the same NYC taxi dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page), the **Yellow** taxi data for March, 2023. 

## Question 1. Select the Tool

You can use the same tool you used when completing the module,
or choose a different one for your homework.

What's the name of the orchestrator you chose?

**Kestra**


## Question 2. Version

What's the version of the orchestrator?

**v0.20.7**


## Question 3. Creating a pipeline

Let's read the March 2023 Yellow taxi trips data.

How many records did we load? 

- 3,003,766
- 3,203,766
- **3,403,766**
- 3,603,766

(Include a print statement in your code)

```bash
PS G:\Mon Drive\DataTalksClub\mlops-zoomcamp\cohorts\2025\03-orchestration> python preprocess.py
Rows after filtering: 3403766
```

Now with Kestra as an orchestrator and flow named *q3_count_rows*
```bash
id: q3_count_rows
namespace: mlops.zoomcamp

tasks:
  - id: extract
    type: io.kestra.plugin.core.http.Download
    uri: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet

  - id: count_rows
    type: io.kestra.plugin.scripts.python.Script
    containerImage: python:3.11-slim
    inputFiles:
      data.parquet: "{{ outputs.extract.uri }}"
    script: |
      import subprocess
      subprocess.run(["pip", "install", "pandas", "pyarrow"], check=True)

      import pandas as pd
      df = pd.read_parquet("data.parquet")
      print("Nombre de lignes :", len(df))
```
```bash
2025-06-04 17:30:15.161Nombre de lignes : 3403766
```


## Question 4. Data preparation

Let's continue with pipeline creation.

We will use the same logic for preparing the data we used previously. 

This is what we used (adjusted for yellow dataset):

```python
def read_dataframe(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df
```

Let's apply to the data we loaded in question 3. 

What's the size of the result? 

- 2,903,766
- 3,103,766
- **3,316,216**
- 3,503,766

```bash
id: q4_data_preparation
namespace: mlops.zoomcamp

tasks:
  - id: extract
    type: io.kestra.plugin.core.http.Download
    uri: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet

  - id: filter_duration
    type: io.kestra.plugin.scripts.python.Script
    containerImage: python:3.11-slim
    inputFiles:
      data.parquet: "{{ outputs.extract.uri }}"
    script: |
      import subprocess
      subprocess.run(["pip", "install", "pandas", "pyarrow"], check=True)

      import pandas as pd
      df = pd.read_parquet("data.parquet")
      df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
      df.duration = df.duration.dt.total_seconds() / 60
      df = df[(df.duration >= 1) & (df.duration <= 60)]
      categorical = ['PULocationID', 'DOLocationID']
      df[categorical] = df[categorical].astype(str)
      print("Nombre de lignes :", len(df))
```
```bash
2025-06-04 18:24:17.964filter_duration4ocg47y5sYKgrFNz81ToJl
Nombre de lignes : 3316216
```

## Question 5. Train a model

We will now train a linear regression model using the same code as in homework 1.

* Fit a dict vectorizer.
* Train a linear regression with default parameters.
* Use pick up and drop off locations separately, don't create a combination feature.

Let's now use it in the pipeline. We will need to create another transformation block, and return both the dict vectorizer and the model.

What's the intercept of the model? 

Hint: print the `intercept_` field in the code block

- 21.77
- 24.77
- 27.77
- 31.77

## Question 6. Register the model 

The model is trained, so let's save it with MLFlow.

Find the logged model, and find MLModel file. What's the size of the model? (`model_size_bytes` field):

* 14,534
* 9,534
* 4,534
* 1,534


## Submit the results

* Submit your results here: https://courses.datatalks.club/mlops-zoomcamp-2025/homework/hw3
* If your answer doesn't match options exactly, select the closest one.