import sys; sys.stdout.reconfigure(encoding='utf-8')
import fitz

# Daksh
d = fitz.open(r'd:\DVA\Daksh DVA Assignment 2.pdf')
print("=== DAKSH PAGE 1 FONTS ===")
p1 = d[0]
blocks = p1.get_text('dict')['blocks']
for b in blocks:
    if 'lines' in b:
        for line in b['lines'][:8]:
            for span in line['spans']:
                fn = span['font']
                sz = span['size']
                tx = span['text'][:60]
                print(f"  {fn:30s}  {sz:5.1f}pt  '{tx}'")

print("\n=== AKSHAT PAGE 1 FONTS ===")
a = fitz.open(r'd:\DVA\Akshat-Education-Dashboard\DVA_Assignment_2_Akshat_Tripathi.pdf')
p1a = a[0]
blocks_a = p1a.get_text('dict')['blocks']
for b in blocks_a:
    if 'lines' in b:
        for line in b['lines'][:8]:
            for span in line['spans']:
                fn = span['font']
                sz = span['size']
                tx = span['text'][:60]
                print(f"  {fn:30s}  {sz:5.1f}pt  '{tx}'")
