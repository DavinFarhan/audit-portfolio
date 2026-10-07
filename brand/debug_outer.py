import fitz
import cv2

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#000000"/>
  <polygon points="500,210 730,380 730,585 500,810 270,585 270,380" fill="#0B192C" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round"/>
</svg>"""

doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
pix = doc[0].get_pixmap(dpi=150)
pix.save('reports/test_outer_only.png')

img = cv2.imread('reports/test_outer_only.png')
mid_x = img.shape[1] // 2
cv2.imwrite('reports/test_outer_peak.png', img[350:550, mid_x-150:mid_x+150])
print("Saved test_outer_peak.png")
