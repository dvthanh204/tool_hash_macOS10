import io, os, sys, zipfile, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from author_app import AuthorApp

# We can reuse the protect_pptx from AuthorApp
class DummyGUI(AuthorApp):
    def __init__(self):
        pass

app = DummyGUI()

# Create dummy pptx
with zipfile.ZipFile("test_sample.pptx", "w") as z:
    z.writestr("[Content_Types].xml", "<Types/>")
    z.writestr("_rels/.rels", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"></Relationships>")
    z.writestr("ppt/presentation.xml", "<p:presentation></p:presentation>")

p_pths = ["test_sample.pptx"]
mz = io.BytesIO()
manifest = {}
with zipfile.ZipFile(mz, 'w', zipfile.ZIP_DEFLATED) as zf:
    for idx, p_pth in enumerate(p_pths):
        orig_name = os.path.basename(p_pth)
        safe_name = f"lesson_{idx}.pptx"
        protected_data = app.protect_pptx(p_pth)
        zf.writestr(safe_name, protected_data)
        manifest[safe_name] = orig_name
    zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False).encode('utf-8'))
    zf.writestr("revocations.json", "{}")

aesgcm = AESGCM(b"12345678901234567890123456789012")
nonce = os.urandom(12)
enc = aesgcm.encrypt(nonce, mz.getvalue(), None)
with open("baigiang.khoa", "wb") as f:
    f.write(nonce + enc)

out_name = "KhoaHoc_Mac_FINAL.zip"
with zipfile.ZipFile(out_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    base_folder = "KhoaHoc_Mac/"
    for d_path in [base_folder, base_folder + "SlideLock.app/"]:
        z_info_dir = zipfile.ZipInfo(d_path)
        z_info_dir.create_system = 3
        z_info_dir.external_attr = (0x41ED) << 16
        zf.writestr(z_info_dir, "")
    
    z_info_file = zipfile.ZipInfo(f"{base_folder}baigiang.khoa")
    z_info_file.create_system = 3
    z_info_file.external_attr = (0x81A4) << 16
    with open("baigiang.khoa", "rb") as f_in: zf.writestr(z_info_file, f_in.read())
    
    for r, d, fs in os.walk("SlideLock.app"):
        for folder in d:
            dp = os.path.join(r, folder)
            arcname_dir = os.path.relpath(dp, ".").replace("\\", "/") + "/"
            if base_folder + arcname_dir == base_folder + "SlideLock.app/": continue
            z_info = zipfile.ZipInfo(base_folder + arcname_dir)
            z_info.create_system = 3
            z_info.external_attr = (0x41ED) << 16
            zf.writestr(z_info, "")
            
        for f in fs:
            fp = os.path.join(r, f)
            arcname = os.path.relpath(fp, ".").replace("\\", "/")
            z_info = zipfile.ZipInfo.from_file(fp, base_folder + arcname)
            z_info.create_system = 3
            if "Contents/MacOS/" in arcname and not arcname.endswith(".plist") and not arcname.endswith(".txt"):
                z_info.external_attr = (0x81ED) << 16
            else:
                z_info.external_attr = (0x81A4) << 16
            with open(fp, "rb") as f_in: zf.writestr(z_info, f_in.read())
            
print(f"Packed {out_name} successfully using the new SlideLock.app!")
os.remove("baigiang.khoa")
os.remove("test_sample.pptx")
