import fitz
import os

OUTPUT_DIR = "brand/executive_broad_variants"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helper function to generate clean, mathematically perfect SVG paths
def build_executive_broad_svg(
    bg_color=None,              # None for transparent, or hex string like "#070E18"
    facet_fill="#0B192C",       # Top facets color
    blade_left="#F59E0B",       # Left amber blade
    blade_right="#E08A00",      # Right amber blade
    line_color="#FFFFFF",       # Facet divider & outline color
    line_width=12,              # Gutter line stroke width
    outer_stroke=False,         # Whether to stroke the outer perimeter
    hole_fill="#FFFFFF",        # Breather hole background
    node_fill="#0B192C",        # Center verification node
    opacity=1.0,                # Overall symbol opacity
    canvas_w=1000,
    canvas_h=1000
):
    bg_rect = f'<rect width="{canvas_w}" height="{canvas_h}" fill="{bg_color}"/>' if bg_color else ''
    
    # Outer hexagon perimeter path
    hex_path = "M 500,210 L 730,380 L 730,585 L 500,810 L 270,585 L 270,380 Z"
    
    outer_outline = ""
    if outer_stroke and line_color:
        outer_outline = f'<path d="{hex_path}" fill="none" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round" stroke-linecap="round"/>'
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">
  {bg_rect}
  <g id="executive_broad" opacity="{opacity}">
    <!-- 1. Central Top Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" 
             fill="{facet_fill}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>
    
    <!-- 2. Upper Left Wing -->
    <polygon points="500,210 270,380 364.3,431.2" 
             fill="{facet_fill}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>
    
    <!-- 3. Upper Right Wing -->
    <polygon points="500,210 635.7,431.2 730,380" 
             fill="{facet_fill}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>
    
    <!-- 4. Lower Left Flank -->
    <polygon points="270,380 270,585 500,505 364.3,431.2" 
             fill="{facet_fill}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>
    
    <!-- 5. Lower Right Flank -->
    <polygon points="730,380 635.7,431.2 500,505 730,585" 
             fill="{facet_fill}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>

    <!-- Left Amber/Gold Blade -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" 
          fill="{blade_left}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>

    <!-- Right Amber/Gold Blade -->
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" 
          fill="{blade_right}" stroke="{line_color}" stroke-width="{line_width}" stroke-linejoin="round"/>

    <!-- Breather Hole Ring (Clean Negative Space) -->
    <circle cx="500" cy="625" r="32" fill="{hole_fill}"/>
    
    <!-- Cryptographic Verification Node -->
    <circle cx="500" cy="625" r="14" fill="{node_fill}"/>

    <!-- Vertical Ink Slit -->
    <line x1="500" y1="657" x2="500" y2="810" stroke="{line_color}" stroke-width="{line_width}" stroke-linecap="square"/>
    
    {outer_outline}
  </g>
