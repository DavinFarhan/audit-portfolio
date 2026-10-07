import fitz
import os

OUTPUT_DIR = "brand/executive_broad_variants"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Base geometry definitions on 1000x1000 canvas
def get_polygons_and_paths(top_facet_colors, bottom_blade_colors, stroke_color, stroke_w=14, hole_bg="#FFFFFF", node_color="#0B192C", slit_color="#FFFFFF"):
    c_top, c_ul, c_ur, c_ll, c_lr = top_facet_colors
    b_left, b_right = bottom_blade_colors
    
    return f"""
    <!-- Facet 1: Central Top Rhombus/Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" 
             fill="{c_top}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Facet 2: Upper Left Wing -->
    <polygon points="500,210 270,380 364.3,431.2" 
             fill="{c_ul}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Facet 3: Upper Right Wing -->
    <polygon points="500,210 635.7,431.2 730,380" 
             fill="{c_ur}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Facet 4: Lower Left Flank -->
    <polygon points="270,380 270,585 500,505 364.3,431.2" 
             fill="{c_ll}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Facet 5: Lower Right Flank -->
    <polygon points="730,380 635.7,431.2 500,505 730,585" 
             fill="{c_lr}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Left Blade -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" 
          fill="{b_left}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Right Blade -->
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" 
          fill="{b_right}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>
    <!-- Breather Hole Ring -->
    <circle cx="500" cy="625" r="32" fill="{hole_bg}"/>
    <!-- Cryptographic Verification Node -->
    <circle cx="500" cy="625" r="14" fill="{node_color}"/>
    <!-- Vertical Ink Slit -->
    <line x1="500" y1="657" x2="500" y2="810" stroke="{slit_color}" stroke-width="12" stroke-linecap="square"/>
    """

# ------------------------------------------------------------------------------
# 1. DARK MODE - SOLID DARK BACKGROUND (#0B192C)
# ------------------------------------------------------------------------------
# In dark backgrounds, the top facets use deep luxury platinum/navy facets
# with crisp white gutters, glowing amber blades, and an amber breather ring.
dark_bg_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#070E18" rx="0"/>
  <g id="executive_broad_dark">
    {get_polygons_and_paths(
        top_facet_colors=("#1E293B", "#162338", "#1A283D", "#0F1A2C", "#132136"),
        bottom_blade_colors=("#F59E0B", "#D97706"),
        stroke_color="#F8FAFC",
        stroke_w=14,
        hole_bg="#F8FAFC",
        node_color="#070E18",
        slit_color="#F8FAFC"
    )}
  </g>
</svg>"""

# ------------------------------------------------------------------------------
# 2. PURE PITCH BLACK (OLED / CYBER SECURITY THEME #000000)
# ------------------------------------------------------------------------------
pitch_black_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#000000"/>
  <g id="executive_broad_pitch_black">
    {get_polygons_and_paths(
        top_facet_colors=("#182234", "#111A28", "#151F30", "#0D1420", "#101825"),
        bottom_blade_colors=("#FBBF24", "#F59E0B"),
        stroke_color="#FFFFFF",
        stroke_w=16,
        hole_bg="#FFFFFF",
        node_color="#000000",
        slit_color="#FFFFFF"
    )}
  </g>
</svg>"""

# ------------------------------------------------------------------------------
# 3. TRANSPARENT CUTOUT (NO BACKGROUND - MASTER CUTOUT)
# ------------------------------------------------------------------------------
transparent_master_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="executive_broad_transparent">
    {get_polygons_and_paths(
        top_facet_colors=("#0B192C", "#0B192C", "#0B192C", "#0B192C", "#0B192C"),
        bottom_blade_colors=("#F59E0B", "#E08A00"),
        stroke_color="#FFFFFF",
        stroke_w=14,
        hole_bg="#FFFFFF",
        node_color="#0B192C",
        slit_color="#FFFFFF"
    )}
  </g>
</svg>"""

# ------------------------------------------------------------------------------
# 4. WATERMARK VARIATIONS (LOW OPACITY FOR PDF AUDIT REPORT BODY)
# ------------------------------------------------------------------------------
# Standard watermark opacities: 12% (very subtle behind text), 25% (balanced), 50% (standout)
def make_watermark(opacity_pct):
    op = opacity_pct / 100.0
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="executive_broad_watermark_{opacity_pct}" opacity="{op}">
    {get_polygons_and_paths(
        top_facet_colors=("#0B192C", "#0B192C", "#0B192C", "#0B192C", "#0B192C"),
        bottom_blade_colors=("#F59E0B", "#E08A00"),
        stroke_color="#FFFFFF",
        stroke_w=14,
        hole_bg="#FFFFFF",
        node_color="#0B192C",
        slit_color="#FFFFFF"
    )}
  </g>
</svg>"""

watermark_12_svg = make_watermark(12)
watermark_25_svg = make_watermark(25)
watermark_50_svg = make_watermark(50)

# ------------------------------------------------------------------------------
# 5. MONOCHROME PURE BLACK (FOR PHYSICAL DOCUMENT STAMP / B&W PRINT)
# ------------------------------------------------------------------------------
mono_black_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="executive_broad_mono_black">
    {get_polygons_and_paths(
        top_facet_colors=("#000000", "#111111", "#0A0A0A", "#1A1A1A", "#141414"),
        bottom_blade_colors=("#222222", "#000000"),
        stroke_color="#FFFFFF",
        stroke_w=16,
        hole_bg="#FFFFFF",
        node_color="#000000",
        slit_color="#FFFFFF"
    )}
  </g>
