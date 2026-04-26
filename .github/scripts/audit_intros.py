import glob, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'C:/Users/scott/Code/Aesop/ai-academy/modules'
all_m = glob.glob(ROOT + '/**/*-m*.html', recursive=True)
all_m = [f for f in all_m if 'archive' not in f and 'i18n' not in f]

m1     = [f for f in all_m if '-m1.html' in f]
m2plus = [f for f in all_m if any('-m%d.html' % n in f for n in range(2,10))]

def has_intro(f):
    return 'id="p-intro"' in open(f, encoding='utf-8', errors='replace').read()

m1_with    = [f for f in m1 if has_intro(f)]
m1_without = [f for f in m1 if not has_intro(f)]
m2_with    = [f for f in m2plus if has_intro(f)]
m2_without = [f for f in m2plus if not has_intro(f)]

print(f'm1  files: {len(m1)}     | with intro: {len(m1_with)} | WITHOUT: {len(m1_without)}')
print(f'm2+ files: {len(m2plus)} | with intro: {len(m2_with)} | WITHOUT: {len(m2_without)}')

if m1_without:
    print('\nm1 files MISSING intro:')
    for f in sorted(m1_without):
        print(' ', f.replace(ROOT, '').lstrip('/').lstrip('\\'))

if m2_without:
    print('\nSample m2+ files missing intro (first 10):')
    for f in sorted(m2_without)[:10]:
        print(' ', f.replace(ROOT, '').lstrip('/').lstrip('\\'))
