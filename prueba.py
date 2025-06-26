import spacy
from textblob import TextBlob
import mysql.connector

# 1. Cargar modelo spaCy (en inglés)
nlp = spacy.load("en_core_web_sm")

# 2. Texto en lenguaje natural (puede ser inglés o español, pero mejor inglés)
text = "Show me all users"  # Cambiálo por "Mostrar todos los usuarios" para español

# 3. Procesar texto con spaCy
doc = nlp(text)

print("🔍 ENTIDADES DETECTADAS:")
for ent in doc.ents:
    print(f" - {ent.text} ({ent.label_})")

# 4. Buscar intención de usuario (con reglas simples)
get_all_users = False
for token in doc:
    if token.lemma_ in ["user", "usuario"]:
        get_all_users = True

# 5. Armar SQL según la intención detectada
if get_all_users:
    sql = "SELECT * FROM Usuario;"
else:
    sql = "SELECT * FROM Usuario;"  # Fallback

print("\n⚙️ Consulta SQL generada:")
print(sql)

# 6. Ejecutar el SQL en la base de datos
try:
    conexion = mysql.connector.connect(
        host="mysql.reto-ucu.net",
        port=50006,
        user="xr_g6_admin",
        password="Bd2025!",
        database="XR_Grupo6"
    )
    cursor = conexion.cursor()
    cursor.execute(sql)
    resultados = cursor.fetchall()
    print("\n📊 Resultados:")
    for fila in resultados:
        print(fila)
    cursor.close()
    conexion.close()
except Exception as e:
    print("\n❌ Error ejecutando SQL:", e)
