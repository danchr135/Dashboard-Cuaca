import pandas as pd
from sqlalchemy import create_engine

db_user = 'root'
db_password = ''
db_host = 'localhost'
db_name = 'dataset_cuaca'

engine = create_engine(
    f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
)


def validate_data():
    print("=== DATA QUALITY VALIDATION ===")
    df = pd.read_sql(
        "SELECT * FROM summary_wheater",
        con=engine
    )
    print(f"\nJumlah baris: {len(df)}")

    if len(df) > 0:
        print("✓ Data tidak kosong")
    else:
        print("✗ Data kosong")

    print("\n=== NULL CHECK ===")

    null_count = df.isnull().sum()

    print(null_count)

    if null_count.sum() == 0:
        print("✓ Tidak ditemukan NULL")
    else:
        print("✗ Masih terdapat NULL")

    print("\n=== DUPLICATE CHECK ===")

    duplicate_count = df.duplicated().sum()

    print(f"Jumlah duplicate: {duplicate_count}")

    if duplicate_count == 0:
        print("✓ Tidak ditemukan duplicate")
    else:
        print("✗ Ditemukan duplicate")

    print("\n=== VALIDATION SELESAI ===")


if __name__ == "__main__":
    validate_data()