</svg>"""
    return svg

# ==============================================================================
# DEFINING ALL REQUESTED VARIANTS
# ==============================================================================

variants = {
    # 1. Background Hitam Pekat (Pitch Black / OLED #000000)
    "nib-dark-pitch-black.svg": build_executive_broad_svg(
        bg_color="#000000",
        facet_fill="#111D30",
        blade_left="#F59E0B",
        blade_right="#D97706",
        line_color="#FFFFFF",
        line_width=14,
        hole_fill="#FFFFFF",
        node_fill="#000000"
    ),
    
    # 2. Background Dark Navy (#0B192C) - Elegan & Mewah
    "nib-dark-navy.svg": build_executive_broad_svg(
        bg_color="#070E18",
        facet_fill="#16253D",
        blade_left="#F59E0B",
        blade_right="#D97706",
        line_color="#FFFFFF",
        line_width=14,
        hole_fill="#FFFFFF",
        node_fill="#070E18"
    ),

    # 3. Transparent Cutout Murni (Tanpa Background - Master PNG/SVG)
    "nib-transparent-master.svg": build_executive_broad_svg(
        bg_color=None,
        facet_fill="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        line_color="#FFFFFF",
        line_width=12,
        hole_fill="#FFFFFF",
        node_fill="#0B192C"
    ),

    # 4. Opacity Rendah: 10% (Watermark Laporan Audit PDF di belakang teks temuan)
    "nib-watermark-10.svg": build_executive_broad_svg(
        bg_color=None,
        facet_fill="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        line_color="#FFFFFF",
        line_width=14,
        hole_fill="#FFFFFF",
        node_fill="#0B192C",
        opacity=0.10
    ),

    # 5. Opacity Sedang: 25% (Watermark Halaman Judul / Slide Deck)
    "nib-watermark-25.svg": build_executive_broad_svg(
        bg_color=None,
        facet_fill="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        line_color="#FFFFFF",
        line_width=14,
        hole_fill="#FFFFFF",
        node_fill="#0B192C",
        opacity=0.25
    ),

    # 6. Opacity 50% (Semi-Transparan)
    "nib-watermark-50.svg": build_executive_broad_svg(
        bg_color=None,
        facet_fill="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        line_color="#FFFFFF",
        line_width=14,
        hole_fill="#FFFFFF",
        node_fill="#0B192C",
        opacity=0.50
    ),

    # 7. Monokrom Hitam (Untuk Cetak 1 Warna / Stempel Resmi Dokumen Fisik)
    "nib-monochrome-black.svg": build_executive_broad_svg(
        bg_color=None,
        facet_fill="#000000",
        blade_left="#1A1A1A",
        blade_right="#000000",
        line_color="#FFFFFF",
        line_width=16,
        hole_fill="#FFFFFF",
        node_fill="#000000"
    ),

    # 8. Monokrom Putih (Untuk Overlay di atas Banner/Video/Latar Gelap)
    "nib-monochrome-white.svg": build_executive_broad_svg(
        bg_color=None,
        facet_fill="#FFFFFF",
        blade_left="#F8FAFC",
        blade_right="#E2E8F0",
        line_color="#070E18",
        line_width=16,
        hole_fill="#070E18",
        node_fill="#FFFFFF"
    ),

    # 9. Emerald Edition di Background Hitam (Dark Mode Audit Verified)
    "nib-dark-emerald.svg": build_executive_broad_svg(
        bg_color="#070E18",
        facet_fill="#16253D",
        blade_left="#10B981",
        blade_right="#059669",
        line_color="#FFFFFF",
        line_width=14,
        hole_fill="#FFFFFF",
        node_fill="#070E18"
    ),
}

# Add Stacked and Horizontal for Dark Mode
stacked_dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 960" width="800" height="960">
  <rect width="800" height="960" fill="#070E18"/>
  <g transform="translate(150, 40) scale(0.5)">
    <!-- 1. Central Top Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 270,380 364.3,431.2" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 635.7,431.2 730,380" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" fill="#F59E0B" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" fill="#D97706" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="32" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="14" fill="#070E18"/>
    <line x1="500" y1="657" x2="500" y2="810" stroke="#FFFFFF" stroke-width="12" stroke-linecap="square"/>
  </g>
  <text x="400" y="580" text-anchor="middle"
        font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="800" font-size="64" fill="#F8FAFC" letter-spacing="3">FARHAN DAVIN</text>
  <text x="400" y="632" text-anchor="middle"
        font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="700" font-size="22" fill="#F59E0B" letter-spacing="7">SMART CONTRACT AUDITOR</text>
  <rect x="330" y="656" width="140" height="4" rx="2" fill="#F59E0B" opacity="0.6"/>
</svg>"""

horizontal_dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480">
  <rect width="1440" height="480" fill="#070E18"/>
  <g transform="translate(60, 20) scale(0.44)">
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 270,380 364.3,431.2" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 635.7,431.2 730,380" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="#16253D" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" fill="#F59E0B" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" fill="#D97706" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="32" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="14" fill="#070E18"/>
    <line x1="500" y1="657" x2="500" y2="810" stroke="#FFFFFF" stroke-width="12" stroke-linecap="square"/>
  </g>
  <text x="560" y="246" font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="800" font-size="88" fill="#F8FAFC" letter-spacing="2">FARHAN DAVIN</text>
  <text x="564" y="316" font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="700" font-size="30" fill="#F59E0B" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="564" y="342" width="140" height="4" rx="2" fill="#F59E0B" opacity="0.6"/>
</svg>"""

variants["nib-stacked-dark.svg"] = stacked_dark_svg
variants["nib-horizontal-dark.svg"] = horizontal_dark_svg

print("Writing SVG variant files...")
for fname, content in variants.items():
    p = os.path.join(OUTPUT_DIR, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {fname}")

# Rendering PNG & PDF
print("\nRendering high-res PNGs and Vector PDFs...")
for fname in variants.keys():
    base = fname[:-4]
    svg_p = os.path.join(OUTPUT_DIR, fname)
    png_p = os.path.join(OUTPUT_DIR, f"{base}.png")
    pdf_p = os.path.join(OUTPUT_DIR, f"{base}.pdf")
    
    width = 1000
    if "stacked" in base:
        width = 1280
    elif "horizontal" in base:
        width = 1440
        
    doc = fitz.open(svg_p)
    pdf_bytes = doc.convert_to_pdf()
    with open(pdf_p, "wb") as f:
        f.write(pdf_bytes)
        
    page = doc[0]
    mat = fitz.Matrix(width / page.rect.width, width / page.rect.width)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(png_p)
    print(f"  -> Generated {png_p} ({pix.width}x{pix.height}) & {pdf_p}")

print("\nAll requested variants successfully rendered!")
