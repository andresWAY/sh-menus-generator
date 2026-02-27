import xlsxwriter

# Crear el archivo Excel
workbook = xlsxwriter.Workbook('Plantilla_Carta_Profesional.xlsx')

# ==========================================
# 1. ESTILOS Y FORMATOS (UI/UX)
# ==========================================
# Cabeceras: Azul Oscuro (#25406c), texto Blanco, negrita
header_format = workbook.add_format({
    'bold': True, 'font_color': 'white', 'bg_color': '#25406c',
    'locked': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'
})
# Celdas bloqueadas (Gris claro para fórmulas automáticas)
locked_gray = workbook.add_format({
    'bg_color': '#F2F2F2', 'locked': True, 'border': 1, 'valign': 'vcenter'
})
# Celdas editables libres
unlocked = workbook.add_format({
    'locked': False, 'border': 1, 'valign': 'vcenter'
})
# Formato Moneda estricto (€ con dos decimales)
currency = workbook.add_format({
    'num_format': '#,##0.00 €', 'locked': False, 'border': 1, 'valign': 'vcenter'
})

# ==========================================
# PESTAÑA 1: CONFIGURACIÓN (El "Cerebro")
# ==========================================
ws_config = workbook.add_worksheet('CONFIGURACIÓN')
ws_config.hide() # Oculta al usuario final

# Datos base extraídos de tu operativa
categorias_comida = [
    ("PARA COMPARTIR", "TO SHARE..."),
    ("ENTRANTES", "STARTERS"),
    ("PRINCIPALES", "MAIN COURSES"),
    ("POSTRES", "DESSERTS")
]
categorias_bebida = [
    ("AGUAS Y REFRESCOS", "WATER & SOFT DRINKS"),
    ("CERVEZAS", "BEERS"),
    ("VINOS BLANCOS", "WHITE WINES"),
    ("VINOS TINTOS", "RED WINES"),
    ("CÓCTELES", "COCKTAILS")
]
alergenos = [
    "1. Gluten", "2. Crustáceos", "3. Huevos", "4. Pescado",
    "5. Cacahuetes", "6. Soja", "7. Lácteos", "8. Frutos de cáscara",
    "9. Apio", "10. Mostaza", "11. Sésamo", "12. Sulfitos",
    "13. Altramuces", "14. Moluscos"
]

# Escribir cabeceras y datos en Configuración
ws_config.write_row('A1', ['Cat Comida ES', 'Cat Comida EN', 'Cat Bebida ES', 'Cat Bebida EN', 'Leyenda Alérgenos'])

for i, (es, en) in enumerate(categorias_comida):
    ws_config.write(i+1, 0, es)
    ws_config.write(i+1, 1, en)

for i, (es, en) in enumerate(categorias_bebida):
    ws_config.write(i+1, 2, es)
    ws_config.write(i+1, 3, en)

for i, alrg in enumerate(alergenos):
    ws_config.write(i+1, 4, alrg)

# ==========================================
# PESTAÑA 2: COMIDA
# ==========================================
ws_comida = workbook.add_worksheet('COMIDA')
ws_comida.freeze_panes(1, 0) # Inmovilizar fila de cabeceras
ws_comida.protect('', {'select_locked_cells': True, 'select_unlocked_cells': True}) # Activar bloqueo de celdas

headers_comida = ['Categoría', 'Categoría EN', 'Nombre ES', 'Descripción ES', 'Descripción EN', 'Precio', 'Alérgenos', 'Visible']
ws_comida.write_row('A1', headers_comida, header_format)

# Anchos de columna y aplicación de candados/formatos
ws_comida.set_column('A:A', 20, unlocked) 
ws_comida.set_column('B:B', 20, locked_gray) # Intocable
ws_comida.set_column('C:C', 30, unlocked) 
ws_comida.set_column('D:E', 40, unlocked) 
ws_comida.set_column('F:F', 15, currency) 
ws_comida.set_column('G:G', 20, unlocked) 
ws_comida.set_column('H:H', 15, unlocked) 

# Reglas para 500 filas de Comida
for row in range(1, 501):
    # Desplegable estricto Categoría
    ws_comida.data_validation(row, 0, row, 0, {'validate': 'list', 'source': '=CONFIGURACIÓN!$A$2:$A$20'})
    # Fórmula de autotraducción en gris
    ws_comida.write_formula(row, 1, f'=IF(A{row+1}="","",VLOOKUP(A{row+1},CONFIGURACIÓN!$A$2:$B$20,2,FALSE))', locked_gray)
    # Validación Moneda (solo permite números)
    ws_comida.data_validation(row, 5, row, 5, {'validate': 'decimal', 'criteria': '>=', 'value': 0, 'error_message': 'Por favor, introduce solo números.'})
    # Desplegable Visible
    ws_comida.data_validation(row, 7, row, 7, {'validate': 'list', 'source': ['SI', 'NO']})

# ==========================================
# PESTAÑA 3: BEBIDAS
# ==========================================
ws_bebidas = workbook.add_worksheet('BEBIDAS')
ws_bebidas.freeze_panes(1, 0)
ws_bebidas.protect('', {'select_locked_cells': True, 'select_unlocked_cells': True})

headers_bebidas = ['Categoría', 'Categoría EN', 'Nombre ES', 'Descripción ES', 'Descripción EN', 'Precio Copa', 'Precio Botella', 'Alérgenos', 'Visible']
ws_bebidas.write_row('A1', headers_bebidas, header_format)

ws_bebidas.set_column('A:A', 20, unlocked)
ws_bebidas.set_column('B:B', 20, locked_gray)
ws_bebidas.set_column('C:C', 30, unlocked)
ws_bebidas.set_column('D:E', 40, unlocked)
ws_bebidas.set_column('F:G', 15, currency) # Dos columnas de precio
ws_bebidas.set_column('H:H', 20, unlocked)
ws_bebidas.set_column('I:I', 15, unlocked)

# Reglas para 500 filas de Bebidas
for row in range(1, 501):
    # Desplegable Categoría Bebida
    ws_bebidas.data_validation(row, 0, row, 0, {'validate': 'list', 'source': '=CONFIGURACIÓN!$C$2:$C$20'})
    # Fórmula autotraducción Bebidas
    ws_bebidas.write_formula(row, 1, f'=IF(A{row+1}="","",VLOOKUP(A{row+1},CONFIGURACIÓN!$C$2:$D$20,2,FALSE))', locked_gray)
    # Validaciones Precios
    ws_bebidas.data_validation(row, 5, row, 6, {'validate': 'decimal', 'criteria': '>=', 'value': 0})
    ws_bebidas.data_validation(row, 8, row, 8, {'validate': 'list', 'source': ['SI', 'NO']})

workbook.close()
print("¡Archivo 'Plantilla_Carta_Profesional.xlsx' generado con éxito!")
