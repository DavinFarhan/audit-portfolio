import fitz

# Test 1: Polygon
svg1 = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <polygon points="100,20 180,80 180,140 100,180 20,140 20,80" fill="blue" stroke="red" stroke-width="10"/>
</svg>"""
doc1 = fitz.open(stream=svg1.encode('utf-8'), filetype='svg')
doc1[0].get_pixmap().save('reports/test_poly_red.png')

# Test 2: Path with explicit Z (Closepath)
svg2 = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <path d="M 100,20 L 180,80 L 180,140 L 100,180 L 20,140 L 20,80 Z" fill="blue" stroke="red" stroke-width="10"/>
</svg>"""
doc2 = fitz.open(stream=svg2.encode('utf-8'), filetype='svg')
doc2[0].get_pixmap().save('reports/test_path_red.png')

print("Saved both test images!")
