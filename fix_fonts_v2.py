import os
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from cu2qu.pens import Cu2QuPen

FONT_DIR = "assets/fonts"

def fix_fonts_v2():
    print(f"Iniciando reparación de fuentes en {FONT_DIR}...")
    
    files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith('.otf')]
    
    if not files:
        print("ℹ️ No se encontraron archivos .otf para convertir.")
        return

    for filename in files:
        otf_path = os.path.join(FONT_DIR, filename)
        ttf_filename = filename.rsplit('.', 1)[0] + ".ttf"
        ttf_path = os.path.join(FONT_DIR, ttf_filename)
        
        print(f"Procesando {filename} -> {ttf_filename}...")
        
        try:
            otf_font = TTFont(otf_path)
            
            # Crear nueva fuente TTF vacía
            ttf_font = TTFont()
            ttf_font.setGlyphOrder(otf_font.getGlyphOrder())
            
            # Copiar tablas esenciales explícitamente
            # 'hmtx' es CRÍTICA y faltó en la versión anterior
            tables_to_copy = ['head', 'hhea', 'maxp', 'post', 'OS/2', 'name', 'cmap', 'hmtx']
            
            for tag in tables_to_copy:
                if tag in otf_font:
                    # No copiar maxp directamente si es CFF, crear nueva
                    if tag == 'maxp': continue
                    ttf_font[tag] = otf_font[tag]
            
            # Ajustes específicos para TTF
            ttf_font['head'].indexToLocFormat = 0 # Short offset
            
            # Crear tabla maxp v1.0 limpia
            ttf_font['maxp'] = newTable('maxp')
            ttf_font['maxp'].tableVersion = 0x00010000
            ttf_font['maxp'].numGlyphs = len(otf_font.getGlyphOrder())
            # Los otros valores de maxp se recalcularán al guardar o se pueden dejar en defaults
            
            ttf_font['post'].formatType = 2.0
            
            # Crear tablas glyf y loca
            ttf_font['loca'] = newTable('loca')
            ttf_font['glyf'] = newTable('glyf')
            ttf_font['glyf'].glyphs = {}
            
            glyphSet = otf_font.getGlyphSet()
            
            for glyphName in otf_font.getGlyphOrder():
                if glyphName not in glyphSet:
                    continue
                
                # Convertir curvas (Cubic a Quadratic)
                pen = TTGlyphPen(glyphSet)
                cu2qu_pen = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
                
                try:
                    glyphSet[glyphName].draw(cu2qu_pen)
                    ttf_font['glyf'].glyphs[glyphName] = pen.glyph()
                except Exception as g_err:
                    # Si falla un glifo, intentamos continuar (podría quedar vacío)
                    print(f"  Warning: Glifo '{glyphName}' falló: {g_err}")
                    pass

            # Guardar
            ttf_font.save(ttf_path)
            print(f"Guardado correctamente: {ttf_filename}")
            
        except Exception as e:
            print(f"Error convirtiendo {filename}: {e}")

if __name__ == "__main__":
    fix_fonts_v2()
