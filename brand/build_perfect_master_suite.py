import os
import fitz

BASE_DIR = 'brand/executive_suite'
os.makedirs(BASE_DIR, exist_ok=True)

def generate_perfect_svg(variant_type, bg_color=None, stroke_color="#FFFFFF", is_transparent=False, opacity=1.0):
    # Palette constants
    navy_color = "#0B192C"
    amber_left = "#F59E0B"
    amber_right = "#E08A00"
    
    # Monochrome adjustments
    if variant_type == "mono_black":
        navy_color = "#000000"
        amber_left = "#000000"
        amber_right = "#000000"
        stroke_color = "#FFFFFF"
    elif variant_type == "mono_white":
        navy_color = "#FFFFFF"
        amber_left = "#FFFFFF"
        amber_right = "#FFFFFF"
        stroke_color = "#000000"

    # Outer border for framed dark variants
    outer_border_tag = ""
    if variant_type in ["pitch_black_framed", "navy_framed", "emerald_framed"]:
        outer_stroke = stroke_color
        # Outer hexagon perimeter with stroke 14 centered (7 inside, 7 outside)
        # Using <path d="... Z"> guarantees PyMuPDF/Fitz closes the top apex completely and symmetrically!
        outer_border_tag = f'<path d="M 500,210 L 730,380 L 730,585 L 500,810 L 270,585 L 270,380 Z" fill="none" stroke="{outer_stroke}" stroke-width="14" stroke-linejoin="round"/>'

    # Background rect
    bg_tag = ""
    if not is_transparent and bg_color:
        bg_tag = f'<rect width="1000" height="1000" fill="{bg_color}"/>'

    opacity_attr = f' opacity="{opacity}"' if opacity < 1.0 else ''

    # Breather diamond fill: matches stroke color (solid crisp white negative space matching the slit lines)
    diamond_fill = stroke_color

    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000"{opacity_attr}>
  {bg_tag}
  <g id="executive_broad_perfect">
    <!-- 1. SOLID FACET FILLS (Seamless underlying mesh, no stroke clipping) -->
    <g id="facet_fills">
      <!-- Central Top Spire -->
      <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="{navy_color}"/>
      <!-- Upper Left Wing (Exact reflection of Right Wing) -->
      <polygon points="500,210 270,380 364.3,431.2" fill="{navy_color}"/>
      <!-- Upper Right Wing -->
      <polygon points="500,210 730,380 635.7,431.2" fill="{navy_color}"/>
      <!-- Lower Left Flank (Exact reflection of Right Flank) -->
      <polygon points="270,380 270,585 500,505 364.3,431.2" fill="{navy_color}"/>
      <!-- Lower Right Flank -->
      <polygon points="730,380 730,585 500,505 635.7,431.2" fill="{navy_color}"/>
      <!-- Left Amber Blade with enlarged diamond notch (w=40, h=52) -->
      <path d="M 500,505 L 270,585 L 500,810 L 500,644 L 480,618 L 500,592 L 500,505 Z" fill="{amber_left}"/>
      <!-- Right Amber Blade with enlarged diamond notch (w=40, h=52) -->
      <path d="M 500,505 L 730,585 L 500,810 L 500,644 L 520,618 L 500,592 L 500,505 Z" fill="{amber_right}"/>
    </g>

    <!-- 2. UNIFORM ARCHITECTURAL LINES (Drawn on top with exact 7px width & mathematical symmetry) -->
    <g id="facet_lines" stroke="{stroke_color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
      <!-- Enlarged Diamond Breather Hole Cutout (Scale 2.2: width 40, height 52) -->
      <polygon points="500,592 520,618 500,644 480,618" fill="{diamond_fill}" stroke="none"/>
      
      <!-- Central Spire Diagonals (Left & Right exact mirror) -->
      <line x1="500" y1="210" x2="364.3" y2="431.2"/>
      <line x1="500" y1="210" x2="635.7" y2="431.2"/>
      
      <!-- Wing to Flank Dividers (Left & Right exact mirror) -->
      <line x1="270" y1="380" x2="364.3" y2="431.2"/>
      <line x1="730" y1="380" x2="635.7" y2="431.2"/>
      
      <!-- Flank to Spire Dividers (Left & Right exact mirror) -->
      <line x1="364.3" y1="431.2" x2="500" y2="505"/>
      <line x1="635.7" y1="431.2" x2="500" y2="505"/>
      
      <!-- Navy Flank to Amber Blade Dividers (Left & Right exact mirror) -->
      <line x1="270" y1="585" x2="500" y2="505"/>
      <line x1="730" y1="585" x2="500" y2="505"/>
      
      <!-- Vertical Slit: Upper section & Lower section to nib tip -->
      <line x1="500" y1="505" x2="500" y2="592"/>
      <line x1="500" y1="644" x2="500" y2="810" stroke-linecap="square"/>
    </g>

    <!-- 3. OPTIONAL OUTER FRAME FOR DARK VARIANTS -->
    {outer_border_tag}
  </g>
