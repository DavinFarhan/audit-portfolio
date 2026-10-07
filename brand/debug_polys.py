import fitz
import cv2
import numpy as np

def render_svg(content):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
      <rect width="1000" height="1000" fill="#FFFFFF"/>
      {content}
    </svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# Test 1: Just P1
p1 = '<polygon points="500,210 364.3,431.2 500,505 635.7,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>'
# Test 2: P1 + P2
p2 = '<polygon points="500,210 270,380 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>'
# Test 3: P1 + P3
p3 = '<polygon points="500,210 635.7,431.2 730,380" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>'

img_p1_p2 = render_svg(p1 + p2)
img_p1_p3 = render_svg(p1 + p3)

# In img_p1_p2, let's measure the stroke on the left edge (500,210 -> 364.3, 431.2)
# In img_p1_p3, let's measure the stroke on the right edge (500,210 -> 635.7, 431.2)

# Flip img_p1_p3 horizontally and compare with img_p1_p2:
flipped_p3 = cv2.flip(img_p1_p3, 1)
diff = cv2.absdiff(img_p1_p2, flipped_p3)
print("P1+P2 vs flipped(P1+P3) max diff:", diff.max())

# Now let's test with all 5 facets:
p4 = '<polygon points="270,380 270,585 500,505 364.3,431.2" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>'
p5 = '<polygon points="730,380 635.7,431.2 500,505 730,585" fill="#0B192C" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>'

img_all = render_svg(p1 + p2 + p3 + p4 + p5)
flipped_all = cv2.flip(img_all, 1)
diff_all = cv2.absdiff(img_all, flipped_all)
print("All 5 facets symmetry diff max:", diff_all.max(), "mean:", diff_all.mean())

cv2.imwrite('reports/diff_all_facets.png', diff_all * 10)
