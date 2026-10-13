from cosmos.config import ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos.constants import InvocationMode
from pathlib import Path

DBT_CONFIG = ProfileConfig(
    profile_name='retail',
    target_name='dev',
    profiles_yml_filepath=Path('/usr/local/airflow/include/dbt/profiles.yml')
)

DBT_PROJECT_CONFIG = ProjectConfig(
    dbt_project_path='/usr/local/airflow/include/dbt/',
)

# dbt nie jest zainstalowany w środowisku Airflow, tylko w dbt_venv (Dockerfile). Bez tej ścieżki
# Cosmos szukałby polecenia `dbt` w PATH i padał zarówno przy wykonaniu tasków, jak i przy
# parsowaniu DAG-a (LoadMode.DBT_LS odpala `dbt ls` już przy imporcie).
DBT_EXECUTABLE_PATH = '/usr/local/airflow/dbt_venv/bin/dbt'

# SUBPROCESS, nie domyślny DBT_RUNNER: DBT_RUNNER importuje dbt jako bibliotekę w środowisku Airflow,
# a tam dbt celowo nie ma. Podproces odpala binarkę z dbt_venv. Ta sama wartość idzie do RenderConfig
# w dags/retail.py, bo parsowanie (dbt ls) ma w Cosmos osobny, domyślnie też DBT_RUNNER, tryb.
DBT_INVOCATION_MODE = InvocationMode.SUBPROCESS

DBT_EXECUTION_CONFIG = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
    invocation_mode=DBT_INVOCATION_MODE,
)