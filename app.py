import streamlit as st
import pandas as pd
import os
import unicodedata
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import CMYKColor, HexColor
from io import BytesIO
import math
from pypdf import PdfWriter, PdfReader

# --- CONFIGURACIÓN ESTATICAS ---
# Colores (CMYK: C=1, M=0.78, Y=0.29, K=0.14)
TEXT_COLOR_CMYK = CMYKColor(1, 0.78, 0.29, 0.14)
REGISTRATION_BLACK = CMYKColor(1, 1, 1, 1)

BG_COLOR = HexColor("#f4f3ec")
HEADER_COLOR = HexColor("#25406c")

# Dimensiones (en puntos, 1 mm = 2.83465 pt)
MM = 2.83465
PAGE_WIDTH = 150 * MM    # 15 cm
PAGE_HEIGHT = 240 * MM   # 24 cm
BLEED = 3 * MM

# --- CONFIGURACIÓN DE FUENTES ---
# Variables Globales (se actualizarán en runtime)
FONT_BOLD = "Helvetica-Bold"
FONT_MEDIUM = "Helvetica"
FONT_REGULAR = "Helvetica" 
FONT_ITALIC = "Helvetica-Oblique"
FONT_HEADER = "Helvetica-Bold" 

# Rutas de Fuentes (Relativas)
FONT_DIR = "assets/fonts"
FONT_FILES_MAPPING = {
    "Custom-Bold": ["Brockmann-SemiBold.ttf", "Brockmann-SemiBold.otf"],
    "Custom-Medium": ["Brockmann-Medium.ttf", "Brockmann-Medium.otf"],
    "Custom-Regular": ["Brockmann-Regular.ttf", "Brockmann-Regular.otf"], 
    "Custom-Italic": ["Brockmann-RegularItalic.ttf", "Brockmann-RegularItalic.otf"],
    "Custom-Header": ["TT Trailers Trial Regular.ttf", "TT Trailers Trial Regular.otf"]
}

# Configuración de Layout
MARGIN_LEFT = 18 * MM
MARGIN_RIGHT_PRICE = 15 * MM
Y_START_MM = 28 
Y_LIMIT_MM = 28
ITEM_SPACING = 5 * MM
CATEGORY_SPACING = 10 * MM
HEADER_MARGIN_TOP_MM = 30 # 3cm de espacio blanco visual

# Tamaños de fuente 
SIZE_TITLE = 11        # Platos
SIZE_DESC = 9.5        # Descripciones (ES y EN)
SIZE_PRICE = 11.5      # Precios
SIZE_ALLERGENS = 8
SIZE_SUBCATEGORY = 14
SIZE_HEADER_CAT = 65   # Titular

def register_fonts():
    """Registra las fuentes necesarias en ReportLab con Fallback."""
    global FONT_BOLD, FONT_MEDIUM, FONT_REGULAR, FONT_ITALIC, FONT_HEADER
    
    # Intentar registrar cada variante
    for custom_name, candidates in FONT_FILES_MAPPING.items():
        registered = False
        for filename in candidates:
            path = os.path.join(FONT_DIR, filename)
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont(custom_name, path))
                    registered = True
                    break 
                except Exception as e:
                    print(f"Debug: Fallo al cargar {filename}: {e}")
        
        if registered:
            if custom_name == "Custom-Bold": FONT_BOLD = custom_name
            if custom_name == "Custom-Medium": FONT_MEDIUM = custom_name
            if custom_name == "Custom-Regular": FONT_REGULAR = custom_name
            if custom_name == "Custom-Italic": FONT_ITALIC = custom_name
            if custom_name == "Custom-Header": FONT_HEADER = custom_name
        else:
            st.warning(f"No se pudo cargar la fuente para '{custom_name}'. Usando Helvetica.")
    
    return True

