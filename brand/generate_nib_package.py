import fitz
import os

OUTPUT_DIR = "brand/executive_broad"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. ORIGINAL VERSION (EXACTLY AS UPLOADED BY USER)
# ------------------------------------------------------------------------------
original_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="sample_2_executive_broad">
    <!-- 1. Central Top Rhombus/Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- 2. Upper Left Wing -->
    <polygon points="500,210 270,380 364.3,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- 3. Upper Right Wing -->
    <polygon points="500,210 635.7,431.2 730,380" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- 4. Lower Left Flank -->
    <polygon points="270,380 270,585 500,505 364.3,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- 5. Lower Right Flank -->
    <polygon points="730,380 635.7,431.2 500,505 730,585" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- Left Amber Blade -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,651 A 26 26 0 0 1 500,599 L 500,505 Z" 
          fill="#F59E0B" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- Right Amber Blade -->
    <path d="M 500,505 L 500,599 A 26 26 0 0 1 500,651 L 500,810 L 730,585 L 500,505 Z" 
          fill="#E08A00" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
    <!-- Breather Hole Ring -->
    <circle cx="500" cy="625" r="26" fill="#FFFFFF"/>
    <!-- Verification Node -->
    <circle cx="500" cy="625" r="10" fill="#0B192C"/>
    <!-- Vertical Ink Slit -->
    <line x1="500" y1="651" x2="500" y2="810" stroke="#FFFFFF" stroke-width="7" stroke-linecap="square"/>
  </g>
</svg>
"""

# ------------------------------------------------------------------------------
# 2. OPTICALLY OPTIMIZED VERSION (SCALABLE TO 16PX FAVICON & BILLBOARDS)
# ------------------------------------------------------------------------------
# Key Improvements:
# - Gutter stroke increased from 7px to 14px for crystal-clear facet separation at small sizes
# - Breather hole enlarged to r=32 (inner r=14) for high-impact visual recognition
# - Slit stroke increased to 12px
# - Centered bounding box in canvas
optimized_amber_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="executive_broad_optimized">
    <!-- Central Top Rhombus/Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Upper Left Wing -->
    <polygon points="500,210 270,380 364.3,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Upper Right Wing -->
    <polygon points="500,210 635.7,431.2 730,380" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Lower Left Flank -->
    <polygon points="270,380 270,585 500,505 364.3,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Lower Right Flank -->
    <polygon points="730,380 635.7,431.2 500,505 730,585" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Left Amber Blade -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" 
          fill="#F59E0B" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Right Amber Blade -->
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" 
          fill="#E08A00" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Breather Hole Ring -->
    <circle cx="500" cy="625" r="32" fill="#FFFFFF"/>
    <!-- Cryptographic Verification Node -->
    <circle cx="500" cy="625" r="14" fill="#0B192C"/>
    <!-- Vertical Ink Slit -->
    <line x1="500" y1="657" x2="500" y2="810" stroke="#FFFFFF" stroke-width="12" stroke-linecap="square"/>
  </g>
</svg>
"""

# ------------------------------------------------------------------------------
# 3. EMERALD SECURITY VERIFIED EDITION (WARM AMBER -> VERIFIED EMERALD)
# ------------------------------------------------------------------------------
optimized_emerald_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <g id="executive_broad_emerald">
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 270,380 364.3,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 635.7,431.2 730,380" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" 
             fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Left Emerald Blade -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" 
          fill="#10B981" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <!-- Right Emerald Blade -->
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" 
          fill="#059669" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="32" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="14" fill="#0B192C"/>
    <line x1="500" y1="657" x2="500" y2="810" stroke="#FFFFFF" stroke-width="12" stroke-linecap="square"/>
  </g>
