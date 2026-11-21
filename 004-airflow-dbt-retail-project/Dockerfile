# Astro Runtime 12.12.0 = Airflow 2.10.5, Python 3.12, protobuf 5.29.6 (łatka na CVE-2022-1941,
# CVE-2025-4565, CVE-2026-0994). Na 8.8.0 łatki nie dało się zainstalować: preinstalowany
# apache-airflow-providers-google 10.0.0 wymaga protobuf<=3.20.0, a biblioteki google-cloud-* <4.0.
# Zostajemy na Airflow 2 - astro-sdk (aql.load_file w dags/retail.py) nie wspiera Airflow 3.
FROM quay.io/astronomer/astro-runtime:12.12.0

# Soda w osobnym venv: jej zależności (google-cloud-*) nie mieszają się z Airflow.
# 3.5.6, bo 3.0.45 nie instaluje się na Pythonie 3.12. Bez soda-core-scientific: wymaga pandas<2.0,
# który nie ma kół dla 3.12, a checki w include/soda/checks używają tylko schema, missing_count
# i failed rows - funkcji z soda-core. Scientific potrzebny dopiero przy checkach anomaly/distribution.
# setuptools: soda-core importuje distutils, usunięte z biblioteki standardowej w Pythonie 3.12 -
# setuptools dostarcza jego zamiennik.
RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir soda-core-bigquery==3.5.6 setuptools && deactivate

# dbt w osobnym venv - Cosmos woła go przez ExecutionConfig (include/dbt/cosmos_config.py).
# dbt w środowisku Airflow kolidowałby z jego przypiętymi zależnościami. 1.12.1, bo dbt 1.5 nie wspiera Pythona 3.12.
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery==1.12.1 && deactivate
