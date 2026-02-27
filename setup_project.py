import os

def create_structure():
    # Definir carpetas
    folders = [
        "data",
        "assets/fonts",
        "assets/backgrounds",
        "assets/static"
    ]

    print("Iniciando configuración del proyecto...")

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Carpeta creada: {folder}")
        
    # Crear un archivo Excel de ejemplo si no existe
    excel_path = "data/menu_data.xlsx"
    if not os.path.exists(excel_path):
        try:
            import pandas as pd
            df_items = pd.DataFrame(columns=[
                "TIPO", "CATEGORIA", "SUBCATEGORIA", "NOMBRE_ES", "NOMBRE_EN", 
                "DESC_ES", "DESC_EN", "PRECIO_1", "PRECIO_2", "ALERGENOS", "VISIBLE"
            ])
            # Agregar una fila de ejemplo
            df_items.loc[0] = [
                "COMIDA", "ENSALADAS", "", "ENSALADA DE TOMATE", "TOMATO SALAD",
                "Con ventresca de atún", "With tuna belly", 13, "", "4, 6", "SI"
            ]
            
            # Hoja de Configuración
            df_config = pd.DataFrame(columns=["KEY", "VALUE"])
            
            with pd.ExcelWriter(excel_path) as writer:
                df_items.to_excel(writer, sheet_name="ITEMS", index=False)
                df_config.to_excel(writer, sheet_name="CONFIG", index=False)
                
            print(f"Archivo de ejemplo creado: {excel_path}")
        except ImportError:
            print(f"No se pudo crear el Excel de ejemplo porque 'pandas' no está instalado.")
            print(f"Ejecuta 'pip install -r requirements.txt' y vuelve a ejecutar este script si necesitas el Excel.")
    else:
        print(f"ℹ️ El archivo {excel_path} ya existe.")

    # Crear archivos README/Dummy para guiar al usuario
    readme_fonts = """
    Por favor, coloca aquí tus fuentes tipográficas:
    - Brockmann-SemiBold.ttf
    - Brockmann-Medium.ttf
    - Brockmann-RegularItalic.ttf
    """
    with open("assets/fonts/LEEME.txt", "w", encoding="utf-8") as f:
        f.write(readme_fonts)

    readme_bg = """
    Por favor, coloca aquí tus imágenes de fondo (.jpg):
    - [NOMBRE_CATEGORIA].jpg (Ej: ENSALADAS.jpg)
    - GENERICO.jpg (Para segundas páginas de categoría)
    - VACIO.jpg (Para páginas de relleno)
    """
    with open("assets/backgrounds/LEEME.txt", "w", encoding="utf-8") as f:
        f.write(readme_bg)
        
    readme_static = """
    Por favor, coloca aquí tu PDF de alérgenos o contraportada final:
    - ALERGENOS.pdf (o .jpg)
    """
    with open("assets/static/LEEME.txt", "w", encoding="utf-8") as f:
        f.write(readme_static)

    print("\n¡Estructura creada con éxito!")
    print("Siguiente paso: Copia tus fuentes e imágenes en las carpetas 'assets' correspondientes.")

if __name__ == "__main__":
    create_structure()
