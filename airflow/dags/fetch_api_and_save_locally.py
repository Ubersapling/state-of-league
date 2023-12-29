import json
import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from config import API_KEY

REGION = "oc1"
QUEUE = "RANKED_SOLO_5x5"
RANKS = ["EMERALD", "DIAMOND"]
DIVISIONS = ["I", "II", "III", "IV"]
PAGE = 1

# Define a DAG with appropriate configurations
dag = DAG(
    "riot_api_to_local_file",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None, # Set to manually trigger only
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    }
)

def current_timestamp():
    return datetime.strftime(datetime.now(), "%Y%m%dT%H:%M:%S")

def get_summoners_by_league(rank, division):
    headers = { "X-Riot-Token": API_KEY }
    endpoint_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/{QUEUE}/{rank}/{division}?page={PAGE}"
    response = requests.get(endpoint_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Define a function which fetches data from the Riot Games API and saves it locally in parquet format
def fetch_riot_api_and_save_locally(rank, division):
    output_file = f"../../data/bronze/summoners_{rank.lower()}_{division}_{current_timestamp()}.json"
    try:
        league_entries = get_summoners_by_league(rank, division)
        with open(output_file, "w+") as json_file:
            json.dump(league_entries, json_file, indent=4)
    except Exception as e:
        print(f"API call error: {e}")
        return None

# Define a task using the above function
for rank in RANKS:
    for division in DIVISIONS:
        fetch_and_save_task = PythonOperator(
            task_id=f"fetch_and_save_data_{rank}_{division}",
            python_callable=fetch_riot_api_and_save_locally,
            op_args=[rank, division],
            dag=dag
        )