</svg>
"""

# ------------------------------------------------------------------------------
# 4. STACKED LOGO FOR PDF REPORT COVER (AMBER)
# ------------------------------------------------------------------------------
stacked_amber_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 960" width="800" height="960">
  <g transform="translate(150, 40) scale(0.5)">
    <!-- Central Top Rhombus/Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 270,380 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 635.7,431.2 730,380" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" fill="#F59E0B" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" fill="#E08A00" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="32" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="14" fill="#0B192C"/>
    <line x1="500" y1="657" x2="500" y2="810" stroke="#FFFFFF" stroke-width="12" stroke-linecap="square"/>
  </g>
  <!-- Wordmark Centered at x=400 -->
  <text x="400" y="580" text-anchor="middle"
        font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="800" font-size="64" fill="#0B192C" letter-spacing="3">FARHAN DAVIN</text>
  <text x="400" y="632" text-anchor="middle"
        font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="700" font-size="22" fill="#F59E0B" letter-spacing="7">SMART CONTRACT AUDITOR</text>
  <rect x="330" y="656" width="140" height="4" rx="2" fill="#0B192C" opacity="0.25"/>
</svg>
"""

# ------------------------------------------------------------------------------
# 5. HORIZONTAL LOGO FOR HEADER / WEBSITE / BANNER
# ------------------------------------------------------------------------------
horizontal_amber_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480">
  <g transform="translate(60, 20) scale(0.44)">
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 270,380 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="500,210 635.7,431.2 730,380" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 270,585 L 500,810 L 500,657 A 32 32 0 0 1 500,593 L 500,505 Z" fill="#F59E0B" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 500,505 L 500,593 A 32 32 0 0 1 500,657 L 500,810 L 730,585 L 500,505 Z" fill="#E08A00" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="32" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="14" fill="#0B192C"/>
    <line x1="500" y1="657" x2="500" y2="810" stroke="#FFFFFF" stroke-width="12" stroke-linecap="square"/>
  </g>
  <text x="560" y="246" font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="800" font-size="88" fill="#0B192C" letter-spacing="2">FARHAN DAVIN</text>
  <text x="564" y="316" font-family="'Inter', 'Montserrat', -apple-system, sans-serif"
        font-weight="700" font-size="30" fill="#F59E0B" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="564" y="342" width="140" height="4" rx="2" fill="#0B192C" opacity="0.3"/>
</svg>
"""

# Map to write and render
assets = {
    "nib-original.svg": original_svg,
    "nib-optimized-amber.svg": optimized_amber_svg,
    "nib-optimized-emerald.svg": optimized_emerald_svg,
    "nib-stacked-amber.svg": stacked_amber_svg,
    "nib-horizontal-amber.svg": horizontal_amber_svg,
}

for name, content in assets.items():
    p = os.path.join(OUTPUT_DIR, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

# Render PNG and PDF
renders = [
    ("nib-original.svg", "nib-original.png", "nib-original.pdf", 1000),
    ("nib-optimized-amber.svg", "nib-optimized-amber.png", "nib-optimized-amber.pdf", 1000),
    ("nib-optimized-emerald.svg", "nib-optimized-emerald.png", "nib-optimized-emerald.pdf", 1000),
    ("nib-stacked-amber.svg", "nib-stacked-amber.png", "nib-stacked-amber.pdf", 1280),
    ("nib-horizontal-amber.svg", "nib-horizontal-amber.png", "nib-horizontal-amber.pdf", 1440),
]

for s_name, p_name, pdf_name, width in renders:
    sp = os.path.join(OUTPUT_DIR, s_name)
    pp = os.path.join(OUTPUT_DIR, p_name)
    pdfp = os.path.join(OUTPUT_DIR, pdf_name)
    
    doc = fitz.open(sp)
    with open(pdfp, "wb") as f:
        f.write(doc.convert_to_pdf())
    
    page = doc[0]
    scale = width / page.rect.width
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(pp)
    print(f"Rendered {p_name} & {pdf_name}")

print("Executive Broad Nib asset package generated successfully!")
