import os
import fitz

OUTPUT_DIR = "brand"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. PURE SYMBOL (STANDALONE LOGOMARK)
# Dimensions: 512x512
# Geometry:
# - Open Shield with balanced crown aperture
# - Verified Ray checkmark surging dynamically upwards and breaking the right shield barrier
# - Vector knock-out band ensuring clean negative space gap around the checkmark
symbol_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Open Aegis &amp; Verified Ray Symbol">
  <title>Open Aegis &amp; Verified Ray Symbol</title>
  <defs>
    <!-- Knock-out negative space band around the checkmark's rising stroke -->
    <clipPath id="aegis-cut">
      <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
               M334 326 L524 140 L482 96 L292 282 Z"/>
    </clipPath>
  </defs>
  <!-- Open Aegis (Transparent & Honest Wireframe, Faithful Shield, Open Welcoming Aperture) -->
  <path clip-path="url(#aegis-cut)"
        d="M232 64 L96 112 V254 C96 358 166 428 256 464 C346 428 416 358 416 254 V112 L280 64"
        fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Verified Ray (Dynamic Checkmark: Verifiable, High-Quality, Keeping Promises) -->
  <polyline points="166,270 236,340 464,120"
            fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 2. MONOCHROME SYMBOL (SINGLE COLOR NAVY)
symbol_mono_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Open Aegis &amp; Verified Ray Symbol Monochrome">
  <title>Open Aegis &amp; Verified Ray Symbol - Monochrome</title>
  <defs>
    <clipPath id="aegis-cut-mono">
      <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
               M334 326 L524 140 L482 96 L292 282 Z"/>
    </clipPath>
  </defs>
  <path clip-path="url(#aegis-cut-mono)"
        d="M232 64 L96 112 V254 C96 358 166 428 256 464 C346 428 416 358 416 254 V112 L280 64"
        fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="166,270 236,340 464,120"
            fill="none" stroke="#0B1F3A" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 3. DARK MODE / INVERTED SYMBOL (WHITE & EMERALD ON DARK BACKGROUNDS)
symbol_dark_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Open Aegis &amp; Verified Ray Symbol Dark">
  <title>Open Aegis &amp; Verified Ray Symbol - Dark Mode</title>
  <defs>
    <clipPath id="aegis-cut-dark">
      <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
               M334 326 L524 140 L482 96 L292 282 Z"/>
    </clipPath>
  </defs>
  <path clip-path="url(#aegis-cut-dark)"
        d="M232 64 L96 112 V254 C96 358 166 428 256 464 C346 428 416 358 416 254 V112 L280 64"
        fill="none" stroke="#F8FAFC" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="166,270 236,340 464,120"
            fill="none" stroke="#10B981" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 4. HORIZONTAL LOGO (SYMBOL + FARHAN DAVIN / SMART CONTRACT AUDITOR)
# Width: 1440, Height: 480
# Clean side-by-side alignment, ideal for document headers, website navbars, and LinkedIn banners.
logo_horizontal_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480" role="img" aria-label="Farhan Davin - Smart Contract Auditor">
  <title>Farhan Davin - Smart Contract Auditor</title>
  <g transform="translate(30, -16)">
    <defs>
      <clipPath id="aegis-cut-h">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M334 326 L524 140 L482 96 L292 282 Z"/>
      </clipPath>
    </defs>
    <!-- Open Aegis -->
    <path clip-path="url(#aegis-cut-h)"
          d="M232 64 L96 112 V254 C96 358 166 428 256 464 C346 428 416 358 416 254 V112 L280 64"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Verified Ray -->
    <polyline points="166,270 236,340 464,120"
              fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <!-- Wordmark Section -->
  <text x="540" y="246" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="88" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="544" y="316" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="30" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <!-- Subtle Trust Accent Bar -->
  <rect x="544" y="342" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.3"/>
