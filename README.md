# State of League Data Estate

## Apache Airflow Setup

1. Set the variable for the directory in which Airflow-related files will be stored using
``export AIRFLOW_HOME=~/airflow``.

2. Install Airflow using the given constraints file
```python
AIRFLOW_VERSION=2.8.0

# Extract the version of Python you have installed.
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.8.0 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.8.0/constraints-3.8.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

2. Install the kubernetes python library using ``pip install kubernetes``.

3. Run ``airflow db migrate`` to set up the airflow database.

4. Create an admin user to access the Airflow webserver UI.
```
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```

5. In separate terminals, run the webserver using ``airflow webserver --port 8080`` and the scheduler using ``airflow scheduler``.