def draw_crop_marks(c, width, height, bleed):
    """Dibuja marcas de corte."""
    c.setStrokeColor(REGISTRATION_BLACK)
    c.setLineWidth(0.5)
    mark_len = 5 * MM
    offset = 2 * MM
    
    trim_x1 = bleed
    trim_y1 = bleed
    trim_x2 = width - bleed
    trim_y2 = height - bleed
    
    # Esquinas
    c.line(trim_x1 - offset - mark_len, trim_y1, trim_x1 - offset, trim_y1)
    c.line(trim_x1, trim_y1 - offset - mark_len, trim_x1, trim_y1 - offset)
    c.line(trim_x2 + offset, trim_y1, trim_x2 + offset + mark_len, trim_y1)
    c.line(trim_x2, trim_y1 - offset - mark_len, trim_x2, trim_y1 - offset)
    c.line(trim_x1 - offset - mark_len, trim_y2, trim_x1 - offset, trim_y2)
    c.line(trim_x1, trim_y2 + offset, trim_x1, trim_y2 + offset + mark_len)
    c.line(trim_x2 + offset, trim_y2, trim_x2 + offset + mark_len, trim_y2)
    c.line(trim_x2, trim_y2 + offset, trim_x2, trim_y2 + offset + mark_len)

def get_wrapped_lines(text, font_name, font_size, max_width, c):
    """Divide texto en líneas que quepan en max_width."""
    if not text:
        return []
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        width = c.stringWidth(test_line, font_name, font_size)
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_page_image(c, image_path, width, height, use_bleed, auto_show=True):
    """Dibuja una imagen a pantalla completa."""
    if os.path.exists(image_path):
        if use_bleed:
            c.drawImage(image_path, 0, 0, width=width, height=height, preserveAspectRatio=False)
        else:
            # Si no hay sangrado, el canvas base (150) se centra respecto a la imagen que es mayor (156)
            img_w = width + (2 * BLEED)
            img_h = height + (2 * BLEED)
            c.drawImage(image_path, -BLEED, -BLEED, width=img_w, height=img_h, preserveAspectRatio=False)
    if use_bleed:
        draw_crop_marks(c, width, height, BLEED)
    if auto_show:
        c.showPage()
    
def draw_text_with_tracking(c, x, y, text, font_name, font_size, tracking=-30, align='left'):
    """
    Dibuja texto con tracking (charSpace).
    tracking en milésimas de em (ej: -30).
    ReportLab charSpace es en puntos? No, es extra space.
    Formula: charSpace = tracking / 1000 * fontSize.
    """
    char_space = (tracking / 1000.0) * font_size
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font_name, font_size)
    t.setCharSpace(char_space)
    
    if align == 'right':
        # Calcular ancho manual porque textObject no soporta right align con charSpace facil
        raw_width = c.stringWidth(text, font_name, font_size)
        total_width = raw_width + (len(text) - 1) * char_space if len(text) > 1 else raw_width
        t.setTextOrigin(x - total_width, y)
    elif align == 'center':
        raw_width = c.stringWidth(text, font_name, font_size)
        total_width = raw_width + (len(text) - 1) * char_space if len(text) > 1 else raw_width
        t.setTextOrigin(x - (total_width / 2.0), y)
    
    t.textOut(text)
    c.drawText(t)