</svg>
"""

# 5. STACKED LOGO (SYMBOL ON TOP, WORDMARK BELOW)
# Width: 640, Height: 720
# Perfect for Audit Report PDF Cover Page (Centered title page composition)
logo_stacked_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 720" width="640" height="720" role="img" aria-label="Farhan Davin - Smart Contract Auditor">
  <title>Farhan Davin - Smart Contract Auditor</title>
  <!-- Centered Symbol (Symbol width 512, offset = (640-512)/2 = 64) -->
  <g transform="translate(64, 20)">
    <defs>
      <clipPath id="aegis-cut-st">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M334 326 L524 140 L482 96 L292 282 Z"/>
      </clipPath>
    </defs>
    <!-- Open Aegis -->
    <path clip-path="url(#aegis-cut-st)"
          d="M232 64 L96 112 V254 C96 358 166 428 256 464 C346 428 416 358 416 254 V112 L280 64"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Verified Ray -->
    <polyline points="166,270 236,340 464,120"
              fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <!-- Wordmark Section Centered at x=320 -->
  <text x="320" y="595" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="82" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="320" y="652" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="28" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <!-- Balanced Anchor Accent Bar -->
  <rect x="250" y="675" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.25"/>
</svg>
"""

# 6. MONOCHROME STACKED LOGO
logo_stacked_mono_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 720" width="640" height="720" role="img" aria-label="Farhan Davin - Smart Contract Auditor Monochrome">
  <title>Farhan Davin - Smart Contract Auditor - Monochrome</title>
  <g transform="translate(64, 20)">
    <defs>
      <clipPath id="aegis-cut-stm">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M334 326 L524 140 L482 96 L292 282 Z"/>
      </clipPath>
    </defs>
    <path clip-path="url(#aegis-cut-stm)"
          d="M232 64 L96 112 V254 C96 358 166 428 256 464 C346 428 416 358 416 254 V112 L280 64"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="166,270 236,340 464,120"
              fill="none" stroke="#0B1F3A" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="320" y="595" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="82" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="320" y="652" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="28" fill="#0B1F3A" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="250" y="675" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.3"/>
</svg>
"""

# Map of assets to save
svg_assets = {
    "audit-symbol.svg": symbol_svg,
    "audit-symbol-mono.svg": symbol_mono_svg,
    "audit-symbol-dark.svg": symbol_dark_svg,
    "audit-logo-horizontal.svg": logo_horizontal_svg,
    "audit-logo-stacked.svg": logo_stacked_svg,
    "audit-logo-stacked-mono.svg": logo_stacked_mono_svg,
}

print("Writing SVG assets...")
for filename, content in svg_assets.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {filepath}")

# Generate PDF and High-Res PNG (1024px+ / 300 DPI) using PyMuPDF (fitz)
raster_and_pdf_targets = [
    ("audit-symbol.svg", "audit-symbol.png", "audit-symbol.pdf", 1024),
    ("audit-symbol-mono.svg", "audit-symbol-mono.png", "audit-symbol-mono.pdf", 1024),
    ("audit-symbol-dark.svg", "audit-symbol-dark.png", "audit-symbol-dark.pdf", 1024),
    ("audit-logo-horizontal.svg", "audit-logo-horizontal.png", "audit-logo-horizontal.pdf", 1600),
    ("audit-logo-stacked.svg", "audit-logo-stacked.png", "audit-logo-stacked.pdf", 1280),
    ("audit-logo-stacked-mono.svg", "audit-logo-stacked-mono.png", "audit-logo-stacked-mono.pdf", 1280),
]

print("\nRendering high-res PNGs and Vector PDFs...")
for svg_name, png_name, pdf_name, target_width in raster_and_pdf_targets:
    svg_path = os.path.join(OUTPUT_DIR, svg_name)
    png_path = os.path.join(OUTPUT_DIR, png_name)
    pdf_path = os.path.join(OUTPUT_DIR, pdf_name)

    # Open with fitz
    doc = fitz.open(svg_path)
    
    # Export vector PDF
    pdf_bytes = doc.convert_to_pdf()
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    
    # Calculate scale for target_width PNG
    page = doc[0]
    rect = page.rect
    scale = target_width / rect.width
    mat = fitz.Matrix(scale, scale)
    
    # Render crisp transparent PNG
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(png_path)
    
    print(f"  -> Generated {png_path} ({pix.width}x{pix.height}) & {pdf_path}")

print("\nAsset generation finished successfully!")
