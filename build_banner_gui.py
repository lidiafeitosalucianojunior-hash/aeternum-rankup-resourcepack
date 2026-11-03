from pathlib import Path
from PIL import Image, ImageOps
import json, zipfile, hashlib

ROOT = Path(__file__).resolve().parent
SOURCE = Path.home() / "Downloads" / "Aeternum_ Escolha Seu Reino.png"
if not SOURCE.is_file():
    raise FileNotFoundError(SOURCE)
image = Image.open(SOURCE).convert("RGBA")
print("Original:", image.size)
# O quadro do Minecraft continua em 176 x 220 unidades de GUI,
# mas os pixels originais sao preservados em 20 celulas de 256x256.
# Isto evita miniaturizar o cartaz inteiro para 176x220 pixels.
image = ImageOps.fit(image, (1024, 1280), method=Image.Resampling.LANCZOS,
    centering=(0.5, 0.5))
texture_dir = ROOT / "assets" / "aeternum" / "textures" / "font"
font_dir = ROOT / "assets" / "aeternum" / "font"
texture_dir.mkdir(parents=True, exist_ok=True)
font_dir.mkdir(parents=True, exist_ok=True)
entries = [("pack.mcmeta", None)]
providers = [{
    "type": "space",
    "advances": {
        chr(0xE100): -8,
        chr(0xE101): -1,
        chr(0xE102): -176
    }
}]
for row in range(5):
    fname = f"reinos_hd_linha_{row}.png"
    row_im = image.crop((0, row*256, 1024, (row+1)*256))
    row_im.save(texture_dir / fname, optimize=True)
    glyphs = "".join(chr(0xE200 + row*4 + col) for col in range(4))
    providers.append({
        "type": "bitmap",
        "file": "aeternum:font/" + fname,
        "ascent": 13 - row * 44,
        "height": 44,
        "chars": [glyphs]
    })
font_path = font_dir / "gui.json"
font_path.write_text(
    json.dumps({"providers":providers}, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
(ROOT / "pack.mcmeta").write_text(
    json.dumps({
        "pack": {
            "pack_format": 34,
            "description": "AETERNUM - Escolha seu Reino HD (20 partes)"
        }
    }, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
# A prévia em 1024px permite inspecionar exatamente a arte reunida.
image.convert("RGB").save(ROOT / "PREVIA_REINOS_HD.png", optimize=True)
# Simula o limite de tamanho exibido numa GUI Minecraft.
preview_small = image.resize((176,220), Image.Resampling.LANCZOS)
preview_small.resize((704,880), Image.Resampling.NEAREST).save(
    ROOT / "PREVIA_TAMANHO_MINECRAFT.png", optimize=True
)
target = ROOT / "AETERNUM_Reinos_GUI_Pack.zip"
with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    allfiles = [
      ROOT / "pack.mcmeta", font_path
    ] + sorted(texture_dir.glob("reinos_hd_linha_*.png"))
    for fp in allfiles:
        z.write(fp, fp.relative_to(ROOT).as_posix())
from make_chat_icons import install
install(ROOT, target)
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    for row in range(5):
        assert Image.open(z.open(
          f"assets/aeternum/textures/font/reinos_hd_linha_{row}.png"
        )).size == (1024,256)
print("PACK_OK",target, target.stat().st_size)
print("SHA1",hashlib.sha1(target.read_bytes()).hexdigest())