class PageBuffer:
    def __init__(self, width, height, use_bleed, hotel_name=""):
        self.width = width
        self.height = height
        self.use_bleed = use_bleed
        self.commands = [] # Lista de funciones lambda o partials
        self.current_bg = None
        self.bg_priority = 0 # 0: Default, 1: Continuation, 2: New Category Start
        self.hotel_name = hotel_name

    def add_command(self, cmd):
        self.commands.append(cmd)

    def set_background(self, bg_name, priority):
        """Actualiza el fondo si la prioridad es mayor o igual."""
        if priority >= self.bg_priority:
            self.current_bg = bg_name
            self.bg_priority = priority

    def render(self, c):
        # 1. Dibujar Fondo Liso y Cabecera Dinámica
        c.setFillColor(BG_COLOR)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        
        offset_bleed = BLEED if self.use_bleed else 0
        y_top_cut = self.height - offset_bleed
        y_bottom_cut = offset_bleed
        x_left_cut = offset_bleed
        x_right_cut = self.width - offset_bleed
        
        # Marca de agua vertical derecha
        if self.current_bg:
            c.saveState()
            c.setFillColor(CMYKColor(0,0,0,0)) # Blanco
            c.setFont(FONT_HEADER, 139)
            c.translate(x_right_cut, y_bottom_cut)
            c.rotate(90)
            c.drawString(0, 0, self.current_bg.upper())
            c.restoreState()
            
        y_header = y_top_cut - (14 * MM)
        x_header_left = x_left_cut + (17 * MM)
        x_header_right = x_right_cut - (17 * MM)
        
        c.setFillColor(HEADER_COLOR)
        
        # Nombre del hotel a la izquierda
        hotel_str = self.hotel_name.upper() if getattr(self, "hotel_name", "") else ""
        if hotel_str:
            draw_text_with_tracking(c, x_header_left, y_header, hotel_str, FONT_MEDIUM, 8.8, tracking=-30, align='left')
        hotel_raw_width = c.stringWidth(hotel_str, FONT_MEDIUM, 8.8)
        char_space = (-30 / 1000.0) * 8.8
        hotel_width = hotel_raw_width + (len(hotel_str) - 1) * char_space if len(hotel_str) > 1 else hotel_raw_width
        
        # RESTAURANTE a la derecha
        rest_str = "RESTAURANTE"
        draw_text_with_tracking(c, x_header_right, y_header, rest_str, FONT_MEDIUM, 8.8, tracking=-30, align='right')
        rest_raw_width = c.stringWidth(rest_str, FONT_MEDIUM, 8.8)
        rest_width = rest_raw_width + (len(rest_str) - 1) * char_space if len(rest_str) > 1 else rest_raw_width
        
        # Línea central adaptativa
        gap = 4 * MM
        line_start = x_header_left + hotel_width + gap
        line_end = x_header_right - rest_width - gap
        
        if line_end > line_start:
            c.setStrokeColor(HEADER_COLOR)
            c.setLineWidth(0.2)
            line_y = y_header + (8.8 * 0.3)  # Alinear visualmente al centro del texto
            c.line(line_start, line_y, line_end, line_y)
        
        # 2. Marcas de corte
        if self.use_bleed:
            draw_crop_marks(c, self.width, self.height, BLEED)
            
        # 3. Datos Legales Footer (Fijo)
        # "PRECIOS EN EUROS" (Izq) - "IVA INCLUIDO" (Der)
        offset_bleed = BLEED if self.use_bleed else 0
        y_bottom_cut = offset_bleed
        x_left_cut = offset_bleed
        x_right_cut = self.width - offset_bleed
        
        # Posición: 1.7 cm de los laterales, 0.4 cm del borde inferior
        footer_y = y_bottom_cut + (4 * MM)
        footer_x_left = x_left_cut + (17 * MM)
        footer_x_right = x_right_cut - (17 * MM)
        
        c.setFillColor(HEADER_COLOR)
        draw_text_with_tracking(c, footer_x_left, footer_y, "*PRECIOS EN EUROS", FONT_ITALIC, 8.8, tracking=-25, align='left')
        draw_text_with_tracking(c, footer_x_right, footer_y, "IVA INCLUIDO", FONT_ITALIC, 8.8, tracking=-25, align='right')

        # 4. Ejecutar comandos (Texto, líneas)
        for cmd in self.commands:
            cmd(c)
            
        c.showPage()

def draw_bg_on_canvas(c, bg_name, w, h, bleed):
    # Eliminar acentos para la comparación
    bg_clean = unicodedata.normalize('NFKD', bg_name).encode('ASCII', 'ignore').decode('utf-8')
    candidates = [
        f"{bg_name}.jpg".strip(),
        f"{bg_name.strip().lower()}.jpg",
        f"{bg_name.replace(' ', '_').strip().lower()}.jpg",
        f"{bg_clean}.jpg".strip(),
        f"{bg_clean.strip().lower()}.jpg",
        "GENERICO.jpg", "generico.jpg"
    ]
    path_found = None
    for cand in candidates:
        p = os.path.join("assets/backgrounds", cand)
        if os.path.exists(p):
            path_found = p
            break
            
    if path_found:
        c.drawImage(path_found, 0, 0, width=w, height=h, preserveAspectRatio=False)

