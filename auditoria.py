import sqlite3
import pandas as pd

conn = sqlite3.connect('especialidades_fae.db')
df = pd.read_sql_query("SELECT * FROM resultados_finales", conn)
print(df.head(20)) # Ver los primeros 20 asignados (mejores antigüedades)
conn.close()