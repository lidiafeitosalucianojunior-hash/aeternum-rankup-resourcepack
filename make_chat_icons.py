from pathlib import Path
from PIL import Image, ImageDraw
import json, zipfile, hashlib, sys

def install(root, target):
    root = Path(root)
    atlas = Image.new("RGBA", (48, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(atlas)
    # INFERNO: chama laranja/dourada
    d.polygon([(8,0),(11,5),(12,3),(14,8),(14,12),(11,15),(4,15),(2,12),(2,9),(5,5),(5,9)], fill="#F74722")
    d.polygon([(8,3),(9,8),(12,10),(11,13),(5,13),(5,9)], fill="#FFA02B")
    d.polygon([(8,7),(10,11),(9,14),(6,14),(6,11)], fill="#FFEC79")
    # PURGATORIO: portal e cristal violeta
    x = 16
    d.polygon([(x+8,0),(x+13,5),(x+14,11),(x+8,15),(x+2,11),(x+3,5)], fill="#5E2DA9")
    d.polygon([(x+8,1),(x+12,5),(x+13,10),(x+8,14),(x+3,10),(x+4,5)], fill="#B56BFC")
    d.polygon([(x+8,3),(x+11,7),(x+8,12),(x+5,7)], fill="#E6C4FF")
    d.polygon([(x+8,3),(x+11,7),(x+8,7)], fill="#FFFFFF")
    # CEU: estrela dourada e asas de luz
    x = 32
    d.polygon([(x+8,0),(x+10,6),(x+15,8),(x+10,10),(x+8,15),(x+6,10),(x+1,8),(x+6,6)], fill="#F4BC40")
    d.polygon([(x+8,2),(x+9,7),(x+13,8),(x+9,9),(x+8,13),(x+7,9),(x+3,8),(x+7,7)], fill="#FFF0AF")
    d.polygon([(x+8,5),(x+10,8),(x+8,11),(x+6,8)], fill="#FFFFFF")
    texture = root / "assets" / "aeternum" / "textures" / "font" / "chat_reinos.png"
    config = root / "assets" / "aeternum" / "font" / "realm_icons.json"
    texture.parent.mkdir(parents=True, exist_ok=True)
    config.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(texture, optimize=True)
    config.write_text(json.dumps({"providers":[{"type":"bitmap",
        "file":"aeternum:font/chat_reinos.png",
        "ascent":9,"height":11,"chars":["".join(chr(0xE310+i) for i in range(3))]}]},
        ensure_ascii=False,indent=2),
        encoding="utf-8")
    preview = atlas.resize((480,160),Image.Resampling.NEAREST)
    preview.save(root / "PREVIA_EMOJIS_REINOS.png")
    with zipfile.ZipFile(target,"a",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(texture, texture.relative_to(root).as_posix())
        z.write(config, config.relative_to(root).as_posix())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert z.read("assets/aeternum/font/realm_icons.json")
    print("ICON_PACK_OK", target, hashlib.sha1(Path(target).read_bytes()).hexdigest())

if __name__ == "__main__":
    root=Path(__file__).resolve().parent
    install(root,root / "AETERNUM_Reinos_GUI_Pack.zip")
