import pandas as pd
from fpdf import FPDF
from pathlib import Path
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
# Esto asegura que el script funcione sin importar desde dónde lo ejecutes
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / 'data' / 'raw' / 'operaciones_logisticas5.xlsx'
OUTPUT_DIR = BASE_DIR / 'reports' / 'ejecutivo'
OUTPUT_PATH = OUTPUT_DIR / f"Reporte_Ejecutivo_{datetime.now().strftime('%Y%m%d')}.pdf"

# Crear carpeta de salida si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- CLASE PDF PERSONALIZADA ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte Ejecutivo de Operaciones Logísticas', 0, 1, 'C')
        self.ln(5)
        # Línea decorativa
        self.set_draw_color(0, 0, 128)
        self.line(10, 20, 200, 20)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def safe_text(self, text):
        # Manejo seguro de caracteres especiales (ñ, tildes)
        if not isinstance(text, str):
            text = str(text)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, self.safe_text(title), 0, 1, 'L', 1)
        self.ln(4)

    def add_kpi_card(self, label, value):
        self.set_font('Arial', 'B', 10)
        self.cell(90, 10, self.safe_text(f"{label}:"), 0, 0)
        self.set_font('Arial', '', 10)
        self.cell(0, 10, self.safe_text(str(value)), 0, 1, 'R')

# --- CARGA Y PROCESAMIENTO DE DATOS ---
print("🔄 Cargando datos desde Excel...")
try:
    df = pd.read_excel(DATA_PATH)
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo en {DATA_PATH}")
    print("✅ Asegúrate de que 'operaciones_logisticas5.xlsx' esté en 'data/raw/'")
    exit()

# Cálculo de KPIs
total_ops = len(df)
total_ingreso = df['Ingreso'].sum()
total_utilidad = df['Utilidad'].sum()
margen = (total_utilidad / total_ingreso * 100) if total_ingreso > 0 else 0
sla_cumplido = len(df[df['Cumple_SLA'] == 'Sí'])
sla_porcentaje = (sla_cumplido / total_ops * 100) if total_ops > 0 else 0

# Top 5 Rutas por Utilidad
top_rutas = df.groupby('Ruta')['Utilidad'].sum().nlargest(5).reset_index()

# Top 5 Conductores
top_conductores = df.groupby('Conductor')['Utilidad'].sum().nlargest(5).reset_index()

# --- GENERACIÓN DEL PDF ---
print("📄 Generando PDF...")
pdf = PDFReport()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# 1. Resumen General
pdf.chapter_title('1. RESUMEN GENERAL DE OPERACIONES')
pdf.add_kpi_card('Total Operaciones', f"{total_ops:,}")
pdf.add_kpi_card('Ingreso Total', f"S/ {total_ingreso:,.2f}")
pdf.add_kpi_card('Utilidad Total', f"S/ {total_utilidad:,.2f}")
pdf.add_kpi_card('Margen Promedio', f"{margen:.2f}%")
pdf.add_kpi_card('Cumplimiento SLA', f"{sla_porcentaje:.2f}%")
pdf.ln(5)

# 2. Top Rutas
pdf.chapter_title('2. TOP 5 RUTAS MÁS RENTABLES')
pdf.set_font('Arial', 'B', 9)
pdf.cell(100, 8, 'Ruta', 1)
pdf.cell(90, 8, 'Utilidad Generada', 1, 1, 'R')
pdf.set_font('Arial', '', 9)
for _, row in top_rutas.iterrows():
    pdf.cell(100, 8, pdf.safe_text(row['Ruta']), 1)
    pdf.cell(90, 8, f"S/ {row['Utilidad']:,.2f}", 1, 1, 'R')
pdf.ln(5)

# 3. Top Conductores
pdf.chapter_title('3. TOP 5 CONDUCTORES POR UTILIDAD')
pdf.set_font('Arial', 'B', 9)
pdf.cell(100, 8, 'Conductor', 1)
pdf.cell(90, 8, 'Utilidad Generada', 1, 1, 'R')
pdf.set_font('Arial', '', 9)
for _, row in top_conductores.iterrows():
    pdf.cell(100, 8, pdf.safe_text(row['Conductor']), 1)
    pdf.cell(90, 8, f"S/ {row['Utilidad']:,.2f}", 1, 1, 'R')
pdf.ln(5)

# 4. Recomendaciones
pdf.chapter_title('4. CONCLUSIONES Y RECOMENDACIONES')
pdf.set_font('Arial', '', 10)
recomendaciones = [
    f"- El margen actual es del {margen:.2f}%, lo cual es saludable.",
    f"- El cumplimiento de SLA es del {sla_porcentaje:.2f}%. " + 
    ("Se requiere atención urgente." if sla_porcentaje < 80 else "Se mantiene dentro del estándar."),
    "- Enfocar recursos en las rutas top identificadas.",
    "- Revisar performance de conductores fuera del top 5."
]
for rec in recomendaciones:
    pdf.multi_cell(0, 7, pdf.safe_text(rec))

# Guardar
pdf.output(str(OUTPUT_PATH))
print(f"✅ ¡Éxito! PDF guardado en: {OUTPUT_PATH}")


