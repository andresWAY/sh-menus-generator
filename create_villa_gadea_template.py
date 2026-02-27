import xlsxwriter
import pandas as pd
import os

print("Leyendo datos de Villa Gadea...")
df_comida = pd.read_excel('data/SH_Villa_Gadea.xlsx', sheet_name='COMIDA')
df_bebidas = pd.read_excel('data/SH_Villa_Gadea.xlsx', sheet_name='BEBIDAS')

# Extraer categorías únicas preservando el orden
categorias_comida_unicas = df_comida['CATEGORIA'].dropna().unique().tolist()
categorias_bebida_unicas = df_bebidas['CATEGORIA'].dropna().unique().tolist()

dict_cat_en = {
    "PARA COMPARTIR": "TO SHARE...",
    "ENSALADAS": "SALADS",
    "SANDWICH Y HAMBURGUESA": "SANDWICH & BURGER",
    "PRINCIPALES": "MAIN COURSES",
    "POSTRES": "DESSERTS",
    "AGUAS Y REFRESCOS": "WATER & SOFT DRINKS",
    "CERVEZAS": "BEERS",
    "VINOS BLANCOS": "WHITE WINES",
    "VINOS TINTOS": "RED WINES",
    "CÓCTELES": "COCKTAILS"
}

categorias_comida = [(c, dict_cat_en.get(c, c)) for c in categorias_comida_unicas]
categorias_bebida = [(c, dict_cat_en.get(c, c)) for c in categorias_bebida_unicas]

alergenos = [
    "1. Gluten", "2. Crustáceos", "3. Huevos", "4. Pescado",
    "5. Cacahuetes", "6. Soja", "7. Lácteos", "8. Frutos de cáscara",
    "9. Apio", "10. Mostaza", "11. Sésamo", "12. Sulfitos",
    "13. Altramuces", "14. Moluscos"
]

# MOVIDO A LA CARPETA DATA
output_path = os.path.join('data', 'MENU_CONFIGURADO_VILLA_GADEA.xlsx')
workbook = xlsxwriter.Workbook(output_path)

# Formatos
header_format = workbook.add_format({
    'bold': True, 'font_color': 'white', 'bg_color': '#25406c',
    'locked': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'
})
locked_gray = workbook.add_format({
    'bg_color': '#F2F2F2', 'locked': True, 'border': 1, 'valign': 'vcenter'
})
unlocked = workbook.add_format({
    'locked': False, 'border': 1, 'valign': 'vcenter', 'text_wrap': True
})
currency = workbook.add_format({
    'num_format': '#,##0.00 €', 'locked': False, 'border': 1, 'valign': 'vcenter'
})
unlocked_center = workbook.add_format({
    'locked': False, 'border': 1, 'align': 'center', 'valign': 'vcenter'
})

# ==========================================
# CONFIGURACIÓN
# ==========================================
ws_config = workbook.add_worksheet('CONFIGURACIÓN')
# No la ocultamos del todo para que tú puedas editar el nombre del restaurante si quieres, 
# pero la idea es que el staff no toque esto.
# ws_config.hide() 

ws_config.write_row('A1', ['Cat Comida ES', 'Cat Comida EN', 'Cat Bebida ES', 'Cat Bebida EN', 'Leyenda Alérgenos', 'NOMBRE DEL HOTEL'])

for i, (es, en) in enumerate(categorias_comida):
    ws_config.write(i+1, 0, es)
    ws_config.write(i+1, 1, en)

for i, (es, en) in enumerate(categorias_bebida):
    ws_config.write(i+1, 2, es)
    ws_config.write(i+1, 3, en)

for i, alrg in enumerate(alergenos):
    ws_config.write(i+1, 4, alrg)

# Campo para el nombre del restaurante
ws_config.write('F2', 'SH VILLA GADEA', unlocked) # Valor por defecto
ws_config.set_column('F:F', 30)

# ==========================================
# COMIDA
# ==========================================
ws_comida = workbook.add_worksheet('COMIDA')
ws_comida.freeze_panes(1, 0)
ws_comida.protect('', {'select_locked_cells': True, 'select_unlocked_cells': True})

