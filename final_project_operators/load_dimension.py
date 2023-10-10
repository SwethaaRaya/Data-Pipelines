from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql="",
                 delete_load = False,
                 table="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql=sql
        self.table=table
        self.delete_load = delete_load

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.delete_load:
            self.log.info(f"Delete load operation set to TRUE. Running delete statement on table {self.table}")
            redshift_hook.run(f"DELETE FROM {self.table}")
        self.log.info(f"Running query to load data into Dimension Table {self.table}")
        load_fact_sql="INSERT INTO {} ({})".format(self.table,self.sql)
        self.log.info('LoadDimensionOperator loading Dimensions table')
        redshift.run(load_fact_sql)
