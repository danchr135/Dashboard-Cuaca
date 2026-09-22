import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2  # Mengganti mysql.connector ke psycopg2
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Dashboard Cuaca Harian',
    page_icon='🌤️',
    layout='wide',
)

st.title('Dashboard Analisis Cuaca Harian')
st.caption('Pantau perubahan suhu, tekanan udara, dan kecepatan angin dari waktu ke waktu.')


@st.cache_data
def load_data():
    try:
        # Dipaksa langsung mengambil data dari [postgres] di rahasia cloud
        connection_config = st.secrets["postgres"]
        
        # Menyambungkan menggunakan driver psycopg2 ke Aiven Cloud
        conn = psycopg2.connect(
            host=connection_config['host'],
            port=int(connection_config['port']),
            database=connection_config['dbname'],
            user=connection_config['user'],
            password=connection_config['password'],
            sslmode=connection_config.get('sslmode', 'no-verify')
        )
    except Exception as error:
        st.error(
            f'Gagal terhubung ke Aiven Cloud. Pastikan kolom Secrets di Streamlit Cloud '
            f'sudah Anda isi dengan benar dan klik Save. Detail kendala: {error}'
        )
        st.stop()

    # Eksekusi query mengambil data cuaca Anda
    query = (
        'SELECT tanggal, rata_rata_suhu, rata_rata_tekanan, '
        'rekor_angin_terkencang FROM public.summary_wheater'
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df


df = load_data()
df['tanggal'] = pd.to_datetime(df['tanggal'])
numeric_columns = ['rata_rata_suhu', 'rata_rata_tekanan', 'rekor_angin_terkencang']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
df['rata_rata_suhu'] = (df['rata_rata_suhu'] - 32) * 5 / 9
df = df.dropna(subset=['tanggal']).sort_values('tanggal')

latest = df.iloc[-1]
metric_columns = st.columns(3)
metric_columns[0].metric('Rata-rata suhu terakhir', f"{latest['rata_rata_suhu']:.2f} °C")
metric_columns[1].metric('Tekanan terakhir', f"{latest['rata_rata_tekanan']:.2f}")
metric_columns[2].metric('Angin terkuat terakhir', f"{latest['rekor_angin_terkencang']:.2f}")

st.subheader('Tren Cuaca')

def make_chart(column, title, color, ylabel):
    figure, axis = plt.subplots(figsize=(10, 3.5))
    figure.patch.set_facecolor('#f8fafc')
    axis.set_facecolor('#f8fafc')
    axis.plot(df['tanggal'], df[column], color=color, linewidth=2)
    axis.fill_between(df['tanggal'], df[column], color=color, alpha=0.12)
    axis.set_title(title, loc='left', fontsize=14, fontweight='bold', pad=12)
    axis.set_ylabel(ylabel)
    axis.grid(axis='y', color='#cbd5e1', alpha=0.45, linewidth=0.8)
    axis.spines[['top', 'right']].set_visible(False)
    axis.spines[['left', 'bottom']].set_color('#cbd5e1')
    locator = mdates.AutoDateLocator()
    axis.xaxis.set_major_locator(locator)
    axis.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    figure.tight_layout()
    return figure

temperature_column, pressure_column = st.columns(2)
with temperature_column:
    st.pyplot(
        make_chart('rata_rata_suhu', 'Rata-rata Suhu Harian', '#f97316', 'Suhu (°C)'),
        use_container_width=True,
    )

with pressure_column:
    st.pyplot(
        make_chart('rata_rata_tekanan', 'Rata-rata Tekanan Udara', '#2563eb', 'Tekanan'),
        use_container_width=True,
    )

st.pyplot(
    make_chart(
        'rekor_angin_terkencang',
        'Rekor Angin Terkencang',
        '#0f766e',
        'Kecepatan angin',
    ),
    use_container_width=True,
)

with st.expander('Lihat data ringkasan'):
    st.dataframe(df, use_container_width=True, hide_index=True)