# ELIMINADO NOMBRE_EN. AÑADIDO RESTAURANTE AL FINAL.
headers_comida = ['CATEGORIA', 'CATEGORIA_EN', 'NOMBRE_ES', 'DESC_ES', 'DESC_EN', 'PRECIO', 'ALERGENOS', 'VISIBLE', 'RESTAURANTE']
ws_comida.write_row('A1', headers_comida, header_format)

ws_comida.set_column('A:A', 20, unlocked) 
ws_comida.set_column('B:B', 20, locked_gray)
ws_comida.set_column('C:C', 30, unlocked) 
ws_comida.set_column('D:D', 40, unlocked) 
ws_comida.set_column('E:E', 40, unlocked) 
ws_comida.set_column('F:F', 12, currency) 
ws_comida.set_column('G:G', 18, unlocked_center) 
ws_comida.set_column('H:H', 10, unlocked_center) 
ws_comida.set_column('I:I', 25, locked_gray) # Formula automatica

comida_records = df_comida.to_dict(orient='records')
for row_idx, row_data in enumerate(comida_records, start=1):
    ws_comida.write(row_idx, 0, str(row_data.get('CATEGORIA', '')) if pd.notna(row_data.get('CATEGORIA')) else '')
    ws_comida.write_formula(row_idx, 1, f'=IF(A{row_idx+1}="","",VLOOKUP(A{row_idx+1},CONFIGURACIÓN!$A$2:$B$40,2,FALSE))', locked_gray)
    ws_comida.write(row_idx, 2, str(row_data.get('NOMBRE_ES', '')) if pd.notna(row_data.get('NOMBRE_ES')) else '')
    ws_comida.write(row_idx, 3, str(row_data.get('DESC_ES', '')) if pd.notna(row_data.get('DESC_ES')) else '')
    ws_comida.write(row_idx, 4, str(row_data.get('DESC_EN', '')) if pd.notna(row_data.get('DESC_EN')) else '')
    
    precio = row_data.get('PRECIO')
    if pd.notna(precio):
        ws_comida.write_number(row_idx, 5, float(precio), currency)
        
    ws_comida.write(row_idx, 6, str(row_data.get('ALERGENOS', '')) if pd.notna(row_data.get('ALERGENOS')) else '')
    ws_comida.write(row_idx, 7, str(row_data.get('VISIBLE', 'SI')) if pd.notna(row_data.get('VISIBLE')) else 'SI')
    
    # Formula para leer el Restaurante de Configuración automáticamente
    ws_comida.write_formula(row_idx, 8, f'=CONFIGURACIÓN!$F$2', locked_gray)

# Validaciones Comida
for row in range(1, 501):
    ws_comida.data_validation(row, 0, row, 0, {'validate': 'list', 'source': '=CONFIGURACIÓN!$A$2:$A$40'})
    if row > len(comida_records):
        ws_comida.write_formula(row, 1, f'=IF(A{row+1}="","",VLOOKUP(A{row+1},CONFIGURACIÓN!$A$2:$B$40,2,FALSE))', locked_gray)
        ws_comida.write_formula(row, 8, f'=CONFIGURACIÓN!$F$2', locked_gray)
    ws_comida.data_validation(row, 5, row, 5, {'validate': 'decimal', 'criteria': '>=', 'value': 0})
    
    ws_comida.data_validation(row, 6, row, 6, {
        'validate': 'any',
        'input_title': 'Lista de Alérgenos',
        'input_message': 'Escribe los números separados por coma (Ej: 1, 4, 7)\n1=Gluten, 2=Crustáceos, 3=Huevos, 4=Pescado, 5=Cacahuetes, 6=Soja, 7=Lácteos, 8=Frut.Cáscara, 9=Apio, 10=Mostaza, 11=Sésamo, 12=Sulfitos, 13=Altramuces, 14=Moluscos'
    })
    ws_comida.data_validation(row, 7, row, 7, {'validate': 'list', 'source': ['SI', 'NO']})

# ==========================================
# BEBIDAS
# ==========================================
ws_bebidas = workbook.add_worksheet('BEBIDAS')
ws_bebidas.freeze_panes(1, 0)
ws_bebidas.protect('', {'select_locked_cells': True, 'select_unlocked_cells': True})

