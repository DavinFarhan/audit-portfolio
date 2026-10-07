import fitz
import os
import math

OUTPUT_DIR = "brand/masterpieces"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# MASTERPIECE 1: "THE MÖBIUS COVENANT" (Simpul Kepercayaan Tak Terputus)
# ==============================================================================
# Inspirasi: Chase Bank, OpenZeppelin, Pentagram, International Woolmark.
# Bentuk: Garis kontinu tunggal geometris yang meliuk membentuk simpul tak terputus.
# Filosofi:
# - Menepati Janji: Satu garis tak terputus (unbroken loop of truth).
# - Jujur & Transparan: Terbuka dan tembus pandang di tengah (optical aperture).
# - Amanah: Simpul yang mengikat dan menjaga keamanan protokol.
# - Murah Hati & Mempermudah: Kurva halus ramah (gentle golden curves), zero visual noise.
# - Warna: Deep Trust Navy (#0B1F3A) & Luminous Emerald (#059669) accent harmonis.
# Geometri: 2 loop simetris yang saling merangkul, membentuk siluet 'Haven' abstrak.
mobius_covenant_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Möbius Covenant">
  <title>Masterpiece 1: The Möbius Covenant</title>
  <!-- Pure Geometric Infinity Shield / Topological Knot -->
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Outer Trust Loop (Deep Navy #0B1F3A) -->
    <!-- Two interlocking golden arcs that form an abstract sanctuary -->
    <path d="M 160 140 
             C 90 220 90 320 160 400 
             C 214 460 298 460 352 400 
             C 422 320 422 220 352 140
             C 300 80 212 80 160 140 Z"
          stroke="#0B1F3A" stroke-width="36"/>
    
    <!-- Inner Lens of Truth (Transparan & Aperture Cahaya) -->
    <path d="M 256 180 
             C 210 230 210 290 256 340
             C 302 290 302 230 256 180 Z"
          stroke="#059669" stroke-width="28"/>
    
    <!-- Horizontal Equator Node (Keseimbangan & Kejujuran Objektif) -->
    <line x1="200" y1="260" x2="312" y2="260" stroke="#059669" stroke-width="14" stroke-linecap="round"/>
  </g>
</svg>
"""

# Let's refine Masterpiece 1 to be even purer: The Interlocking Twin Arcs of Integrity
mobius_refined_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Covenant Knot">
  <title>Masterpiece 1: The Covenant Knot</title>
  <!-- Two Interlocking Ribbons: Navy (Security & Fiduciary Duty) + Emerald (Truth & Verification) -->
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Left Ribbon: Navy Security Arch -->
    <path d="M 256 80 
             C 140 80 84 164 84 270 
             C 84 376 160 436 256 436"
          stroke="#0B1F3A" stroke-width="36"/>
    
    <!-- Right Ribbon: Emerald Truth Arch -->
    <path d="M 256 436 
             C 352 436 428 376 428 270 
             C 428 164 372 80 256 80"
          stroke="#059669" stroke-width="36"/>
          
    <!-- Central Negative Space Aperture: Golden Diamond Eye of Truth -->
    <polygon points="256,190 306,260 256,330 206,260" 
             stroke="#0B1F3A" stroke-width="16"/>
             
    <!-- Unbroken Core Spark (Titik Pusat Kebenaran Kriptografis) -->
    <circle cx="256" cy="260" r="14" fill="#059669"/>
  </g>
</svg>
"""

# ==============================================================================
# MASTERPIECE 2: "THE PRISMATIC KEYSTONE" (Batu Penjuru Kriptografi)
# ==============================================================================
# Inspirasi: Ethereum, Chase Octagon, Basel Institute, MIT.
# Bentuk: Heksagon isometrik murni dengan aperture tengah terbuka.
# Filosofi:
# - Amanah: Keystone adalah batu kunci yang menahan seluruh kubah keamanan.
# - Jujur & Transparan: Faset berongga isometrik (wireframe kristal kaca), tembus pandang 100%.
# - Menepati Janji & Berkualitas: Simetri heksagonal 60°/120° (matematika blockchain).
# - Mempermudah: Struktur yang menguraikan kerumitan kode menjadi keteraturan murni.
keystone_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Prismatic Keystone">
  <title>Masterpiece 2: The Prismatic Keystone</title>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Outer Hexagonal Frame (Solid Navy Perimeter) -->
    <path d="M 256 64 
             L 424 160 
             L 424 352 
             L 256 448 
             L 88 352 
             L 88 160 Z"
          stroke="#0B1F3A" stroke-width="32"/>
    
    <!-- Isometric Inner Gateway (Aperture / Gerbang Terbuka = Mempermudah & Murah Hati) -->
    <!-- Top Apex Aperture is intentionally open, forming a welcoming portal -->
    <path d="M 172 208 L 256 256 L 340 208" stroke="#059669" stroke-width="28"/>
    <line x1="256" y1="256" x2="256" y2="384" stroke="#059669" stroke-width="28"/>
    
    <!-- Floating Verification Core (The Keystone Gem) -->
    <polygon points="256,128 300,160 256,192 212,160" 
             fill="#0B1F3A" stroke="#0B1F3A" stroke-width="6"/>
  </g>
</svg>
"""

# ==============================================================================
# MASTERPIECE 3: "THE ARCHITECTURAL CIPHER: F+D" (Monogram Bespoke Tingkat Dunia)
# ==============================================================================
# Inspirasi: Paul Rand, Massimo Vignelli, Peter Saville, Chermayeff & Geismar.
# Bentuk: Satu kesatuan monolinear arsitektural yang menggabungkan huruf F dan D secara cerdas.
# - Pilar kokoh di kiri (F).
# - Dua balok horizontal (Farms) yang meliuk membentuk busur pelindung perisai (D).
# - Di ruang tengah tercipta portal panah ke kanan atas secara alami (bukan tempelan centang).
# - 100% orisinal dan tidak ada yang menyamai di dunia.
cipher_fd_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Architectural Cipher FD">
  <title>Masterpiece 3: The Architectural Cipher FD</title>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- The Monolinear FD Circuit: Unbroken Single Path -->
    <!-- Starts at base of F, rises, forms F top, curves into D arc, grounds at bottom -->
    <path d="M 148 424 
             V 88 
             H 276 
             C 380 88 436 156 436 256 
             C 436 356 380 424 276 424 
             H 148"
          stroke="#0B1F3A" stroke-width="36"/>
          
    <!-- Central F Arm & Dynamic Verification Beam (Emerald #059669) -->
    <!-- Extends horizontally from F spine and terminates with a golden chamfer -->
    <path d="M 148 256 H 312" stroke="#059669" stroke-width="36"/>
    
    <!-- Ascending Vector Node (Subtle 45-deg truth beacon) -->
    <circle cx="364" cy="204" r="16" fill="#059669"/>
  </g>
</svg>
"""

# Horizontal Wordmark helper
def make_h(svg_inner, width=1440, height=480):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <g transform="translate(30, -16)">
    {svg_inner}
  </g>
  <text x="540" y="246" font-family="'Inter', -apple-system, sans-serif"
        font-weight="800" font-size="88" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="544" y="316" font-family="'Inter', -apple-system, sans-serif"
        font-weight="700" font-size="30" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="544" y="342" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.3"/>
</svg>"""

# Stacked Wordmark helper
def make_st(svg_inner, width=640, height=720):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <g transform="translate(64, 20)">
    {svg_inner}
  </g>
  <text x="320" y="595" text-anchor="middle"
        font-family="'Inter', -apple-system, sans-serif"
        font-weight="800" font-size="82" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="320" y="652" text-anchor="middle"
        font-family="'Inter', -apple-system, sans-serif"
        font-weight="700" font-size="28" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="250" y="675" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.25"/>
</svg>"""

items = [
    ("masterpiece-1-covenant", mobius_refined_svg),
    ("masterpiece-2-keystone", keystone_svg),
    ("masterpiece-3-cipher", cipher_fd_svg),
]

for slug, s_svg in items:
    # Save Symbol SVG
    sp = os.path.join(OUTPUT_DIR, f"{slug}-symbol.svg")
    with open(sp, "w", encoding="utf-8") as f:
        f.write(s_svg)
        
    # Extract inner
    i_start = s_svg.find(">") + 1
    i_end = s_svg.rfind("</svg>")
    inner = s_svg[i_start:i_end]
    
    # Save Horizontal & Stacked
    hp = os.path.join(OUTPUT_DIR, f"{slug}-horizontal.svg")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(make_h(inner))
        
    stp = os.path.join(OUTPUT_DIR, f"{slug}-stacked.svg")
    with open(stp, "w", encoding="utf-8") as f:
        f.write(make_st(inner))

# Render PNGs and PDFs
for slug, _ in items:
    for target, width in [
        (f"{slug}-symbol", 1024),
        (f"{slug}-horizontal", 1440),
        (f"{slug}-stacked", 1280),
    ]:
        svg_file = os.path.join(OUTPUT_DIR, f"{target}.svg")
        png_file = os.path.join(OUTPUT_DIR, f"{target}.png")
        pdf_file = os.path.join(OUTPUT_DIR, f"{target}.pdf")
        
        doc = fitz.open(svg_file)
        pdf_bytes = doc.convert_to_pdf()
        with open(pdf_file, "wb") as f:
            f.write(pdf_bytes)
            
        page = doc[0]
        scale = width / page.rect.width
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat, alpha=True)
        pix.save(png_file)
        print(f"Rendered {png_file} & {pdf_file}")

print("Masterpiece assets created successfully!")
