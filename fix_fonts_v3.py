import os
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from cu2qu.pens import Cu2QuPen

FONT_DIR = "assets/fonts"

def init_maxp(font, num_glyphs):
    """Inicializa la tabla maxp con valores seguros."""
    if 'maxp' not in font:
        font['maxp'] = newTable('maxp')
    
    maxp = font['maxp']
    maxp.tableVersion = 0x00010000
    maxp.numGlyphs = num_glyphs
    
    attrs = ['maxPoints', 'maxContours', 'maxCompositePoints', 'maxZones', 
             'maxTwilightPoints', 'maxStorage', 'maxFunctionDefs', 
             'maxInstructionDefs', 'maxStackElements', 'maxSizeOfInstructions', 
             'maxComponentElements', 'maxComponentDepth']
    
    for attr in attrs:
        if not hasattr(maxp, attr):
            setattr(maxp, attr, 0)
            
    maxp.maxZones = 2 # Valor seguro por defecto

def fix_fonts_v3():
    print(f"Iniciando reparación v3 en {FONT_DIR}...")
    
    files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith('.otf')]
    
    if not files:
        print("ℹ️ No se encontraron archivos .otf.")
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
            
            # Copiar tablas
            # ESTA VEZ INCLUIIMOS hmtx y EXCLUIMOS maxp (para crearla manual)
            tables_to_copy = ['head', 'hhea', 'post', 'OS/2', 'name', 'cmap', 'hmtx']
            
            for tag in tables_to_copy:
                if tag in otf_font:
                    ttf_font[tag] = otf_font[tag]
            
            # Ajustes head
            ttf_font['head'].indexToLocFormat = 0 
            
            # Ajustes post
            ttf_font['post'].formatType = 2.0
            
            # Inicializar glyf y loca vacíos
            ttf_font['loca'] = newTable('loca')
            ttf_font['glyf'] = newTable('glyf')
            ttf_font['glyf'].glyphs = {}
            
            # Inicializar maxp ROBUSTO
            init_maxp(ttf_font, len(otf_font.getGlyphOrder()))
            
            glyphSet = otf_font.getGlyphSet()
            
            for glyphName in otf_font.getGlyphOrder():
                if glyphName not in glyphSet:
                    continue
                
                # Convertir curvas
                pen = TTGlyphPen(glyphSet)
                cu2qu_pen = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
                
                try:
                    glyphSet[glyphName].draw(cu2qu_pen)
                    ttf_font['glyf'].glyphs[glyphName] = pen.glyph()
                except Exception as g_err:
                    print(f"  Glifo '{glyphName}': {g_err}")

            # Guardar
            ttf_font.save(ttf_path)
            print(f"Guardado correctamente: {ttf_filename}")
            
        except Exception as e:
            print(f"Error convirtiendo {filename}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    fix_fonts_v3()
