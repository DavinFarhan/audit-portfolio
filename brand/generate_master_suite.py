import fitz
import os

OUTPUT_DIR = "brand/executive_suite"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_svg(
    bg_color=None,
    top_navy="#0B192C",
    blade_left="#F59E0B",
    blade_right="#E08A00",
    gutter_color="#FFFFFF",
    gutter_width=10,
    outer_border=False,
    hole_bg="#FFFFFF",
    node_color="#0B192C",
    opacity=1.0,
    width=1000,
    height=1000
):
    bg_tag = f'<rect width="{width}" height="{height}" fill="{bg_color}"/>' if bg_color else ''
    
    border_tag = ""
    if outer_border and gutter_color:
        border_tag = f'<polygon points="500,210 730,380 730,585 500,810 270,585 270,380" fill="none" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linejoin="round"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  {bg_tag}
  <g id="executive_broad" opacity="{opacity}">
    <!-- 1. Central Top Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="{top_navy}"/>
    
    <!-- 2. Upper Left Wing -->
    <polygon points="500,210 270,380 364.3,431.2" fill="{top_navy}"/>
    
    <!-- 3. Upper Right Wing -->
    <polygon points="500,210 635.7,431.2 730,380" fill="{top_navy}"/>
    
    <!-- 4. Lower Left Flank -->
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="{top_navy}"/>
    
    <!-- 5. Lower Right Flank -->
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="{top_navy}"/>

    <!-- Left Blade -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,651 A 26 26 0 0 1 500,599 L 500,505 Z" fill="{blade_left}"/>

    <!-- Right Blade -->
    <path d="M 500,505 L 500,599 A 26 26 0 0 1 500,651 L 500,810 L 730,585 L 500,505 Z" fill="{blade_right}"/>

    <!-- Internal Facet Crease Lines -->
    <line x1="500" y1="210" x2="364.3" y2="431.2" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="500" y1="210" x2="635.7" y2="431.2" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="364.3" y1="431.2" x2="500" y2="505" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="635.7" y1="431.2" x2="500" y2="505" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="270" y1="380" x2="364.3" y2="431.2" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="730" y1="380" x2="635.7" y2="431.2" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="270" y1="585" x2="500" y2="505" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
    <line x1="500" y1="505" x2="730" y2="585" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>

    {border_tag}

    <!-- Breather Hole Ring -->
    <circle cx="500" cy="625" r="28" fill="{hole_bg}"/>
    
    <!-- Cryptographic Verification Node -->
    <circle cx="500" cy="625" r="12" fill="{node_color}"/>

    <!-- Vertical Ink Slit -->
    <line x1="500" y1="653" x2="500" y2="810" stroke="{gutter_color}" stroke-width="{gutter_width}" stroke-linecap="round"/>
  </g>
