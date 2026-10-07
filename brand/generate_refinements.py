import os
import fitz

BASE_DIR = 'brand/nib_refinements'
os.makedirs(BASE_DIR, exist_ok=True)

# Upper facets (identical across all versions)
def get_upper_facets(navy_fill="#0B192C", stroke_color="#FFFFFF"):
    return f"""
    <!-- 1. Central Top Rhombus/Spire -->
    <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" 
             fill="{navy_fill}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- 2. Upper Left Wing -->
    <polygon points="500,210 270,380 364.3,431.2" 
             fill="{navy_fill}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- 3. Upper Right Wing -->
    <polygon points="500,210 635.7,431.2 730,380" 
             fill="{navy_fill}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- 4. Lower Left Flank -->
    <polygon points="270,380 270,585 500,505 364.3,431.2" 
             fill="{navy_fill}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- 5. Lower Right Flank -->
    <polygon points="730,380 635.7,431.2 500,505 730,585" 
             fill="{navy_fill}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    """

def generate_svg(variant_id, bg_type):
    # Colors
    if bg_type == "white":
        bg_color = "#FFFFFF"
        stroke_color = "#FFFFFF"
        navy_fill = "#0B192C"
        outer_frame = False
    elif bg_type == "navy":
        bg_color = "#070E18"
        stroke_color = "#FFFFFF"
        navy_fill = "#0B192C"
        outer_frame = True
    elif bg_type == "black":
        bg_color = "#000000"
        stroke_color = "#FFFFFF"
        navy_fill = "#0B192C"
        outer_frame = True

    amber_left = "#F59E0B"
    amber_right = "#E08A00"

    outer_tag = ""
    if outer_frame:
        outer_tag = f'<polygon points="500,210 730,380 730,585 500,810 270,585 270,380" fill="none" stroke="{stroke_color}" stroke-width="14" stroke-linejoin="round"/>\n'

    facets = get_upper_facets(navy_fill, stroke_color)

    # 4 distinct treatments for the lower nib:
    if variant_id == "opt1_micro_circle":
        # Diameter 24 (r=12), pure white negative space, NO inner pupil
        nib_content = f"""
    <!-- Left Amber Blade with small arc -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,627 A 12 12 0 0 1 500,603 L 500,505 Z" 
          fill="{amber_left}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Right Amber Blade with small arc -->
    <path d="M 500,505 L 500,603 A 12 12 0 0 1 500,627 L 500,810 L 730,585 L 500,505 Z" 
          fill="{amber_right}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Pure Negative Space Breather Hole (NO PUPIL / NO INNER DOT) -->
    <circle cx="500" cy="615" r="12" fill="{stroke_color}"/>
    <!-- Mechanical Ink Slit -->
    <line x1="500" y1="627" x2="500" y2="810" stroke="{stroke_color}" stroke-width="7" stroke-linecap="square"/>
        """

    elif variant_id == "opt2_diamond_cut":
        # Diamond rhombus matching hexagonal facet angles (rhombus 18px wide, 24px high)
        nib_content = f"""
    <!-- Left Amber Blade with diamond notch -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,627 L 491,615 L 500,603 L 500,505 Z" 
          fill="{amber_left}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Right Amber Blade with diamond notch -->
    <path d="M 500,505 L 500,603 L 509,615 L 500,627 L 500,810 L 730,585 L 500,505 Z" 
          fill="{amber_right}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Diamond Breather Hole (Negative Space Rhombus) -->
    <polygon points="500,603 509,615 500,627 491,615" fill="{stroke_color}"/>
    <!-- Mechanical Ink Slit -->
    <line x1="500" y1="627" x2="500" y2="810" stroke="{stroke_color}" stroke-width="7" stroke-linecap="square"/>
        """

    elif variant_id == "opt3_pure_slit":
        # PURE MINIMAL SLIT: Zero holes. Just the razor-sharp vertical slit dividing two solid geometric amber blades.
        nib_content = f"""
    <!-- Left Solid Amber Blade -->
    <polygon points="500,505 270,585 500,810" 
             fill="{amber_left}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Right Solid Amber Blade -->
    <polygon points="500,505 500,810 730,585" 
             fill="{amber_right}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Pure Razor Slit from Center to Tip -->
    <line x1="500" y1="505" x2="500" y2="810" stroke="{stroke_color}" stroke-width="7" stroke-linecap="square"/>
        """

    elif variant_id == "opt4_classic_teardrop":
        # Inverted teardrop / heart nib breather hole
        nib_content = f"""
    <!-- Left Amber Blade with teardrop contour -->
    <path d="M 500,505 L 270,585 L 500,810 L 500,629 L 492,618 A 10 10 0 0 1 500,604 L 500,505 Z" 
          fill="{amber_left}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Right Amber Blade with teardrop contour -->
    <path d="M 500,505 L 500,604 A 10 10 0 0 1 508,618 L 500,629 L 500,810 L 730,585 L 500,505 Z" 
          fill="{amber_right}" stroke="{stroke_color}" stroke-width="7" stroke-linejoin="round"/>
    <!-- Teardrop Cutout (Negative Space) -->
    <path d="M 500,604 A 10 10 0 0 1 508,618 L 500,629 L 492,618 A 10 10 0 0 1 500,604 Z" fill="{stroke_color}"/>
    <!-- Mechanical Ink Slit -->
    <line x1="500" y1="629" x2="500" y2="810" stroke="{stroke_color}" stroke-width="7" stroke-linecap="square"/>
        """

    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="{bg_color}"/>
  <g id="{variant_id}">
    {outer_tag}
    {facets}
    {nib_content}
  </g>
</svg>"""
    return svg_str

variants = ["opt1_micro_circle", "opt2_diamond_cut", "opt3_pure_slit", "opt4_classic_teardrop"]
bg_types = ["white", "navy", "black"]

for var in variants:
    for bg in bg_types:
        filename = f"{var}_{bg}"
        svg_content = generate_svg(var, bg)
        svg_path = os.path.join(BASE_DIR, f"{filename}.svg")
        png_path = os.path.join(BASE_DIR, f"{filename}.png")
        
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
        doc = fitz.open(svg_path)
        page = doc[0]
        pix = page.get_pixmap(dpi=150)
        pix.save(png_path)

print("Generated all 12 refined SVGs and PNGs!")
