import pandas as pd
import xlsxwriter

# Nombre del archivo final
filename = 'MENU_MASTER_FINAL.xlsx'

# Crear el escritor de Excel
workbook = xlsxwriter.Workbook(filename)

# --- FORMATOS VISUALES ---
header_fmt = workbook.add_format({
    'bold': True, 'font_color': 'white', 'bg_color': '#003366', # Azul corporativo
    'border': 1, 'align': 'center', 'valign': 'vcenter'
})
text_fmt = workbook.add_format({'text_wrap': True, 'valign': 'top'})
price_fmt = workbook.add_format({'num_format': '0.00', 'align': 'right'})
locked_fmt = workbook.add_format({'bg_color': '#E0E0E0', 'border': 1}) # Para columnas que no aplican

# --- CREAR PESTAÑAS ---
ws_comida = workbook.add_worksheet('COMIDA')
ws_bebida = workbook.add_worksheet('BEBIDAS')
ws_config = workbook.add_worksheet('CONFIGURACION') # Aquí guardamos las listas para los desplegables

# ==========================================
# 1. PESTAÑA CONFIGURACIÓN (Listas Maestras)
# ==========================================
ws_config.write('A1', 'LISTA CATEGORIAS COMIDA', header_fmt)
ws_config.write_column('A2', ['ENTRANTES', 'PRINCIPALES', 'POSTRES', 'PARA COMPARTIR'])

ws_config.write('B1', 'LISTA CATEGORIAS BEBIDA', header_fmt)
ws_config.write_column('B2', ['VINOS', 'COCTELES', 'CERVEZAS', 'REFRESCOS', 'LICORES', 'CAFES'])

ws_config.write('C1', 'LISTA SUBCATEGORIAS (Títulos)', header_fmt)
ws_config.write_column('C2', ['GENERICO', 'D.O. RIOJA', 'D.O. RIBERA', 'D.O. VALENCIA', 'RON', 'GINEBRA', 'WHISKY', 'VODKA', 'BRANDY'])

ws_config.write('D1', 'OPCIONES VISIBLES', header_fmt)
ws_config.write_column('D2', ['SI', 'NO'])

ws_config.write('E1', 'LEYENDA ALERGENOS', header_fmt)
ws_config.write_column('E2', ['1=Gluten', '2=Crustáceos', '3=Huevos', '4=Pescado', '5=Cacahuetes', '6=Soja', '7=Lácteos', '...'])

# ==========================================
# 2. PESTAÑA COMIDA (Estructura)
# ==========================================
cols_comida = [
    'CATEGORIA',        # A - Desplegable
    'SUBCATEGORIA',     # B - Desplegable
    'NOMBRE_ES',        # C
    'NOMBRE_EN',        # D
    'DESC_ES',          # E
    'DESC_EN',          # F
    'PRECIO',           # G
    'ALERGENOS (Ej: 1,4)', # H
    'VISIBLE'           # I - Desplegable
]

ws_comida.write_row('A1', cols_comida, header_fmt)
ws_comida.set_column('A:B', 20) # Ancho columnas categoría
ws_comida.set_column('C:F', 30) # Ancho textos
ws_comida.set_column('G:G', 10, price_fmt)
ws_comida.set_column('H:I', 15)

# --- VALIDACIÓN DE DATOS (Desplegables) ---
# Validar Categoria Comida (Lee de Config A2:A20)
ws_comida.data_validation('A2:A500', {'validate': 'list', 'source': '=CONFIGURACION!$A$2:$A$20'})
# Validar Subcategoria (Lee de Config C2:C20)
ws_comida.data_validation('B2:B500', {'validate': 'list', 'source': '=CONFIGURACION!$C$2:$C$20'})
# Validar Visible (SI/NO)
ws_comida.data_validation('I2:I500', {'validate': 'list', 'source': '=CONFIGURACION!$D$2:$D$3'})

# ==========================================
# 3. PESTAÑA BEBIDAS (Estructura)
# ==========================================
cols_bebida = [
    'CATEGORIA',        # A
    'SUBCATEGORIA',     # B
    'NOMBRE_ES',        # C
    'NOMBRE_EN',        # D
    'DESC_ES',          # E
    'DESC_EN',          # F
    'PRECIO_COPA',      # G
    'PRECIO_BOTELLA',   # H
    'ALERGENOS',        # I
    'VISIBLE'           # J
]

ws_bebida.write_row('A1', cols_bebida, header_fmt)
ws_bebida.set_column('A:B', 20)
ws_bebida.set_column('C:F', 30)
ws_bebida.set_column('G:H', 12, price_fmt)
ws_bebida.set_column('I:J', 15)

# --- VALIDACIÓN DE DATOS (Desplegables) ---
# Validar Categoria Bebida (Lee de Config B2:B20)
ws_bebida.data_validation('A2:A500', {'validate': 'list', 'source': '=CONFIGURACION!$B$2:$B$20'})
# Validar Subcategoria
ws_bebida.data_validation('B2:B500', {'validate': 'list', 'source': '=CONFIGURACION!$C$2:$C$20'})
# Validar Visible
ws_bebida.data_validation('J2:J500', {'validate': 'list', 'source': '=CONFIGURACION!$D$2:$D$3'})

# ==========================================
# CERRAR Y GUARDAR
# ==========================================
workbook.close()
print(f"Archivo '{filename}' creado exitosamente. ¡Abrelo y empieza a llenar!")