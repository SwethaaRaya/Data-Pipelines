from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from udacity.common.final_project_sql_statements import SqlQueries

default_args = {
    'depends_on_past': False,
    'owner': 'udacity',
    'start_date': pendulum.now(),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)

def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    end_operator = DummyOperator(task_id='End_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_events",
        s3_bucket="raya-swethaa",
        s3_key="log-data/2018/",
        json ="log_json_path.json"
    )


    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_songs",
        s3_bucket="raya-swethaa",
        s3_key="song-data/",
        json="auto" 
    )


    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id="redshift",
        table="songplays",
        sql=SqlQueries.songplay_table_insert 
    )


    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id="redshift",
        table="users",
        sql=SqlQueries.user_table_insert
    )


    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id="redshift",
        table="songs",
        sql=SqlQueries.song_table_insert
    )


    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id="redshift",
        table="artists",
        sql=SqlQueries.artist_table_insert
    )


    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id="redshift",
        table="time",
        sql=SqlQueries.time_table_insert
    )


    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id="redshift",
        table_list=['songplays','songs','artists','time','users']
    )

    start_operator >> [stage_events_to_redshift,stage_songs_to_redshift] >> load_songplays_table
    load_songplays_table >> [load_user_dimension_table,load_song_dimension_table,load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks 
    run_quality_checks >> end_operator
    
final_project_dag = final_project()
