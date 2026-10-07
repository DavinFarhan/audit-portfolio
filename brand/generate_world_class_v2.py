import fitz
import os
import math

OUTPUT_DIR = "brand/world_class_v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. THE APEX PORTAL (Archway of Truth & The Keystone Diamond)
# ------------------------------------------------------------------------------
# Inspired by: National Geographic, Gateway Arch, Pentagram architecture.
# Concept: A monumental open archway (welcoming, simplifying, protective) crowned
# with a floating cryptographic diamond (truth, precision, unbroken trust).
apex_portal_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Apex Portal">
  <title>The Apex Portal</title>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- The Great Welcoming Arch (Murah Hati, Amanah, Mempermudah) -->
    <!-- Two symmetrical pillars that curve inward to form a protective yet open portal -->
    <path d="M 120 424 
             V 240 
             C 120 130 190 76 256 76 
             C 322 76 392 130 392 240 
             V 424" 
          stroke="#0B1F3A" stroke-width="36"/>
          
    <!-- Inner Portal Line (Glass-Box Transparency / Wireframe Double Path) -->
    <path d="M 184 424 
             V 260 
             C 184 196 216 156 256 156 
             C 296 156 328 196 328 260 
             V 424" 
          stroke="#059669" stroke-width="26"/>
          
    <!-- The Keystone Diamond (Amanah, Menepati Janji, Cryptographic Verity) -->
    <!-- Floating in the upper aperture as the unshakeable capstone -->
    <polygon points="256,60 286,96 256,132 226,96" 
             fill="#059669" stroke="#059669" stroke-width="4"/>
  </g>
</svg>
"""

# ------------------------------------------------------------------------------
# 2. THE CHASE/ETHEREUM HYBRID: "THE CIPHER OCTAGON" (Oktagon Presisi Kriptografi)
# ------------------------------------------------------------------------------
# Inspired by: Chermayeff & Geismar (Chase Bank), Ethereum, Bauhaus.
# 4 geometric angled geometric wedges creating an open square aperture in the center.
# Perfectly balanced, abstract, timeless, authoritative, zero clipart.
cipher_octagon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Cipher Octagon">
  <title>The Cipher Octagon</title>
  <!-- 4 Monolithic Geometric Wedges creating an unshakeable vault aperture -->
  <!-- Center is 256, 256. Center void size is 120x120 -->
  <g fill="#0B1F3A">
    <!-- Top Wedge -->
    <polygon points="176,80 336,80 396,140 336,200 176,200"/>
    <!-- Right Wedge (Emerald Accent: The Active Verification Shard) -->
    <polygon points="432,176 432,336 372,396 312,336 312,176" fill="#059669"/>
    <!-- Bottom Wedge -->
    <polygon points="336,432 176,432 116,372 176,312 336,312"/>
    <!-- Left Wedge -->
    <polygon points="80,336 80,176 140,116 200,176 200,336"/>
  </g>
</svg>
"""

# ------------------------------------------------------------------------------
# 3. THE INFINITE HARMONY: "THE TRIQUETRA OF TRUST" (Simpul Tiga Pilar Keamanan)
# ------------------------------------------------------------------------------
# Inspired by: OpenZeppelin, Woolmark, Pentagram.
# Three interlocking curved ribbons forming a continuous topological node.
# Represents the 3 Pillars: Integrity (Amanah), Transparency (Jujur), Excellence (Kualitas).
# Humanistic, warm, fluid, impossible to break (menepati janji), zero clipart.
triquetra_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="The Triquetra of Trust">
  <title>The Triquetra of Trust</title>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Ribbon 1: Upper Apex Shield (Deep Navy) -->
    <path d="M 256 70 
             C 360 170 380 320 256 430
             C 132 320 152 170 256 70 Z" 
          stroke="#0B1F3A" stroke-width="32"/>
          
    <!-- Ribbon 2: Left Embracing Arc (Murah Hati & Mempermudah) -->
    <path d="M 120 330 
             C 170 190 310 160 390 280
             C 270 390 170 380 120 330 Z" 
          stroke="#0B1F3A" stroke-width="32" opacity="0.9"/>
          
    <!-- Ribbon 3: Ascending Emerald Ray (Menepati Janji & Kualitas) -->
    <path d="M 392 330 
             C 342 190 202 160 122 280
             C 242 390 342 380 392 330 Z" 
          stroke="#059669" stroke-width="32"/>
  </g>
</svg>
"""

# Let's save and render these
v2_items = [
    ("v2-1-portal", apex_portal_svg),
    ("v2-2-octagon", cipher_octagon_svg),
    ("v2-3-triquetra", triquetra_svg),
]

for slug, s_svg in v2_items:
    sp = os.path.join(OUTPUT_DIR, f"{slug}.svg")
    pp = os.path.join(OUTPUT_DIR, f"{slug}.png")
    pdfp = os.path.join(OUTPUT_DIR, f"{slug}.pdf")
    
    with open(sp, "w", encoding="utf-8") as f:
        f.write(s_svg)
        
    doc = fitz.open(sp)
    pdf_bytes = doc.convert_to_pdf()
    with open(pdfp, "wb") as f:
        f.write(pdf_bytes)
        
    page = doc[0]
    mat = fitz.Matrix(1024 / page.rect.width, 1024 / page.rect.width)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(pp)
    print(f"Rendered {slug}")

print("V2 generation complete!")