</svg>"""
    return svg_str

# Configurations for master suite
configs = [
    ("nib-master-white", "master_white", "#FFFFFF", "#FFFFFF", False, 1.0),
    ("nib-master-transparent", "master_transparent", None, "#FFFFFF", True, 1.0),
    ("nib-dark-pitch-black-framed", "pitch_black_framed", "#000000", "#FFFFFF", False, 1.0),
    ("nib-dark-navy-framed", "navy_framed", "#070E18", "#FFFFFF", False, 1.0),
    ("nib-dark-floating", "dark_floating", "#070E18", "#FFFFFF", False, 1.0),
    ("nib-watermark-10pct", "watermark", None, "#FFFFFF", True, 0.10),
    ("nib-watermark-25pct", "watermark", None, "#FFFFFF", True, 0.25),
    ("nib-watermark-50pct", "watermark", None, "#FFFFFF", True, 0.50),
    ("nib-monochrome-black", "mono_black", "#FFFFFF", "#FFFFFF", False, 1.0),
    ("nib-monochrome-white", "mono_white", "#000000", "#000000", False, 1.0),
]

for name, vtype, bg, stroke, trans, op in configs:
    svg_code = generate_perfect_svg(vtype, bg, stroke, trans, op)
    svg_file = os.path.join(BASE_DIR, f"{name}.svg")
    pdf_file = os.path.join(BASE_DIR, f"{name}.pdf")
    png_file = os.path.join(BASE_DIR, f"{name}.png")
    
    with open(svg_file, 'w', encoding='utf-8') as f:
        f.write(svg_code)
        
    doc = fitz.open(stream=svg_code.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(png_file)
    
    # Save vector PDF
    pdf_bytes = doc.convert_to_pdf()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    pdf_doc.save(pdf_file)

# Lockup configurations
def generate_lockup_svg(layout, mode):
    if mode == 'dark':
        bg_col = "#070E18"
        text_primary = "#F8FAFC"
        text_sub = "#F59E0B"
        sym_svg = generate_perfect_svg("navy_framed", bg_color=None, stroke_color="#FFFFFF", is_transparent=True)
    else:
        bg_col = "#FFFFFF"
        text_primary = "#0B192C"
        text_sub = "#D97706"
        sym_svg = generate_perfect_svg("master_white", bg_color=None, stroke_color="#FFFFFF", is_transparent=True)
    
    inner_symbol = sym_svg[sym_svg.find('<g id="executive_broad_perfect">'):sym_svg.rfind('</svg>')]
    
    if layout == 'stacked':
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">
  <rect width="800" height="800" fill="{bg_col}"/>
  <g transform="translate(150, 40) scale(0.5)">
    {inner_symbol}
  </g>
  <text x="400" y="580" text-anchor="middle" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="800" font-size="64" fill="{text_primary}" letter-spacing="3">FARHAN DAVIN</text>
  <text x="400" y="632" text-anchor="middle" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="700" font-size="22" fill="{text_sub}" letter-spacing="7">SMART CONTRACT AUDITOR</text>
  <rect x="330" y="656" width="140" height="4" rx="2" fill="{text_sub}" opacity="0.6"/>
</svg>"""
    elif layout == 'horizontal':
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480">
  <rect width="1440" height="480" fill="{bg_col}"/>
  <g transform="translate(60, 20) scale(0.44)">
    {inner_symbol}
  </g>
  <text x="560" y="246" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="800" font-size="88" fill="{text_primary}" letter-spacing="2">FARHAN DAVIN</text>
  <text x="564" y="316" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="700" font-size="30" fill="{text_sub}" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="564" y="342" width="140" height="4" rx="2" fill="{text_sub}" opacity="0.6"/>
</svg>"""

lockup_configs = [
    ("nib-stacked-dark", "stacked", "dark"),
    ("nib-horizontal-dark", "horizontal", "dark"),
    ("nib-stacked-light", "stacked", "light"),
    ("nib-horizontal-light", "horizontal", "light"),
]

for name, layout, mode in lockup_configs:
    svg_code = generate_lockup_svg(layout, mode)
    svg_file = os.path.join(BASE_DIR, f"{name}.svg")
    pdf_file = os.path.join(BASE_DIR, f"{name}.pdf")
    png_file = os.path.join(BASE_DIR, f"{name}.png")
    
    with open(svg_file, 'w', encoding='utf-8') as f:
        f.write(svg_code)
        
    doc = fitz.open(stream=svg_code.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(png_file)
    
    pdf_bytes = doc.convert_to_pdf()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    pdf_doc.save(pdf_file)

print("Generated all perfected master suite assets including lockups!")
