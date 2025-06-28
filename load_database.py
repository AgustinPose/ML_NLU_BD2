import pandas as pd
import mysql.connector

# --- Conexión a la base de datos ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",
    database="books_demo"
)
cursor = conn.cursor()

# --- LIBROS ---
print("📚 Cargando libros...")
libros = pd.read_csv("books_ds/Books.csv", sep=",", encoding="latin1", low_memory=False)
libros = libros[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]

# Filtrar registros inválidos: año no numérico o año fuera de rango
libros = libros[libros['Year-Of-Publication'].apply(lambda x: str(x).isdigit())]
libros['Year-Of-Publication'] = libros['Year-Of-Publication'].astype(int)
libros = libros[libros['Year-Of-Publication'].between(1000, 2025)]
libros = libros.dropna()

libros_tuplas = [
    (
        str(row['ISBN']).strip(),
        str(row['Book-Title']).strip(),
        str(row['Book-Author']).strip(),
        int(row['Year-Of-Publication']),
        str(row['Publisher']).strip()
    )
    for _, row in libros.iterrows()
]

cursor.executemany("""
    INSERT IGNORE INTO libros (isbn, titulo, autor, anio_publicacion, editorial)
    VALUES (%s, %s, %s, %s, %s)
""", libros_tuplas)
conn.commit()
print(f"✅ Libros insertados: {len(libros_tuplas)}")

# --- USUARIOS ---
print("👤 Cargando usuarios...")
usuarios = pd.read_csv("books_ds/Users.csv", sep=",", encoding="latin1", low_memory=False)
usuarios = usuarios[['User-ID', 'Location', 'Age']]

# Eliminar filas con edad nula o no numérica
usuarios = usuarios[usuarios['Age'].apply(lambda x: pd.notnull(x) and str(x).isdigit())]
usuarios['Age'] = usuarios['Age'].astype(int)
usuarios = usuarios[usuarios['Age'].between(5, 120)]

# Eliminar nulos en Location y extraer país
usuarios = usuarios.dropna(subset=['Location'])
usuarios['pais'] = usuarios['Location'].apply(lambda loc: loc.split(",")[-1].strip())

usuarios_tuplas = [
    (
        int(row['User-ID']),
        str(row['Location']).strip(),
        str(row['pais']),
        int(row['Age'])
    )
    for _, row in usuarios.iterrows()
]

cursor.executemany("""
    INSERT IGNORE INTO usuarios (id_usuario, localidad, pais, edad)
    VALUES (%s, %s, %s, %s)
""", usuarios_tuplas)
conn.commit()
print(f"✅ Usuarios insertados: {len(usuarios_tuplas)}")

# --- VALORACIONES ---
print("⭐ Cargando valoraciones...")
ratings = pd.read_csv("books_ds/Ratings.csv", sep=",", encoding="latin1", low_memory=False)
ratings = ratings[['User-ID', 'ISBN', 'Book-Rating']]
ratings = ratings.dropna()

# Asegurar que todos los valores sean numéricos
ratings = ratings[
    ratings['User-ID'].apply(lambda x: str(x).isdigit()) &
    ratings['Book-Rating'].apply(lambda x: str(x).isdigit())
]

ratings['User-ID'] = ratings['User-ID'].astype(int)
ratings['Book-Rating'] = ratings['Book-Rating'].astype(int)

ratings_tuplas = [
    (
        int(row['User-ID']),
        str(row['ISBN']).strip(),
        int(row['Book-Rating'])
    )
    for _, row in ratings.iterrows()
]

cursor.executemany("""
    INSERT IGNORE INTO valoraciones (id_usuario, isbn, puntuacion)
    VALUES (%s, %s, %s)
""", ratings_tuplas)
conn.commit()
print(f"✅ Valoraciones insertadas: {len(ratings_tuplas)}")

# --- Cierre ---
cursor.close()
conn.close()
print("🏁 Finalizado con éxito.")