</svg>"""

# Full Master Suite Definitions
suite = {
    # 1. Dark Mode: Pitch Black (#000000) dengan White Framing (Bercahaya di Hitam Pekat)
    "nib-dark-pitch-black-framed.svg": generate_svg(
        bg_color="#000000",
        top_navy="#111D30",
        blade_left="#F59E0B",
        blade_right="#D97706",
        gutter_color="#FFFFFF",
        gutter_width=12,
        outer_border=True,
        hole_bg="#FFFFFF",
        node_color="#000000"
    ),

    # 2. Dark Mode: Dark Navy Background (#070E18) dengan White Framing
    "nib-dark-navy-framed.svg": generate_svg(
        bg_color="#070E18",
        top_navy="#13233A",
        blade_left="#F59E0B",
        blade_right="#D97706",
        gutter_color="#FFFFFF",
        gutter_width=12,
        outer_border=True,
        hole_bg="#FFFFFF",
        node_color="#070E18"
    ),

    # 3. Dark Mode Floating (Tanpa Border Luar, Siluet Murni di Dark Background)
    "nib-dark-floating.svg": generate_svg(
        bg_color="#0A111E",
        top_navy="#182A45",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        gutter_color="#FFFFFF",
        gutter_width=10,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0A111E"
    ),

    # 4. Master Transparent Cutout (100% Bersih, Tanpa Background)
    "nib-master-transparent.svg": generate_svg(
        bg_color=None,
        top_navy="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        gutter_color="#FFFFFF",
        gutter_width=10,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0B192C"
    ),

    # 5. Master White Canvas (Sesuai Upload Pengguna)
    "nib-master-white.svg": generate_svg(
        bg_color="#FFFFFF",
        top_navy="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        gutter_color="#FFFFFF",
        gutter_width=10,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0B192C"
    ),

    # 6. Watermark 10% (Sangat Halus di Balik Teks Laporan PDF)
    "nib-watermark-10pct.svg": generate_svg(
        bg_color=None,
        top_navy="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        gutter_color="#FFFFFF",
        gutter_width=10,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0B192C",
        opacity=0.10
    ),

    # 7. Watermark 25% (Medium untuk Halaman Cover / Slide Transparan)
    "nib-watermark-25pct.svg": generate_svg(
        bg_color=None,
        top_navy="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        gutter_color="#FFFFFF",
        gutter_width=10,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0B192C",
        opacity=0.25
    ),

    # 8. Watermark 50% (Semi-Transparan)
    "nib-watermark-50pct.svg": generate_svg(
        bg_color=None,
        top_navy="#0B192C",
        blade_left="#F59E0B",
        blade_right="#E08A00",
        gutter_color="#FFFFFF",
        gutter_width=10,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0B192C",
        opacity=0.50
    ),

    # 9. Monokrom Hitam Murni (Untuk Cap Stempel Resmi Dokumen Fisik / Cetak B&W)
    "nib-monochrome-black.svg": generate_svg(
        bg_color=None,
        top_navy="#0F172A",
        blade_left="#334155",
        blade_right="#0F172A",
        gutter_color="#FFFFFF",
        gutter_width=12,
        outer_border=False,
        hole_bg="#FFFFFF",
        node_color="#0F172A"
    ),

    # 10. Monokrom Putih Murni (Untuk Watermark Gelap / Overlay Video / Dark BG)
    "nib-monochrome-white.svg": generate_svg(
        bg_color=None,
        top_navy="#FFFFFF",
        blade_left="#E2E8F0",
        blade_right="#CBD5E1",
        gutter_color="#0B192C",
        gutter_width=12,
        outer_border=False,
        hole_bg="#0B192C",
        node_color="#FFFFFF"
    ),

    # 11. Emerald Verified Dark Mode (Hijau Audit Passed di Latar Gelap)
    "nib-dark-emerald-framed.svg": generate_svg(
        bg_color="#070E18",
        top_navy="#13233A",
        blade_left="#10B981",
        blade_right="#059669",
        gutter_color="#FFFFFF",
        gutter_width=12,
        outer_border=True,
        hole_bg="#FFFFFF",
        node_color="#070E18"
    ),
}

# Typography helpers for Stacked & Horizontal in Dark Mode & Light Mode
stacked_dark_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 960" width="800" height="960">
  <rect width="800" height="960" fill="#070E18"/>
  <g transform="translate(150, 40) scale(0.5)">
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#13233A"/>
    <polygon points="500,210 270,380 364.3,431.2" fill="#0E1B2E"/>
    <polygon points="500,210 635.7,431.2 730,380" fill="#0E1B2E"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="#182B46"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="#182B46"/>
    <path d="M 500,505 L 270,585 L 500,810 L 500,651 A 26 26 0 0 1 500,599 L 500,505 Z" fill="#F59E0B"/>
    <path d="M 500,505 L 500,599 A 26 26 0 0 1 500,651 L 500,810 L 730,585 L 500,505 Z" fill="#D97706"/>
    <line x1="500" y1="210" x2="364.3" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="500" y1="210" x2="635.7" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="364.3" y1="431.2" x2="500" y2="505" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="635.7" y1="431.2" x2="500" y2="505" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="270" y1="380" x2="364.3" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="730" y1="380" x2="635.7" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="270" y1="585" x2="500" y2="505" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="500" y1="505" x2="730" y2="585" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <polygon points="500,210 730,380 730,585 500,810 270,585 270,380" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="28" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="12" fill="#070E18"/>
    <line x1="500" y1="653" x2="500" y2="810" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  </g>
  <text x="400" y="580" text-anchor="middle" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="800" font-size="64" fill="#F8FAFC" letter-spacing="3">FARHAN DAVIN</text>
  <text x="400" y="632" text-anchor="middle" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="700" font-size="22" fill="#F59E0B" letter-spacing="7">SMART CONTRACT AUDITOR</text>
  <rect x="330" y="656" width="140" height="4" rx="2" fill="#F59E0B" opacity="0.6"/>
</svg>"""

horizontal_dark_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480">
  <rect width="1440" height="480" fill="#070E18"/>
  <g transform="translate(60, 20) scale(0.44)">
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#13233A"/>
    <polygon points="500,210 270,380 364.3,431.2" fill="#0E1B2E"/>
    <polygon points="500,210 635.7,431.2 730,380" fill="#0E1B2E"/>
    <polygon points="270,380 270,585 500,505 364.3,431.2" fill="#182B46"/>
    <polygon points="730,380 635.7,431.2 500,505 730,585" fill="#182B46"/>
    <path d="M 500,505 L 270,585 L 500,810 L 500,651 A 26 26 0 0 1 500,599 L 500,505 Z" fill="#F59E0B"/>
    <path d="M 500,505 L 500,599 A 26 26 0 0 1 500,651 L 500,810 L 730,585 L 500,505 Z" fill="#D97706"/>
    <line x1="500" y1="210" x2="364.3" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="500" y1="210" x2="635.7" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="364.3" y1="431.2" x2="500" y2="505" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="635.7" y1="431.2" x2="500" y2="505" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="270" y1="380" x2="364.3" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="730" y1="380" x2="635.7" y2="431.2" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="270" y1="585" x2="500" y2="505" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <line x1="500" y1="505" x2="730" y2="585" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
    <polygon points="500,210 730,380 730,585 500,810 270,585 270,380" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linejoin="round"/>
    <circle cx="500" cy="625" r="28" fill="#FFFFFF"/>
    <circle cx="500" cy="625" r="12" fill="#070E18"/>
    <line x1="500" y1="653" x2="500" y2="810" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  </g>
  <text x="560" y="246" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="800" font-size="88" fill="#F8FAFC" letter-spacing="2">FARHAN DAVIN</text>
  <text x="564" y="316" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="700" font-size="30" fill="#F59E0B" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="564" y="342" width="140" height="4" rx="2" fill="#F59E0B" opacity="0.6"/>
</svg>"""

suite["nib-stacked-dark.svg"] = stacked_dark_code
suite["nib-horizontal-dark.svg"] = horizontal_dark_code

print("Writing SVG suite files...")
for fname, content in suite.items():
    p = os.path.join(OUTPUT_DIR, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {fname}")

# Render PNG & PDF
print("\nRendering high-res PNGs and Vector PDFs...")
for fname in suite.keys():
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

print("\nExecutive Broad Master Suite successfully generated!")
