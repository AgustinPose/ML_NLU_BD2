import google.generativeai as genai
import mysql.connector
conexion = mysql.connector.connect(
            host="mysql.reto-ucu.net",
            port=50006,
            user="xr_g6_admin",
            password="Bd2025!",
            database="XR_Grupo6"
        )

cursor = conexion.cursor()

def obtener_esquema():
    try:
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'XR_Grupo6'
            ORDER BY TABLE_NAME, ORDINAL_POSITION
        """)
        
        tablas = {}
        for tabla, columna, tipo in cursor.fetchall():
            columnas = tablas.setdefault(tabla, [])
            columnas.append(f"{columna} {tipo}")

        esquema = ["Tablas:"]
        for tabla, columnas in tablas.items():
            esquema.append(f"- {tabla} ({', '.join(columnas)})")
        
        return "\n".join(esquema)

    except Exception as e:
        return f"Error obteniendo esquema: {e}"


# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyD1cmFLbjjlwhRe0M8eZ6uOIBNm3ODd_5E" 
MODELO_GEMINI = "models/gemini-1.5-flash"

# --- INICIALIZACIÓN DEL MODELO ---
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODELO_GEMINI)

# --- CONSULTA EN LENGUAJE NATURAL ---
esquema = obtener_esquema()

consulta_natural = input("Ingrese su consulta en lenguaje natural: ")


prompt = f"""{esquema}
Teniendo en cuenta el esquema de tablas anterior, convertí la siguiente consulta en un SQL, 
y optimizándola, solo devolvé el SQL y nada más:
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
    cursor.execute(sql_clean)
    resultados = cursor.fetchall()
    print("\n📊 Resultados:")
    for fila in resultados:
        print(fila)
except Exception as e:
    print("\n❌ Error ejecutando SQL:", e)
