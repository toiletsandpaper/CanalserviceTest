"""Database controller
"""
import pandas as pd
from sqlalchemy import create_engine, exc
import settings

def dump_to_sql(df: pd.DataFrame, echo: bool = settings.SQL_ECHO) -> None:
    """Dumps data from pandas dataframe to chosen database

    Args:
        df (pd.DataFrame): dataframe to be dumped
    """    
    try:
        # I wish I can know do you need primary key or not
        engine = create_engine(settings.DATABASE, echo=echo)
        df.to_sql('orders', engine, if_exists='replace', index=False)
    except exc.SQLAlchemyError as err:
        print(f'error: {err}')
        return
