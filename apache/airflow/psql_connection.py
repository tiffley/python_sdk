from airflow.utils.session import provide_session
from airflow import models
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
# from airflow.models.base import Base
from airflow import settings
from airflow.configuration import conf  

def create_new_engine():
    engine_args = settings.prepare_engine_args()
    SQL_ALCHEMY_CONN = conf.get("database", "SQL_ALCHEMY_CONN")
    return create_engine(SQL_ALCHEMY_CONN, **engine_args)

Base = declarative_base()
class SinkConCatalog(Base):
    __tablename__ = "kafkaSinkConCatalog"
    name = Column(String, primary_key=True)
    path = Column(String)
    file_format = Column(String)
    offsetColumnName = Column(String)

@provide_session
def update_db(record, engine, session=None):
    Base.metadata.create_all(bind=engine)
    session.add(record)
    session.commit()

@provide_session
def check_db(engine=None, session=None):
    print('--------------')
    res = session.query(SinkConCatalog).all()
    print(res)
    print('--------------')
    print(engine.table_names())


# 3. compare and update DB
# engine = create_new_engine()
# record = SinkConCatalog(**di_con_conf)
# print(record)
# update_db(record, engine)

# check_db(engine)
