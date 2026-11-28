import sys, glob
from PIL import Image
d = sys.argv[1]; fs = sorted(glob.glob(f"{d}/*.jpg"), key=lambda f: float(f.split("_")[-1][:-4]))
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 5; w, h = 270, 480
rows = (len(fs) + cols - 1) // cols; g = Image.new("RGB", (cols * w, rows * h))
for i, f in enumerate(fs): g.paste(Image.open(f).resize((w, h)), ((i % cols) * w, (i // cols) * h))
g.save(f"{d}_grade.jpg", quality=85); print(f"{d}_grade.jpg")
