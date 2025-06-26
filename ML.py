import google.generativeai as genai
import mysql.connector

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyDBWpMtDVZ8icLNNeP9uQBT0AkRwq1BMVA"  # Pegá tu API KEY de Gemini aquí
MODELO_GEMINI = "models/gemini-1.5-flash"  # O prueba con "models/gemini-2.5-pro" si querés

# --- INICIALIZACIÓN DEL MODELO ---
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODELO_GEMINI)

# --- CONSULTA EN LENGUAJE NATURAL ---
esquema = """
Tablas:
- Ciudadano (ci, nombre, apellido, serie_credencial, nro_circuito)
- Circuito (nro, es_accesible, id_establecimiento, es_cerrado, se_abrio)
- Establecimiento (id, nombre, tipo, direccion, id_zona)
- Zona (id, nombre, id_ciudad)
- Ciudad (id, nombre, id_departamento)
"""

consulta_natural = "Dame los nombres y apellidos de los ciudadanos que votan en circuitos accesibles de la ciudad de Montevideo."


prompt = f"""{esquema}
Convertí la siguiente consulta en SQL, solo devolvé el SQL y nada más:
{consulta_natural}
"""

# --- MOSTRAR INFO DE ENTRADA ---
print("\n📝 Esquema usado:")
print(esquema)
print("\n💬 Consulta en lenguaje natural:")
print(consulta_natural)

# --- OBTENER SQL DESDE GEMINI ---
response = model.generate_content(prompt)
sql = response.text.strip()

# --- LIMPIEZA: ELIMINAR ```sql Y ``` SI LOS HUBIERA ---
lines = [line for line in sql.splitlines() if not line.strip().startswith("```")]
sql_clean = "\n".join(lines).strip()

print("\n🧠 SQL generado para ejecutar:")
print(sql_clean)

# --- EJECUTAR SQL EN TU BASE DE DATOS ---
try:
    conexion = mysql.connector.connect(
        host="mysql.reto-ucu.net",
        port=50006,
        user="xr_g6_admin",
        password="Bd2025!",
        database="XR_Grupo6"
    )
    cursor = conexion.cursor()
    cursor.execute(sql_clean)
    resultados = cursor.fetchall()
    print("\n📊 Resultados:")
    for fila in resultados:
        print(fila)
    cursor.close()
    conexion.close()
except Exception as e:
    print("\n❌ Error ejecutando SQL:", e)
