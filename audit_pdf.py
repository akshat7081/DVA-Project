import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r'd:\DVA\Akshat-Education-Dashboard\DVA_Assignment_2_Akshat_Tripathi.pdf')
print(f"Total pages: {len(doc)}\n{'='*70}")

for i, page in enumerate(doc):
    text = page.get_text().strip()
    imgs = page.get_images()
    print(f"\n{'='*70}")
    print(f"PAGE {i+1}  |  Images: {len(imgs)}")
    print(f"{'='*70}")
    print(text[:1500])
    if len(text) > 1500:
        print(f"  ... [{len(text)-1500} more chars]")
