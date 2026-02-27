import os
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from cu2qu.pens import Cu2QuPen

FONT_DIR = "assets/fonts"

def init_maxp(font, num_glyphs):
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
        if not hasattr(maxp, attr): setattr(maxp, attr, 0)
    maxp.maxZones = 2

def init_post(font):
    if 'post' not in font:
        font['post'] = newTable('post')
    post = font['post']
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    attrs = ['italicAngle', 'underlinePosition', 'underlineThickness', 
             'isFixedPitch', 'minMemType42', 'maxMemType42', 'minMemType1', 'maxMemType1']
    for attr in attrs:
        if not hasattr(post, attr): setattr(post, attr, 0)

def fix_fonts_v4():
    print(f"Iniciando reparación v4 en {FONT_DIR}...")
    files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith('.otf')]
    if not files: return

    for filename in files:
        otf_path = os.path.join(FONT_DIR, filename)
        ttf_filename = filename.rsplit('.', 1)[0] + ".ttf"
        ttf_path = os.path.join(FONT_DIR, ttf_filename)
        print(f"Procesando {filename} -> {ttf_filename}...")
        
        try:
            otf_font = TTFont(otf_path)
            ttf_font = TTFont()
            ttf_font.setGlyphOrder(otf_font.getGlyphOrder())
            
            # Copiar tablas seguras
            for tag in ['head', 'hhea', 'OS/2', 'name', 'cmap', 'hmtx']:
                if tag in otf_font: ttf_font[tag] = otf_font[tag]
            
            ttf_font['head'].indexToLocFormat = 0 
            
            # Inicializar tablas complejas
            init_post(ttf_font)
            init_maxp(ttf_font, len(otf_font.getGlyphOrder()))
            
            ttf_font['loca'] = newTable('loca')
            ttf_font['glyf'] = newTable('glyf')
            ttf_font['glyf'].glyphs = {}
            
            glyphSet = otf_font.getGlyphSet()
            for glyphName in otf_font.getGlyphOrder():
                if glyphName not in glyphSet: continue
                pen = TTGlyphPen(glyphSet)
                cu2qu_pen = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
                try:
                    glyphSet[glyphName].draw(cu2qu_pen)
                    ttf_font['glyf'].glyphs[glyphName] = pen.glyph()
                except: pass

            ttf_font.save(ttf_path)
            print(f"ÉXITO: {ttf_filename}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    fix_fonts_v4()
