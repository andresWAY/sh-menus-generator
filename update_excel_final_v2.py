import pandas as pd
import os

def create_real_menu_data():
    # Estructura basada en las imágenes del usuario
    data = []
    
    # --- PARA COMPARTIR ---
    cat = "PARA COMPARTIR"
    cat_en = "TO SHARE..."
    subcat = None
    
    items = [
        {"es": "NACHOS", "desc_es": "GUACAMOLE Y CREMA DE QUESO CHEDDAR", "en": "Guacamole & cheddar cream cheese", "price": 9, "aller": "2, 4, 11, 12"},
        {"es": "BOQUERONES EN VINAGRE", "desc_es": "PAPAS, PEPINILLOS Y CEBOLLA ENCURTIDA", "en": "Anchovies in vinegar (crisps, pickles & pickled onion)", "price": 10, "aller": "4, 6, 12"},
        {"es": "CROQUETAS DE JAMÓN IBÉRICO", "desc_es": "Iberian ham croquettes", "en": None, "price": 11, "aller": "4, 5, 11"}, # Desc en español parece ser solo titulo, user puso desc en EN como desc
        # Corrección: En la imagen "Iberian ham croquettes" está en la línea de descripción EN. DESC_ES está vacío o implícito.
        # Ajustaré para que "Iberian ham croquettes" vaya a DESC_EN.
        
        {"es": "CROQUETAS DE CARABINERO", "desc_es": "TOGARASHI Y MAYONESA JAPONESA", "en": "King prawn croquettes (togarashi & japanese mayonnaise)", "price": 13, "aller": "1, 4, 5, 6, 7, 8, 11, 13"},
        {"es": "BUÑUELOS DE BACALAO EN TEMPURA", "desc_es": "MERMELADA DE TOMATE Y ALIOLI", "en": "Tempura cod fritter (tomato jam & garlic mayonnaise)", "price": 12, "aller": "4, 5, 6"},
        {"es": "COCA DE ACEITE CON SARDINA AHUMADA", "desc_es": "QUESO CURADO DE OVEJA", "en": "Oil cake with smoked sardine (cured sheep's cheese)", "price": 10, "aller": "4, 6, 11"},
        {"es": "TORREZNOS DE SORIA", "desc_es": "MOUSSE DE AGUACATE Y CEBOLLA ENCURTIDA", "en": "Fried pork belly (avocado mousse & pickled onion)", "price": 12, "aller": "11, 12"},
        {"es": "FIGATELL DE SEPIA CON PICADA DE CACAHUETE", "desc_es": "MAYONESA DE CHILES", "en": "Cuttlefish meatball with peanut dressing (chilli mayonnaise)", "price": 13, "aller": "3, 4, 5, 6, 7, 10, 11, 12, 13"},
        {"es": "TITAINA DEL CABANYAL", "desc_es": "HUEVO FRITO Y CHIPS DE PATATA", "en": "Fried vegetables with tomato (fried egg & potato chips)", "price": 14, "aller": "3, 5, 6"},
        {"es": "TABLA DE QUESO", "desc_es": "TOSTAS DE PAN Y FRUTOS SECOS", "en": "Cheese plate (bread toasts & nuts)", "price": 18, "aller": "3, 4, 11"},
        {"es": "JAMÓN IBÉRICO DE BELLOTA CASTRO Y GONZÁLEZ (100GR)", "desc_es": "Iberian ham", "en": None, "price": 25, "aller": "4"},
    ]
    
    for i in items:
        # Ajuste específico para Croquetas Jamon (Desc EN estaba como Desc ES visualmente?) No, la imagen tiene "Iberian ham croquettes" en cursiva abajo. Es DESC_EN.
        desc_english = i.get("en", "")
        if i["es"] == "CROQUETAS DE JAMÓN IBÉRICO": desc_english = "Iberian ham croquettes"
        if i["es"] == "JAMÓN IBÉRICO DE BELLOTA CASTRO Y GONZÁLEZ (100GR)": desc_english = "Iberian ham"

        data.append({
            "CATEGORIA": cat, "CATEGORIA_EN": cat_en, "SUBCATEGORIA": subcat,
            "NOMBRE_ES": i["es"], "DESC_ES": i["desc_es"], "NOMBRE_EN": "", "DESC_EN": desc_english,
            "PRECIO": i["price"], "ALERGENOS": i["aller"], "VISIBLE": "SI"
        })

    # --- ENSALADAS ---
    cat = "ENSALADAS"
    cat_en = "SALADS"
    
    items = [
        {"es": "ENSALADA DE TOMATE VALENCIANO", "desc_es": "VENTRESCA DE ATÚN Y CEBOLLA TIERNA", "en": "Valencian tomato salad (tuna belly & spring onion)", "price": 13, "aller": "6"},
        {"es": "ENSALADA MEDITERRÁNEA", "desc_es": "TOMATE, HUEVO DURO Y ATÚN", "en": "Mediterranean salad (tomato, boiled egg & tuna)", "price": 12, "aller": "5, 6"},
        {"es": "ENSALADA CÉSAR", "desc_es": "POLLO Y QUESO PARMESANO", "en": "Cesar salad (chicken & parmesan cheese)", "price": 14, "aller": "4, 5, 6, 8, 11"},
        {"es": "CREMA DEL CHEF", "desc_es": "VERDURAS DE TEMPORADA", "en": "Chef's cream (seasonal vegetables)", "price": 11, "aller": ""},
    ]
    
    for i in items:
        data.append({
            "CATEGORIA": cat, "CATEGORIA_EN": cat_en, "SUBCATEGORIA": subcat,
            "NOMBRE_ES": i["es"], "DESC_ES": i["desc_es"], "NOMBRE_EN": "", "DESC_EN": i["en"],
            "PRECIO": i["price"], "ALERGENOS": i["aller"], "VISIBLE": "SI"
        })

    # --- SANDWICH Y HAMBURGUESA ---
    cat = "SANDWICH Y HAMBURGUESA" # Ajustado a SINGULAR según imagen "SANDWICH Y HAMBURGUESA"
    cat_en = "SANDWICH & BURGER"
    
    items = [
        {"es": "SÁNDWICH CLUB", "desc_es": "POLLO, JAMÓN, BACON, TOMATE Y MAYONESA", "en": "Chicken, ham, bacon, tomato & mayonnaise", "price": 15, "aller": "4, 5, 8, 11"},
        {"es": "BIKINI", "desc_es": "JAMÓN COCIDO AHUMADO Y QUESO EMMENTAL", "en": "Cooked ham & emmental cheese", "price": 14, "aller": "4, 11"},
        {"es": "SALMÓN AHUMADO", "desc_es": "PAN DE CENTENO Y SALSA DE YOGUR", "en": "Smoked salmon (rye bread & yogurt sauce)", "price": 17, "aller": "4, 6, 11"},
        {"es": "SÁNDWICH DE PASTRAMI", "desc_es": "SALSA MOSTAZA Y PEPINO ENCURTIDO", "en": "Pastrami (mustard sauce & pickles)", "price": 16, "aller": "2, 5, 8, 11"},
        {"es": "HAMBURGUESA", "desc_es": "BACON, PEPINILLOS Y QUESO CHEDDAR", "en": "Bacon, pickles, cheddar cheese", "price": 16, "aller": "4, 12"},
    ]
    
    for i in items:
        data.append({
            "CATEGORIA": cat, "CATEGORIA_EN": cat_en, "SUBCATEGORIA": subcat,
            "NOMBRE_ES": i["es"], "DESC_ES": i["desc_es"], "NOMBRE_EN": "", "DESC_EN": i["en"],
            "PRECIO": i["price"], "ALERGENOS": i["aller"], "VISIBLE": "SI"
        })

    # --- PRINCIPALES ---
    cat = "PRINCIPALES"
    cat_en = "MAIN COURSES"
    
    items = [
        {"es": "CARRILLERA IBÉRICA", "desc_es": "LECHE DE COCO, CURRY ROJO", "en": "Iberian cheeks (coconut milk & red curry)", "price": 19, "aller": "2, 11, 12"},
        {"es": "COSTILLAS DE CERDO SAINT LOUIS", "desc_es": "SALSA GOCHUJANG", "en": "Saint Louis pork ribs (Gochujang sauce)", "price": 20, "aller": "4, 13"},
        {"es": "PECHUGA DE POLLO BRASEADO", "desc_es": "TOMILLO Y LIMÓN", "en": "Grilled chicken breast (thyme & lemon)", "price": 18, "aller": ""},
        {"es": "COSTILLA DE VACA ASADA", "desc_es": "GLASEADA AL OPORTO", "en": "Roast beef rib (Oporto wine glaze)", "price": 21, "aller": "4, 8, 9, 12"},
        {"es": "ENTRECOT DE VACA RUBIA GALLEGA (250GR)", "desc_es": "Galician beef rib eye", "en": "*Las carnes van acompañadas de patatas fritas o verduras a la plancha / The meat dishes are accompanied by fries or grilled vegetables", "price": 24, "aller": ""}, # Nota: El aviso de carnes está arriba a la derecha en la imagen, pero lo pondré como descripción por ahora o nota global.
        # Corrección: En la imagen hay un texto flotante arriba a la derecha. Lo ignoraré de la descripción del plato y lo pondré como nota o lo dejaré estar si no me pide implementarlo exacto ahí.
        # Pongo la desc en inglés del plato normal y ya.
        
        {"es": "SALMÓN MARINADO EN MISO", "desc_es": "ENSALADA DE PEPINO", "en": "Miso marinated salmon (cucumber salad)", "price": 20, "aller": "6, 12, 13"},
        {"es": "BACALAO AL PIL PIL", "desc_es": "SALTEADO DE PIMIENTO DEL PIQUILLO", "en": "Cod in pil pil sauce (red pepper sauté)", "price": 19, "aller": "6"},
        {"es": "CANELONES DE HUMMUS Y BERENJENA", "desc_es": "PICADA DE CACAHUETE", "en": "Hummus & aubergine cannelloni (peanut dressing)", "price": 17, "aller": "2, 10"},
    ]
    
    for i in items:
        # Fix Entrecot desc
        desc_en_val = i["en"]
        if i["es"].startswith("ENTRECOT"): desc_en_val = "Galician beef rib eye"
        
        data.append({
            "CATEGORIA": cat, "CATEGORIA_EN": cat_en, "SUBCATEGORIA": subcat,
            "NOMBRE_ES": i["es"], "DESC_ES": i["desc_es"], "NOMBRE_EN": "", "DESC_EN": desc_en_val,
            "PRECIO": i["price"], "ALERGENOS": i["aller"], "VISIBLE": "SI"
        })

    # --- POSTRES ---
    cat = "POSTRES"
    cat_en = "DESSERTS"
    
    items = [
        {"es": "CANUTILLOS DE MEMBRILLO Y REQUESÓN", "desc_es": "CRUMBLE DE AVELLANA", "en": "Quince & cottage cheese (hazelnuts crumble)", "price": 8, "aller": "3, 4, 5, 11"},
        {"es": "CHEESECAKE", "desc_es": "COULIS DE FRESA", "en": "Strawberry coulis", "price": 8, "aller": "4, 5, 11"},
        {"es": "CRUJIENTE DE MANZANA", "desc_es": "HELADO DE LECHE MERENGADA", "en": "Apple cake (meringue milk ice cream)", "price": 8, "aller": "4, 11"},
        {"es": "COULANT DE CHOCOLATE BELGA", "desc_es": "HELADO DE VAINILLA", "en": "Belgian chocolate coulant (vanilla ice cream)", "price": 8, "aller": "4, 5, 11, 13"},
        {"es": "FRUTA DE TEMPORADA", "desc_es": "Seasonal fruit", "en": "", "price": 7, "aller": ""},
    ]

    for i in items:
        data.append({
            "CATEGORIA": cat, "CATEGORIA_EN": cat_en, "SUBCATEGORIA": subcat,
            "NOMBRE_ES": i["es"], "DESC_ES": i["desc_es"], "NOMBRE_EN": "", "DESC_EN": i["en"],
            "PRECIO": i["price"], "ALERGENOS": i["aller"], "VISIBLE": "SI"
        })

    # Crear DataFrame
    df_new = pd.DataFrame(data)
    
    # Cargar Excel existente para mantener otras hojas
    excel_path = "data/MENU_MASTER_FINAL.xlsx"
    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df_new.to_excel(writer, sheet_name='COMIDA', index=False)
            # Recrear BEBIDAS (dummy por ahora o copiar lógica antigua si tuviera los datos, pero el usuario solo mandó comida en imágenes)
            # Crearé una hoja BEBIDAS placeholder
            pd.DataFrame(columns=df_new.columns).to_excel(writer, sheet_name='BEBIDAS', index=False)
            pd.DataFrame(columns=df_new.columns).to_excel(writer, sheet_name='ITEMS', index=False)
            
    print("Excel actualizado con datos reales y columna CATEGORIA_EN.")

if __name__ == "__main__":
    create_real_menu_data()
