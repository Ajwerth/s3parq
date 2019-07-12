from s3parq.session_helper import SessionHelper
from sqlalchemy import Column, Integer, String
from s3parq.redshift_naming_helper import RedshiftNamingHelper
import logging

logger = logging.getLogger(__name__)


def schema_name_validator(schema_name: str, database: str):
    schema_validated = RedshiftNamingHelper().validate_name(schema_name)
    database_validated = RedshiftNamingHelper().validate_name(database)
    if not schema_validated[0] and not database_validated[0]:
        raise ValueError(schema_validated[1], database_validated[0])



def create_schema(schema_name: str, database: str, iam_role: str, session_helper: SessionHelper):
    schema_name_validator(schema_name, database)
    with session_helper.db_session_scope() as scope:
        new_schema_query = f"CREATE EXTERNAL SCHEMA IF NOT EXISTS {schema_name} \
                FROM DATA CATALOG \
                database '{database}' \
                iam_role '{iam_role}' \
                CREATE EXTERNAL DATABASE IF NOT EXISTS;"

        logger.info(f'Running query to create schema: {new_schema_query}')
        scope.execute(new_schema_query)



#     query = f"ALTER TABLE {schema}.{table} \
#               ADD PARTITION ({' ,'.join(formatted_partitions)}) \
#               LOCATION 's3://{bucket}/{path_to_data}';"
