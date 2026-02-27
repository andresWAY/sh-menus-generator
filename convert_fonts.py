import os
from fontTools.ttLib import TTFont

FONT_DIR = "assets/fonts"

def convert_otf_to_ttf():
    print(f"Buscando fuentes OTF en {FONT_DIR}...")
    
    if not os.path.exists(FONT_DIR):
        print("Carpeta de fuentes no encontrada.")
        return

    files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith('.otf')]
    
    if not files:
        print("ℹ️ No se encontraron archivos .otf.")
        return

    for filename in files:
        otf_path = os.path.join(FONT_DIR, filename)
        ttf_filename = filename.rsplit('.', 1)[0] + ".ttf"
        ttf_path = os.path.join(FONT_DIR, ttf_filename)
        
        print(f"Convirtiendo {filename} a {ttf_filename}...")
        
        try:
            font = TTFont(otf_path)
            font.flavor = None # Remove flavour just in case
            font.save(ttf_path)
            print(f"Guardado: {ttf_filename}")
        except Exception as e:
            print(f"Error convirtiendo {filename}: {e}")

if __name__ == "__main__":
    convert_otf_to_ttf()
