from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://postgres:ruking29@localhost/se4g')
df = pd.read_csv('C:/Users/Lenovo/user_server/env/BIKOD_2/data/bike.csv')
df.to_sql('bike', engine, if_exists='replace')