def generate_pdf_reportlab(df, use_bleed, hotel_name="", is_drinks=False):
    buffer = BytesIO()
    
    if use_bleed:
        page_width = PAGE_WIDTH + (2 * BLEED)
        page_height = PAGE_HEIGHT + (2 * BLEED)
        origin_x = BLEED
        origin_y = BLEED
    else:
        page_width = PAGE_WIDTH
        page_height = PAGE_HEIGHT
        origin_x = 0
        origin_y = 0

    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    
    # Resolver nombre del hotel dinámico
    display_name = hotel_name
    if hotel_name:
        col_match = None
        for col in df.columns:
            if str(col).strip().upper() == 'RESTAURANTE':
                col_match = col
                break
        if col_match:
            valid_rest = df[col_match].dropna()
            if not valid_rest.empty:
                val = valid_rest.iloc[0]
                if str(val).strip():
                    display_name = str(val).strip()

    # --- 1. PORTADA ---
    portada_path = os.path.join("assets/static", "portada.jpg")
    if os.path.exists(portada_path):
        draw_page_image(c, portada_path, page_width, page_height, use_bleed, auto_show=False)
        if display_name:
            # Aplicar color y texto (BLANCO para que se vea sobre el fondo oscuro de la portada)
            from reportlab.lib.colors import CMYKColor, white
            c.setFillColor(white)
            text_str = display_name.upper()
            # Centered and 7.2 cm (72 mm) from the top edge of the image
            text_x = page_width / 2.0
            text_y = page_height - (72 * MM)
            draw_text_with_tracking(c, text_x, text_y, text_str, FONT_MEDIUM, 16, tracking=-15, align='center')
        c.showPage()

    # --- 2. CONTENIDO (BUFFERED) ---
    draw_top = page_height - origin_y - (Y_START_MM * MM)
    draw_bottom_limit = origin_y + (Y_LIMIT_MM * MM)
    
    x_text = origin_x + MARGIN_LEFT
    x_price = origin_x + PAGE_WIDTH - MARGIN_RIGHT_PRICE
    max_text_width = (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT_PRICE - (15 * MM))
    
    # Estado inicial
    current_y = draw_top
    page_buffer = PageBuffer(page_width, page_height, use_bleed, hotel_name=display_name)
    
    categories = df['CATEGORIA'].unique()
    
    for category in categories:
        cat_items = df[df['CATEGORIA'] == category]
        if cat_items.empty: continue
        
        # --- HEADER DE CATEGORÍA ---
        cap_height_mm = SIZE_HEADER_CAT * 0.3527 * 0.7 
        header_block_height = (cap_height_mm * MM) + (20 * MM) # Altura aprox header + subtitulo + margen
        
        # Necesitamos espacio para header + al menos un poco de contenido (15 MM)
        # Si no cabe, saltamos.
        available_space = current_y - draw_bottom_limit
        header_total_height = header_block_height
        
        # Prevenir viudas/huérfanas: requerir espacio para el header + margen (aprox 45mm extra)
        if available_space < (header_total_height + 45 * MM):
            # Salto de página
            page_buffer.render(c)
            page_buffer = PageBuffer(page_width, page_height, use_bleed, hotel_name=display_name)
            current_y = draw_top
            
            # Al saltar, esta categoría empieza fresca en nueva página (Top margin standard)
            is_top_of_page = True
        else:
             is_top_of_page = (current_y == draw_top)
        
        # Establecer fondo: Priority 2 (gana a continuation)
        page_buffer.set_background(category, priority=2)
        
        if is_top_of_page:
            # Si es top, usar margen standard (3cm)
            cap_height_mm = SIZE_HEADER_CAT * 0.3527 * 0.7 
            header_y_baseline = page_height - origin_y - (HEADER_MARGIN_TOP_MM * MM) - (cap_height_mm * MM)
            current_y = header_y_baseline 
        else:
            # Si es continuación, usamos el margen normal de categoría
            current_y -= CATEGORY_SPACING
            header_y_baseline = current_y

        # Command: Draw Header
        def cmd_draw_header(cv, txt=category.upper(), x=x_text, y=header_y_baseline):
            cv.setFont(FONT_HEADER, SIZE_HEADER_CAT)
            cv.setFillColor(TEXT_COLOR_CMYK)
            cv.drawString(x, y, txt)
            
        page_buffer.add_command(cmd_draw_header)
        
        # Subtítulo EN
        cat_en = ""
        if 'CATEGORIA_EN' in df.columns:
            val = df[df['CATEGORIA'] == category]['CATEGORIA_EN'].iloc[0]
            if pd.notna(val) and str(val).strip() != "": cat_en = str(val)
        
        if cat_en:
             # La distancia visual entre la base del título (mayúsculas, sin descendientes) 
             # y la parte superior de la traducción (fuente de 10pt = ~7pt height) debe ser 2mm.
             # Diferencia total de líneas bases = 2mm (gap) + ~7pt (ascendente del inglés) = ~4.5 mm
             current_y -= (4.5 * MM)
             def cmd_draw_subcat_en(cv, txt=cat_en, x=x_text, y=current_y):
                 cv.setFont(FONT_BOLD, 10) 
                 cv.setFillColor(TEXT_COLOR_CMYK)
                 cv.drawString(x, y, txt)
             page_buffer.add_command(cmd_draw_subcat_en)

        current_y -= (10 * MM) 

        # --- ITEMS ---
        current_subcategory = None
        
        for index, row in cat_items.iterrows():
            if str(row.get('VISIBLE', 'SI')).upper() != 'SI': continue

            name = str(row['NOMBRE_ES']).upper() if pd.notna(row['NOMBRE_ES']) else ""
            desc_es = str(row['DESC_ES']) if pd.notna(row['DESC_ES']) else ""
            desc_en = str(row.get('DESC_EN', '')).lower() if pd.notna(row.get('DESC_EN', '')) else ""
            
            price_str_1 = ""
            price_str_2 = ""
            if is_drinks:
                 p_bot = str(row.get('PRECIO_BOTELLA',''))
                 p_copa = str(row.get('PRECIO_COPA',''))
                 if p_bot and p_bot != 'nan': price_str_1 = p_bot
                 if p_copa and p_copa != 'nan': price_str_2 = p_copa
            else:
                 p = str(row.get('PRECIO',''))
                 if p and p != 'nan': price_str_1 = p
            
            allergens = str(row.get('ALERGENOS', '')) if pd.notna(row.get('ALERGENOS', '')) else ""
            if allergens == "nan": allergens = ""
            subcategory = str(row.get('SUBCATEGORIA', '')) if pd.notna(row.get('SUBCATEGORIA', '')) else ""
            if subcategory == "nan": subcategory = ""

            # Calcular Altura Item (Temp Canvas)
            temp_c = canvas.Canvas(BytesIO())
            
            height_sub = (SIZE_SUBCATEGORY + 8) if (subcategory and subcategory != current_subcategory) else 0
            # Altura del alérgeno = Tamaño de fuente. El gap será de 2mm (0.2cm).
            height_allergens = (SIZE_ALLERGENS + (2 * MM)) if allergens else 0
            
            name_lines = get_wrapped_lines(name, FONT_BOLD, SIZE_TITLE, max_text_width, temp_c)
            height_name = len(name_lines) * (SIZE_TITLE + 2)
            
            # Tracking compensacion en el calculo de ancho? get_wrapped_lines usa stringWidth standard.
            # Con tracking, el texto es un poco mas ancho (si tracking pos) o estrecho (si neg).
            # Como tracking es -30 (estrecho), estamos safe usando wrap standard (sobrará espacio).
            
            desc_es_lines = get_wrapped_lines(desc_es, FONT_REGULAR, SIZE_DESC, max_text_width, temp_c)
            height_desc_es = len(desc_es_lines) * (SIZE_DESC + 2)
            
            desc_en_lines = get_wrapped_lines(desc_en, FONT_ITALIC, SIZE_DESC, max_text_width, temp_c)
            height_desc_en = len(desc_en_lines) * (SIZE_DESC + 2)
            
            total_item_height = height_sub + height_allergens + height_name + height_desc_es + height_desc_en + ITEM_SPACING
            
            # Chequear espacio
            if current_y - total_item_height < draw_bottom_limit:
                page_buffer.render(c)
                page_buffer = PageBuffer(page_width, page_height, use_bleed, hotel_name=display_name)
                current_y = draw_top
                page_buffer.set_background(category, priority=1)
            
            # --- AGREGAR COMANDOS ---
            
            if subcategory and subcategory != current_subcategory:
                current_subcategory = subcategory
                def cmd_sub(cv, txt=subcategory.upper(), y=current_y):
                    cv.setFont(FONT_BOLD, SIZE_SUBCATEGORY)
                    cv.setFillColor(TEXT_COLOR_CMYK)
                    cv.drawString(x_text, y, txt)
                    line_y = y + (SIZE_SUBCATEGORY * 0.3)
                    cv.setLineWidth(1)
                    cv.setStrokeColor(TEXT_COLOR_CMYK)
                    cv.line(origin_x, line_y, x_text - 3*MM, line_y)
                page_buffer.add_command(cmd_sub)
                current_y -= (SIZE_SUBCATEGORY + 8)
                
            if allergens:
                def cmd_aller(cv, txt=f"({allergens})", y=current_y):
                    cv.setFont(FONT_MEDIUM, SIZE_ALLERGENS)
                    cv.setFillColor(TEXT_COLOR_CMYK)
                    draw_text_with_tracking(cv, x_text, y, txt, FONT_MEDIUM, SIZE_ALLERGENS, -30)
                page_buffer.add_command(cmd_aller)
                # Restar la altura del número + los 2mm exactos hasta el nombre del plato
                current_y -= (SIZE_ALLERGENS + (2 * MM))
            
            def cmd_name_price(cv, n_lines=name_lines, p1=price_str_1, p2=price_str_2, y_start=current_y):
                cv.setFont(FONT_MEDIUM, SIZE_PRICE)
                cv.setFillColor(TEXT_COLOR_CMYK)
                if p1: draw_text_with_tracking(cv, x_price, y_start, p1, FONT_MEDIUM, SIZE_PRICE, -30, align='right')
                if p2: 
                     off = 15*MM if p1 else 0
                     draw_text_with_tracking(cv, x_price - off, y_start, p2, FONT_MEDIUM, SIZE_PRICE, -30, align='right')
                
                cv.setFont(FONT_BOLD, SIZE_TITLE)
                y = y_start
                for line in n_lines:
                    draw_text_with_tracking(cv, x_text, y, line, FONT_BOLD, SIZE_TITLE, -30)
                    y -= (SIZE_TITLE + 2)
            
            page_buffer.add_command(cmd_name_price)
            current_y -= height_name
            
            def cmd_desc(cv, d_es=desc_es_lines, d_en=desc_en_lines, y_start=current_y):
                cv.setFillColor(TEXT_COLOR_CMYK)
                y = y_start
                cv.setFont(FONT_REGULAR, SIZE_DESC)
                for line in d_es:
                    draw_text_with_tracking(cv, x_text, y, line, FONT_REGULAR, SIZE_DESC, -30)
                    y -= (SIZE_DESC + 2)
                cv.setFont(FONT_ITALIC, SIZE_DESC)
                for line in d_en:
                    draw_text_with_tracking(cv, x_text, y, line, FONT_ITALIC, SIZE_DESC, -30)
                    y -= (SIZE_DESC + 2)
            
            page_buffer.add_command(cmd_desc)
            current_y -= (height_desc_es + height_desc_en + ITEM_SPACING)
            
        # Añade 1 cm por debajo del contenedor de toda la categoría
        current_y -= (10 * MM)

    page_buffer.render(c)
    
    # --- 3. ALERGENOS JPG ---
    alergenos_path = os.path.join("assets/static", "alergenos.jpg")
    if os.path.exists(alergenos_path):
        draw_page_image(c, alergenos_path, page_width, page_height, use_bleed)

    c.save()
    buffer.seek(0)
    
    # --- 4. FUSIÓN Y PAGINACIÓN ---
    output_writer = PdfWriter()
    content_reader = PdfReader(buffer)
    current_total_pages = 0
    for page in content_reader.pages:
        output_writer.add_page(page)
        current_total_pages += 1
        
    alergenos_pdf = os.path.join("assets/static", "ALERGENOS.pdf")
    if not os.path.exists(alergenos_path) and os.path.exists(alergenos_pdf):
        try:
            r = PdfReader(alergenos_pdf)
            for page in r.pages:
                output_writer.add_page(page)
                current_total_pages += 1
        except: pass
        
    remainder = (current_total_pages + 1) % 4
    padding_needed = (4 - remainder) if remainder != 0 else 0
    
    if padding_needed > 0:
        fill_buffer = BytesIO()
        c_fill = canvas.Canvas(fill_buffer, pagesize=(page_width, page_height))
        for _ in range(padding_needed):
            c_fill.setFillColor(BG_COLOR)
            c_fill.rect(0, 0, page_width, page_height, fill=1, stroke=0)
            if use_bleed: draw_crop_marks(c_fill, page_width, page_height, BLEED)
            c_fill.showPage()
        c_fill.save()
        fill_buffer.seek(0)
        fill_reader = PdfReader(fill_buffer)
        for page in fill_reader.pages:
            output_writer.add_page(page)
            current_total_pages += 1

    contra_path = os.path.join("assets/static", "contraportada.jpg")
    if os.path.exists(contra_path):
        contra_buffer = BytesIO()
        c_contra = canvas.Canvas(contra_buffer, pagesize=(page_width, page_height))
        draw_page_image(c_contra, contra_path, page_width, page_height, use_bleed)
        c_contra.save()
        contra_buffer.seek(0)
        contra_reader = PdfReader(contra_buffer)
        for page in contra_reader.pages:
            output_writer.add_page(page)

    final_buffer = BytesIO()
    output_writer.write(final_buffer)
    final_buffer.seek(0)
    return final_buffer

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Generador de Menús CMYK", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Manrope', sans-serif !important;
    }
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Manrope', sans-serif !important;
    }
    
    .main-title {
        text-align: center;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        line-height: 110% !important;
        letter-spacing: -0.1rem !important;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .main-title span {
        color: #2563EB;
    }
    
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 0.95rem;
        margin-bottom: 3rem;
        line-height: 1.5;
    }
    
    .section-title {
        text-align: center;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.05rem !important;
        color: #000000;
    }
    
    /* Pill Radio Buttons */
    .stRadio > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 0.5rem !important;
    }
    .stRadio label {
        background-color: #F3F4F6 !important;
        padding: 0.6rem 1.25rem !important;
        border-radius: 9999px !important;
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        cursor: pointer;
        border: none !important;
        transition: all 0.2s;
        box-shadow: none !important;
    }
    .stRadio label:hover {
        background-color: #E5E7EB !important;
    }
    .stRadio label[aria-checked="true"], 
    .stRadio label:has(input:checked) {
        background-color: #2563EB !important;
        color: white !important;
    }
    .stRadio > div[role="radiogroup"] > label > div:first-child {
        display: none !important; /* Hide the actual radio circle */
    }
    
    /* Selectbox */
    div[data-testid="stSelectbox"] {
        max-width: 600px;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    div[data-testid="stSelectbox"] > div {
        width: 100%;
        max-width: 450px; /* Ancho ajustado para que parezca el botón de la imagen */
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #F3F4F6 !important;
        border: none !important;
        border-radius: 9999px !important;
        height: 52px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        justify-content: center !important;
        width: 100% !important;
        padding-left: 24px !important; /* Compensate for the arrow to keep text perfectly centered */
    }
    .stSelectbox div[data-baseweb="select"] span {
        text-align: center !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Button */
    div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    div[data-testid="stButton"] button {
        border-radius: 9999px !important;
        height: 56px !important;
        width: 100% !important;
        max-width: 320px !important;
        font-size: 1.125rem !important;
        font-weight: 700 !important;
        border: none !important;
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    div[data-testid="stButton"] button:hover {
        opacity: 0.9 !important;
        background-color: #1D4ED8 !important; /* Darker blue */
        border: none !important;
    }
    div[data-testid="stButton"] button:disabled,
    div[data-testid="stButton"] button[disabled] {
        background-color: #D1D5DB !important; /* Gray color for disabled state */
        color: #6B7280 !important;
        cursor: not-allowed !important;
        opacity: 1 !important;
        border: none !important;
    }
    
    div[data-testid="stDownloadButton"] {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    div[data-testid="stDownloadButton"] button {
        border-radius: 9999px !important;
        height: 56px !important;
        width: 100% !important;
        max-width: 320px !important;
        font-size: 1.125rem !important;
        font-weight: 700 !important;
        border: none !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    
    /* Confirmation Cards */
    [data-testid="column"] {
        background-color: #F3F4F6;
        border-radius: 16px;
        padding: 1.75rem;
    }
    .card-title {
        color: #3B82F6; /* Closer to the light blue in the mockup for titles inside gray containers */
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .status-item {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .divider {
        height: 1px;
        background-color: #CECECE;
        margin: 0.75rem 0;
        width: 100%;
        max-width: 200px;
    }
    
    .stCheckbox label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    .stCheckbox div[data-testid="stWidgetLabel"] p {
        font-size: 0.9rem !important;
    }
    
    /* Adjust top padding of the whole app */
    .block-container {
        padding-top: 2rem !important;
        max-width: 800px; /* Constrain width to look more compact like the mockup */
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Generador menús<br><span>SH HOTELS</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Accede a <b>SH-menus\\data</b>, edita el <b>Excel master</b> y vuelve aquí para<br>generar un nuevo menú en PDF listo para imprimir.</div>", unsafe_allow_html=True)

# 1. SELECCIONA HOTEL
st.markdown("<div class='section-title'>Selecciona hotel...</div>", unsafe_allow_html=True)
hoteles = ["SH Jávea", "SH Calle Colón", "SH Castellón", "SH Avenida del Puerto", "SH Avenida de Francia", "SH Villa Gadea"]
hotel_seleccionado = st.radio("Hotel", hoteles, horizontal=True, label_visibility="collapsed")

# 2. SELECCIONA TIPO
st.markdown("<div class='section-title'>Selecciona tipo...</div>", unsafe_allow_html=True)

import shutil
import time

# Dynamic file path based on hotel
hotel_filename = hotel_seleccionado.replace(" ", "_") + ".xlsx"
file_path = os.path.join("data", hotel_filename)

# Fallback to master if specific hotel file doesn't exist yet (optional behavior, keeping it strict for now)
if not os.path.exists(file_path):
    # Using a generic placeholder or the master if we want to be forgiving. 
    # Let's enforce the specific file to match the requirement: "varios excel separados por hotel"
    pass

# Silent checks
fonts_ok = register_fonts()
folders_ok = os.path.exists("data") and os.path.exists("assets")
excel_ok = os.path.exists(file_path)

valid_sheets = ["Selecciona tipo de carta..."]
if excel_ok:
    target_path = file_path
    is_temp_copy = False
    try:
        temp_filename = f"temp_read_{int(time.time())}.xlsx"
        shutil.copy(file_path, temp_filename)
        target_path = temp_filename
        is_temp_copy = True
    except:
        pass
        
    try:
        with pd.ExcelFile(target_path) as xls:
            # Exclude 'ITEMS' sheet from the dropdown
            sheets = [s for s in xls.sheet_names if s != "ITEMS"]
            valid_sheets.extend(sheets)
    except:
        pass
    finally:
        if is_temp_copy and os.path.exists(target_path):
            try:
                os.remove(target_path)
            except:
                pass

tipo_carta = st.selectbox("Tipo de carta", valid_sheets, label_visibility="collapsed")

# 3. CONFIRMAR
st.markdown("<div class='section-title'>Confirmar...</div>", unsafe_allow_html=True)

col_sys, col_conf = st.columns(2, gap="large")

with col_sys:
    st.markdown("<div class='card-title'>Sistema</div>", unsafe_allow_html=True)
    
    fonts_text = "Fuentes activadas (ok)" if fonts_ok else "Fuentes activadas (pendiente)"
    folders_text = "Estructura de carpetas detectada (ok)" if folders_ok else "Faltan carpetas (error)"
    excel_text = f"Excel {hotel_filename} (ok)" if excel_ok else f"Falta {hotel_filename} (error)"
    
    st.markdown(f"""
    <div class='status-item' style='color: {"#16A34A" if fonts_ok else "#DC2626"}'>{fonts_text}</div>
    <div class='divider'></div>
    <div class='status-item' style='color: {"#16A34A" if folders_ok else "#DC2626"}'>{folders_text}</div>
    <div class='divider'></div>
    <div class='status-item' style='color: {"#16A34A" if excel_ok else "#DC2626"}'>{excel_text}</div>
    """, unsafe_allow_html=True)
    
with col_conf:
    st.markdown("<div class='card-title'>Configuración</div>", unsafe_allow_html=True)
    use_bleed = st.checkbox("Añadir sangre de 3mm")
    st.markdown("<div class='divider' style='margin-top: 10px; margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    use_marks = st.checkbox("Añadir marcas de corte")

# 4. BOTON GENERAR
is_ready = excel_ok and tipo_carta != "Selecciona tipo de carta..."

st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    if st.button("Generar menú", type="primary", disabled=not is_ready, use_container_width=True):
        with st.spinner("Compilando PDF..."):
            try:
                target_path = file_path
                is_temp_copy = False
                try:
                    temp_filename = f"temp_read_{int(time.time())}.xlsx"
                    shutil.copy(file_path, temp_filename)
                    target_path = temp_filename
                    is_temp_copy = True
                except:
                    pass
                    
                df_run = pd.read_excel(target_path, sheet_name=tipo_carta)
                
                if is_temp_copy and os.path.exists(target_path):
                    try:
                        os.remove(target_path)
                    except:
                        pass
                    
                is_drinks = (tipo_carta == "BEBIDAS")
                
                final_pdf = generate_pdf_reportlab(df_run, use_bleed, hotel_name=hotel_seleccionado, is_drinks=is_drinks)
                
                st.success(f"¡PDF Generado con éxito para {hotel_seleccionado} - {tipo_carta}!")
                st.download_button(
                    label="Descargar PDF",
                    data=final_pdf,
                    file_name=f"Menu_{hotel_seleccionado.replace(' ', '_')}_{tipo_carta}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generando PDF: {e}")
