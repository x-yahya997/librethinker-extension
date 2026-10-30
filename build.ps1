# Build LibreThinker.oxt using Python's zipfile module
# (PowerShell's Compress-Archive creates Windows directory entry formats that LibreOffice rejects)

$pythonScript = @"
import os
import zipfile

src_dir = 'extension'
out_file = 'dist/LibreThinker.oxt'

os.makedirs(os.path.dirname(out_file), exist_ok=True)
if os.path.exists(out_file):
    try:
        os.remove(out_file)
    except PermissionError:
        print('Error: dist/LibreThinker.oxt is locked. Please close LibreOffice and try again.')
        exit(1)

with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(src_dir):
        # Exclude pycache and hidden folders
        dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith('.')]
        for file in files:
            if file.endswith(('.pyc', '.pyo', '.DS_Store')) or file.startswith('.'):
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, src_dir).replace('\\\\', '/')
            z.write(file_path, arcname)

print('Successfully created dist/LibreThinker.oxt')
"@

python -c $pythonScript
