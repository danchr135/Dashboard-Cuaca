import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('data/data_cuaca.csv')
print(f"Berhasil membaca {len(df)} baris data dari CSV.")

db_user = 'root'
db_password = ''
db_host = 'localhost'
db_name = 'database_cuaca'

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

print("Sedang mengirim data ke phpMyAdmin...")
df.to_sql('staging_weather', con=engine, if_exists='append', index=False)
print("Sukses! Data berhasil dimuat ke tabel staging_weather di phpMyAdmin.")