</svg>"""

# ------------------------------------------------------------------------------
# 6. MONOCHROME PURE WHITE (FOR DARK OVERLAYS / STAMPS ON DARK COVERS)
# ------------------------------------------------------------------------------
mono_white_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="executive_broad_mono_white">
    {get_polygons_and_paths(
        top_facet_colors=("#FFFFFF", "#F1F5F9", "#E2E8F0", "#CBD5E1", "#E2E8F0"),
        bottom_blade_colors=("#FFFFFF", "#E2E8F0"),
        stroke_color="#0B192C",
        stroke_w=16,
        hole_bg="#0B192C",
        node_color="#FFFFFF",
        slit_color="#0B192C"
    )}
  </g>
</svg>"""

# ------------------------------------------------------------------------------
# 7. DARK MODE STACKED (COVER REPORT PDF IN DARK MODE)
# ------------------------------------------------------------------------------
stacked_dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 960" width="800" height="960">
  <rect width="800" height="960" fill="#070E18"/>
  <g transform="translate(150, 40) scale(0.5)">
    {get_polygons_and_paths(
        top_facet_colors=("#1E293B", "#162338", "#1A283D", "#0F1A2C", "#132136"),
        bottom_blade_colors=("#F59E0B", "#D97706"),
        stroke_color="#F8FAFC",
        stroke_w=14,
        hole_bg="#F8FAFC",
        node_color="#070E18",
        slit_color="#F8FAFC"
    )}
  </g>
  <text x="400" y="580" text-anchor="middle"
        font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="800" font-size="64" fill="#F8FAFC" letter-spacing="3">FARHAN DAVIN</text>
  <text x="400" y="632" text-anchor="middle"
        font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="700" font-size="22" fill="#F59E0B" letter-spacing="7">SMART CONTRACT AUDITOR</text>
  <rect x="330" y="656" width="140" height="4" rx="2" fill="#F59E0B" opacity="0.6"/>
</svg>"""

# ------------------------------------------------------------------------------
# 8. DARK MODE HORIZONTAL (HEADER IN DARK MODE)
# ------------------------------------------------------------------------------
horizontal_dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480">
  <rect width="1440" height="480" fill="#070E18"/>
  <g transform="translate(60, 20) scale(0.44)">
    {get_polygons_and_paths(
        top_facet_colors=("#1E293B", "#162338", "#1A283D", "#0F1A2C", "#132136"),
        bottom_blade_colors=("#F59E0B", "#D97706"),
        stroke_color="#F8FAFC",
        stroke_w=14,
        hole_bg="#F8FAFC",
        node_color="#070E18",
        slit_color="#F8FAFC"
    )}
  </g>
  <text x="560" y="246" font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="800" font-size="88" fill="#F8FAFC" letter-spacing="2">FARHAN DAVIN</text>
  <text x="564" y="316" font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="700" font-size="30" fill="#F59E0B" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="564" y="342" width="140" height="4" rx="2" fill="#F59E0B" opacity="0.6"/>
</svg>"""

# Collection of all files to save
file_dict = {
    "nib-dark-solid.svg": dark_bg_svg,
    "nib-pitch-black.svg": pitch_black_svg,
    "nib-transparent-master.svg": transparent_master_svg,
    "nib-watermark-12.svg": watermark_12_svg,
    "nib-watermark-25.svg": watermark_25_svg,
    "nib-watermark-50.svg": watermark_50_svg,
    "nib-mono-black.svg": mono_black_svg,
    "nib-mono-white.svg": mono_white_svg,
    "nib-stacked-dark.svg": stacked_dark_svg,
    "nib-horizontal-dark.svg": horizontal_dark_svg,
}

print("Saving SVG variant files...")
for filename, svg_str in file_dict.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_str)
    print(f"  -> Saved {filename}")

# High-resolution rendering to PNG and Vector PDF
render_tasks = [
    ("nib-dark-solid.svg", "nib-dark-solid.png", "nib-dark-solid.pdf", 1000),
    ("nib-pitch-black.svg", "nib-pitch-black.png", "nib-pitch-black.pdf", 1000),
    ("nib-transparent-master.svg", "nib-transparent-master.png", "nib-transparent-master.pdf", 1000),
    ("nib-watermark-12.svg", "nib-watermark-12.png", "nib-watermark-12.pdf", 1000),
    ("nib-watermark-25.svg", "nib-watermark-25.png", "nib-watermark-25.pdf", 1000),
    ("nib-watermark-50.svg", "nib-watermark-50.png", "nib-watermark-50.pdf", 1000),
    ("nib-mono-black.svg", "nib-mono-black.png", "nib-mono-black.pdf", 1000),
    ("nib-mono-white.svg", "nib-mono-white.png", "nib-mono-white.pdf", 1000),
    ("nib-stacked-dark.svg", "nib-stacked-dark.png", "nib-stacked-dark.pdf", 1280),
    ("nib-horizontal-dark.svg", "nib-horizontal-dark.png", "nib-horizontal-dark.pdf", 1440),
]

print("\nRendering high-resolution PNGs and Vector PDFs...")
for svg_f, png_f, pdf_f, width in render_tasks:
    svg_p = os.path.join(OUTPUT_DIR, svg_f)
    png_p = os.path.join(OUTPUT_DIR, png_f)
    pdf_p = os.path.join(OUTPUT_DIR, pdf_f)
    
    doc = fitz.open(svg_p)
    pdf_bytes = doc.convert_to_pdf()
    with open(pdf_p, "wb") as f:
        f.write(pdf_bytes)
        
    page = doc[0]
    scale = width / page.rect.width
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(png_p)
    print(f"  -> Generated {png_f} ({pix.width}x{pix.height}) & {pdf_f}")

print("\nAll brand variants generated successfully!")
