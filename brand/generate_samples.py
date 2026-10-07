import fitz
import os

OUTPUT_DIR = "brand/samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# SAMPLE A: "OPEN AEGIS REFINED" (GENTLE APERTURE & VERIFIED RAY)
# -------------------------------------------------------------
# Fitur:
# - Bahu atas perisai melengkung lembut (softer golden arc), menghilangkan kekakuan sudut
# - Bukaan mahkota atas lebih lapang dan ramah (welcoming aperture = murah hati & mempermudah)
# - Garis centang emerald presisi dengan knockout gap 18px sempurna
sample_a_symbol_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Sample A - Open Aegis Refined">
  <title>Sample A: Open Aegis Refined</title>
  <defs>
    <!-- Knockout band parallel to the rising verified checkmark (slope approx -45 deg) -->
    <clipPath id="cut-a">
      <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
               M340 330 L530 140 L480 90 L290 280 Z"/>
    </clipPath>
  </defs>
  <!-- Refined Aegis with Sweeping Welcoming Crown Arc (Approachable, Generous, Honest Wireframe) -->
  <path clip-path="url(#cut-a)"
        d="M216 78 C170 78 116 104 96 156 V254 C96 360 168 430 256 466 C344 430 416 360 416 254 V156 C396 104 342 78 296 78"
        fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Verified Ray (Dynamic, High Quality, Fulfilling Promises) -->
  <polyline points="160,274 234,348 466,116"
            fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# Horizontal Sample A
sample_a_horizontal_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480" role="img" aria-label="Sample A Horizontal">
  <title>Sample A: Farhan Davin Horizontal</title>
  <g transform="translate(30, -16)">
    <defs>
      <clipPath id="cut-a-h">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M340 330 L530 140 L480 90 L290 280 Z"/>
      </clipPath>
    </defs>
    <path clip-path="url(#cut-a-h)"
          d="M216 78 C170 78 116 104 96 156 V254 C96 360 168 430 256 466 C344 430 416 360 416 254 V156 C396 104 342 78 296 78"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="160,274 234,348 466,116"
              fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="540" y="246" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="88" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="544" y="316" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="30" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="544" y="342" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.3"/>
</svg>
"""

# Stacked Sample A
sample_a_stacked_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 720" width="640" height="720" role="img" aria-label="Sample A Stacked">
  <title>Sample A: Farhan Davin Stacked</title>
  <g transform="translate(64, 20)">
    <defs>
      <clipPath id="cut-a-st">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M340 330 L530 140 L480 90 L290 280 Z"/>
      </clipPath>
    </defs>
    <path clip-path="url(#cut-a-st)"
          d="M216 78 C170 78 116 104 96 156 V254 C96 360 168 430 256 466 C344 430 416 360 416 254 V156 C396 104 342 78 296 78"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="160,274 234,348 466,116"
              fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="320" y="595" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="82" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="320" y="652" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="28" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="250" y="675" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.25"/>
</svg>
"""


# -------------------------------------------------------------
# SAMPLE B: "THE EMBRACING HAVEN" (OPEN WINGS & VERIFIED BEACON)
# -------------------------------------------------------------
# Fitur:
# - Siluet Perisai Berbentuk Dua Sayap Merangkul / Dua Tangan Menengadah (Embracing Sanctuary)
# - Memancarkan kehangatan, kemurahan hati (generosity), dan kemudahan akses (approachable & simplifying)
# - Di bagian tengah terdapat Verified Checkmark yang memotong keluar dengan aksen presisi tinggi
# - Berongga murni (zero dark fill), sangat fleksibel dan scalable
sample_b_symbol_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Sample B - The Embracing Haven">
  <title>Sample B: The Embracing Haven</title>
  <defs>
    <!-- Knockout for the checkmark cutting across the right wing -->
    <clipPath id="cut-b">
      <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
               M330 330 L520 140 L470 90 L280 280 Z"/>
    </clipPath>
  </defs>
  <!-- Embracing Wings / Generous Sanctuary Shield (Murah Hati, Amanah, Transparan) -->
  <!-- Left Wing -->
  <path d="M 124 96 C 88 160 88 280 160 380 C 196 426 234 456 256 468"
        fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round"/>
  <!-- Right Wing with Knockout -->
  <path clip-path="url(#cut-b)"
        d="M 388 96 C 424 160 424 280 352 380 C 316 426 278 456 256 468"
        fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round"/>
  <!-- Verified Ray (Menepati Janji, Berkualitas, Mempermudah) -->
  <polyline points="152,274 232,354 466,120"
            fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# Horizontal Sample B
