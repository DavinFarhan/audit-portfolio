import fitz
import cv2
import numpy as np

svg_test = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#FFFFFF"/>
  <!-- 1. Central Top Rhombus/Spire -->
  <polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <!-- 2. Upper Left Wing -->
  <polygon points="500,210 270,380 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <!-- 3. Upper Right Wing -->
  <polygon points="500,210 635.7,431.2 730,380" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
</svg>"""

doc = fitz.open(stream=svg_test.encode('utf-8'), filetype='svg')
pix = doc[0].get_pixmap(dpi=150)
pix.save('reports/test_top_3_polys.png')

img = cv2.imread('reports/test_top_3_polys.png')
print("Image shape:", img.shape)
# Test horizontal symmetry across the entire image
# Center is x = img.shape[1] // 2
mid = img.shape[1] // 2
left_half = img[:, :mid]
right_half = img[:, mid:]
right_flipped = cv2.flip(right_half, 1)

min_w = min(left_half.shape[1], right_flipped.shape[1])
diff = cv2.absdiff(left_half[:, :min_w], right_flipped[:, -min_w:])
print("Max diff:", diff.max(), "Mean diff:", diff.mean())

cv2.imwrite('reports/diff_map.png', diff * 10)
print("Saved diff_map.png")