headers_bebidas = ['CATEGORIA', 'CATEGORIA_EN', 'NOMBRE_ES', 'DESC_ES', 'DESC_EN', 'PRECIO_COPA', 'PRECIO_BOTELLA', 'ALERGENOS', 'VISIBLE', 'RESTAURANTE']
ws_bebidas.write_row('A1', headers_bebidas, header_format)

ws_bebidas.set_column('A:A', 20, unlocked)
ws_bebidas.set_column('B:B', 20, locked_gray)
ws_bebidas.set_column('C:C', 30, unlocked)
ws_bebidas.set_column('D:D', 40, unlocked)
ws_bebidas.set_column('E:E', 40, unlocked)
ws_bebidas.set_column('F:G', 12, currency) 
ws_bebidas.set_column('H:H', 18, unlocked_center)
ws_bebidas.set_column('I:I', 10, unlocked_center)
ws_bebidas.set_column('J:J', 25, locked_gray)

bebidas_records = df_bebidas.to_dict(orient='records')
for row_idx, row_data in enumerate(bebidas_records, start=1):
    ws_bebidas.write(row_idx, 0, str(row_data.get('CATEGORIA', '')) if pd.notna(row_data.get('CATEGORIA')) else '')
    ws_bebidas.write_formula(row_idx, 1, f'=IF(A{row_idx+1}="","",VLOOKUP(A{row_idx+1},CONFIGURACIÓN!$C$2:$D$40,2,FALSE))', locked_gray)
    ws_bebidas.write(row_idx, 2, str(row_data.get('NOMBRE_ES', '')) if pd.notna(row_data.get('NOMBRE_ES')) else '')
    ws_bebidas.write(row_idx, 3, str(row_data.get('DESC_ES', '')) if pd.notna(row_data.get('DESC_ES')) else '')
    # Bebidas nunca tuvo NOMBRE_EN en la V1, pero por si acaso, DESC_EN aqui es la Columna 4 (E)
    ws_bebidas.write(row_idx, 4, str(row_data.get('DESC_EN', '')) if pd.notna(row_data.get('DESC_EN')) else '')
    
    precio_copa = row_data.get('PRECIO_COPA')
    if pd.notna(precio_copa):
        ws_bebidas.write_number(row_idx, 5, float(precio_copa), currency)
        
    precio_botella = row_data.get('PRECIO_BOTELLA')
    if pd.notna(precio_botella):
        ws_bebidas.write_number(row_idx, 6, float(precio_botella), currency)
        
    ws_bebidas.write(row_idx, 7, str(row_data.get('ALERGENOS', '')) if pd.notna(row_data.get('ALERGENOS')) else '')
    ws_bebidas.write(row_idx, 8, str(row_data.get('VISIBLE', 'SI')) if pd.notna(row_data.get('VISIBLE')) else 'SI')
    
    ws_bebidas.write_formula(row_idx, 9, f'=CONFIGURACIÓN!$F$2', locked_gray)

# Validaciones Bebidas
for row in range(1, 501):
    ws_bebidas.data_validation(row, 0, row, 0, {'validate': 'list', 'source': '=CONFIGURACIÓN!$C$2:$C$40'})
    if row > len(bebidas_records):
        ws_bebidas.write_formula(row, 1, f'=IF(A{row+1}="","",VLOOKUP(A{row+1},CONFIGURACIÓN!$C$2:$D$40,2,FALSE))', locked_gray)
        ws_bebidas.write_formula(row, 9, f'=CONFIGURACIÓN!$F$2', locked_gray)
    ws_bebidas.data_validation(row, 5, row, 6, {'validate': 'decimal', 'criteria': '>=', 'value': 0})
    ws_bebidas.data_validation(row, 7, row, 7, {
        'validate': 'any',
        'input_title': 'Lista de Alérgenos',
        'input_message': 'Escribe los números separados por coma (Ej: 1, 4, 7)\n1=Gluten, 2=Crustáceos, 3=Huevos, 4=Pescado, 5=Cacahuetes, 6=Soja, 7=Lácteos, 8=Frut.Cáscara, 9=Apio, 10=Mostaza, 11=Sésamo, 12=Sulfitos, 13=Altramuces, 14=Moluscos'
    })
    ws_bebidas.data_validation(row, 8, row, 8, {'validate': 'list', 'source': ['SI', 'NO']})

workbook.close()
print(f"¡Archivo '{output_path}' generado con los datos integrados!")