sample_b_horizontal_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" width="1440" height="480" role="img" aria-label="Sample B Horizontal">
  <title>Sample B: Farhan Davin Horizontal</title>
  <g transform="translate(30, -16)">
    <defs>
      <clipPath id="cut-b-h">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M330 330 L520 140 L470 90 L280 280 Z"/>
      </clipPath>
    </defs>
    <path d="M 124 96 C 88 160 88 280 160 380 C 196 426 234 456 256 468"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round"/>
    <path clip-path="url(#cut-b-h)"
          d="M 388 96 C 424 160 424 280 352 380 C 316 426 278 456 256 468"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round"/>
    <polyline points="152,274 232,354 466,120"
              fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="540" y="246" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="88" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="544" y="316" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="30" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="544" y="342" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.3"/>
</svg>
"""

# Stacked Sample B
sample_b_stacked_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 720" width="640" height="720" role="img" aria-label="Sample B Stacked">
  <title>Sample B: Farhan Davin Stacked</title>
  <g transform="translate(64, 20)">
    <defs>
      <clipPath id="cut-b-st">
        <path clip-rule="evenodd" d="M-100 -100 H612 V612 H-100 Z
                 M330 330 L520 140 L470 90 L280 280 Z"/>
      </clipPath>
    </defs>
    <path d="M 124 96 C 88 160 88 280 160 380 C 196 426 234 456 256 468"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round"/>
    <path clip-path="url(#cut-b-st)"
          d="M 388 96 C 424 160 424 280 352 380 C 316 426 278 456 256 468"
          fill="none" stroke="#0B1F3A" stroke-width="32" stroke-linecap="round"/>
    <polyline points="152,274 232,354 466,120"
              fill="none" stroke="#059669" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="320" y="595" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="800" font-size="82" fill="#0B1F3A" letter-spacing="2">FARHAN DAVIN</text>
  <text x="320" y="652" text-anchor="middle"
        font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Montserrat', Arial, sans-serif"
        font-weight="700" font-size="28" fill="#059669" letter-spacing="6">SMART CONTRACT AUDITOR</text>
  <rect x="250" y="675" width="140" height="4" rx="2" fill="#0B1F3A" opacity="0.25"/>
</svg>
"""

files_to_save = {
    "sample-a-symbol.svg": sample_a_symbol_svg,
    "sample-a-horizontal.svg": sample_a_horizontal_svg,
    "sample-a-stacked.svg": sample_a_stacked_svg,
    "sample-b-symbol.svg": sample_b_symbol_svg,
    "sample-b-horizontal.svg": sample_b_horizontal_svg,
    "sample-b-stacked.svg": sample_b_stacked_svg,
}

for name, content in files_to_save.items():
    p = os.path.join(OUTPUT_DIR, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

# Render PNG and PDF
renders = [
    ("sample-a-symbol.svg", "sample-a-symbol.png", "sample-a-symbol.pdf", 1024),
    ("sample-a-horizontal.svg", "sample-a-horizontal.png", "sample-a-horizontal.pdf", 1600),
    ("sample-a-stacked.svg", "sample-a-stacked.png", "sample-a-stacked.pdf", 1280),
    ("sample-b-symbol.svg", "sample-b-symbol.png", "sample-b-symbol.pdf", 1024),
    ("sample-b-horizontal.svg", "sample-b-horizontal.png", "sample-b-horizontal.pdf", 1600),
    ("sample-b-stacked.svg", "sample-b-stacked.png", "sample-b-stacked.pdf", 1280),
]

for svg_name, png_name, pdf_name, width in renders:
    sp = os.path.join(OUTPUT_DIR, svg_name)
    pp = os.path.join(OUTPUT_DIR, png_name)
    pdfp = os.path.join(OUTPUT_DIR, pdf_name)
    
    doc = fitz.open(sp)
    pdf_bytes = doc.convert_to_pdf()
    with open(pdfp, "wb") as f:
        f.write(pdf_bytes)
    
    page = doc[0]
    mat = fitz.Matrix(width / page.rect.width, width / page.rect.width)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(pp)
    print(f"Rendered {png_name} & {pdf_name}")

print("All sample assets generated successfully!")
