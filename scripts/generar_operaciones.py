import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Crear carpeta data si no existe
os.makedirs("data", exist_ok=True)

NUM_REGISTROS = 5000
fecha_inicio = datetime(2025, 1, 1)

clientes = [f"Cliente_{i}" for i in range(1, 41)]
rutas = ["Ruta Norte", "Ruta Centro", "Ruta Sur", "Ruta Express"]
ciudades = ["Lima", "Arequipa", "Trujillo", "Cusco", "Piura"]
conductores = ["Carlos", "Miguel", "José", "Luis", "Andrés"]
vehiculos = ["Camión A", "Camión B", "Furgón 1", "Furgón 2"]
tipos_carga = ["General", "Frágil", "Refrigerada", "Pesada"]

datos = []

for i in range(1, NUM_REGISTROS + 1):

    fecha_envio = fecha_inicio + timedelta(days=random.randint(0, 365))
    tiempo_estimado = random.randint(4, 72)  # horas estimadas
    retraso = random.choice([0, 0, 0, 2, 4, 6])  # más probabilidad de estar a tiempo

    fecha_entrega = fecha_envio + timedelta(hours=tiempo_estimado + retraso)

    cumple_sla = "Sí" if retraso == 0 else "No"
    estado = "A Tiempo" if retraso == 0 else "Retrasado"

    peso = random.randint(100, 2000)
    costo_operacion = random.randint(500, 5000)
    ingreso = costo_operacion + random.randint(500, 4000)
    utilidad = ingreso - costo_operacion

    datos.append([
        i,
        fecha_envio,
        fecha_entrega,
        random.choice(clientes),
        random.choice(rutas),
        random.choice(ciudades),
        random.choice(ciudades),
        random.choice(conductores),
        random.choice(vehiculos),
        random.choice(tipos_carga),
        peso,
        costo_operacion,
        ingreso,
        utilidad,
        tiempo_estimado + retraso,
        estado,
        cumple_sla
    ])

columnas = [
    "ID_Operacion",
    "Fecha_Envio",
    "Fecha_Entrega",
    "Cliente",
    "Ruta",
    "Ciudad_Origen",
    "Ciudad_Destino",
    "Conductor",
    "Vehiculo",
    "Tipo_Carga",
    "Peso_kg",
    "Costo_Operacion",
    "Ingreso",
    "Utilidad",
    "Tiempo_Entrega_Horas",
    "Estado",
    "Cumple_SLA"
]

df = pd.DataFrame(datos, columns=columnas)

ruta_archivo = "data/operaciones_logisticas.xlsx"
df.to_excel(ruta_archivo, index=False)

print("✅ Archivo logístico generado correctamente en /data/operaciones_logisticas.xlsx")