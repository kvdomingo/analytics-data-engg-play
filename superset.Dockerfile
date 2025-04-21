FROM apache/superset:4.1.2

USER root

RUN pip install --no-cache-dir  \
    duckdb==1.1.3  \
    duckdb_engine==0.17.0 \
    prophet==1.1.6  \
    psycopg2-binary==2.9.10

USER superset
