import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import Glyph
from cu2qu.pens import Cu2QuPen
from fontTools.ttLib import newTable

FONT_DIR = "assets/fonts"

def convert_cff_to_ttf_advanced():
    print(f"Iniciando conversión avanzada en {FONT_DIR}...")
    
    files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith('.otf')]
    
    if not files:
        print("ℹ️ No se encontraron archivos .otf para convertir.")
        return

    for filename in files:
        otf_path = os.path.join(FONT_DIR, filename)
        ttf_filename = filename.rsplit('.', 1)[0] + ".ttf"
        ttf_path = os.path.join(FONT_DIR, ttf_filename)
        
        print(f"Reconstruyendo {filename} a {ttf_filename} (Cubic -> Quadratic)...")
        
        try:
            font = TTFont(otf_path)
            
            if 'CFF ' not in font:
                print(f"{filename} no parece ser CFF. Guardando directo como TTF.")
                font.save(ttf_path)
                continue

            # Crear nueva fuente vacía para TTF
            ttf_font = TTFont()
            ttf_font.setGlyphOrder(font.getGlyphOrder())
            
            # Copiar tablas básicas
            for table in ['head', 'hhea', 'maxp', 'post', 'OS/2', 'name', 'cmap']:
                if table in font:
                    ttf_font[table] = font[table]
            
            # Ajustar tablas para TTF
            ttf_font['head'].indexToLocFormat = 0
            ttf_font['maxp'].tableVersion = 0x00010000
            ttf_font['post'].formatType = 2.0
            
            # Crear tabla glyf y loca
            ttf_font['loca'] = newTable('loca')
            ttf_font['glyf'] = newTable('glyf')
            ttf_font['glyf'].glyphs = {}
            
            glyphSet = font.getGlyphSet()
            
            for glyphName in font.getGlyphOrder():
                if glyphName not in glyphSet:
                    continue
                
                # Usar Pen para convertir curvas
                pen = TTGlyphPen(glyphSet)
                cu2qu_pen = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
                
                glyphSet[glyphName].draw(cu2qu_pen)
                
                ttf_font['glyf'].glyphs[glyphName] = pen.glyph()
            
            # Guardar
            ttf_font.save(ttf_path)
            print(f"Conversión exitosa: {ttf_filename}")
            
        except Exception as e:
            print(f"Error crítico convirtiendo {filename}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    convert_cff_to_ttf_advanced()
