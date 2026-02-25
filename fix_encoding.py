import os

try:
    import chardet
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'chardet'])
    import chardet

root = r'C:\Users\boula\Desktop\main\IDE\BlackTorch'
exts = {'.py', '.ts', '.tsx', '.js', '.mjs', '.json', '.txt',
        '.yml', '.yaml', '.md', '.css', '.toml', '.env', '.mts', '.cjs'}
skip = {'node_modules', '.next', '.venv', '__pycache__', '.git', 'dist', 'build', 'fix_encoding.py'}

converted = []
errors = []

for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in skip]
    for fname in files:
        if fname in skip:
            continue
        if os.path.splitext(fname)[1].lower() not in exts:
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            with open(fpath, 'rb') as f:
                raw = f.read()

            had_bom = False
            # Strip UTF-8 BOM
            if raw.startswith(b'\xef\xbb\xbf'):
                raw = raw[3:]
                had_bom = True
            # Strip UTF-16 BOM
            elif raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
                det = chardet.detect(raw)
                enc = det.get('encoding') or 'utf-16'
                text = raw.decode(enc, errors='replace')
                with open(fpath, 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
                converted.append(f'UTF-16 BOM -> utf-8: {fpath}')
                continue

            try:
                text = raw.decode('utf-8')
                if had_bom:
                    with open(fpath, 'w', encoding='utf-8', newline='') as f:
                        f.write(text)
                    converted.append(f'BOM removed: {fpath}')
                # else: already clean UTF-8, skip
            except UnicodeDecodeError:
                det = chardet.detect(raw)
                enc = det.get('encoding') or 'latin-1'
                text = raw.decode(enc, errors='replace')
                with open(fpath, 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
                converted.append(f'{enc} -> utf-8: {fpath}')

        except Exception as e:
            errors.append(f'ERROR {fpath}: {e}')

print('=== CONVERTED ===')
for c in converted:
    print(c)
print(f'\nTotal converted: {len(converted)}')

if errors:
    print('\n=== ERRORS ===')
    for e in errors:
        print(e)

print('\nDONE')
