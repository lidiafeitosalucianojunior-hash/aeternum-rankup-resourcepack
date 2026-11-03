from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, zipfile, random

ROOT = Path(__file__).parent
W, H, SCALE = 176, 128, 4
IMG_W, IMG_H = W*SCALE, H*SCALE
im = Image.new("RGB", (IMG_W, IMG_H), (19,19,31))
d = ImageDraw.Draw(im)
random.seed(42)
def box(x0,y0,x1,y1,fill,outline=None,width=1):
    d.rectangle((x0*SCALE,y0*SCALE,x1*SCALE,y1*SCALE),fill=fill,outline=outline,width=width*SCALE if outline else 1)
def poly(points, color):
    d.polygon([(x*SCALE,y*SCALE) for x,y in points],fill=color)
def line(points, fill, width=1):
    d.line([(x*SCALE,y*SCALE) for x,y in points],fill=fill,width=width*SCALE)
def circle(box_, fill, outline=None, width=1):
    x0,y0,x1,y1=box_
    d.ellipse((x0*SCALE,y0*SCALE,x1*SCALE,y1*SCALE),fill=fill,outline=outline,width=width*SCALE)
def font(size, bold=True):
    candidates = ["C:/Windows/Fonts/ariblk.ttf", "C:/Windows/Fonts/arialbd.ttf",
                  "C:/Windows/Fonts/arial.ttf"] if bold else ["C:/Windows/Fonts/arial.ttf"]
    for f in candidates:
        if Path(f).exists(): return ImageFont.truetype(f,int(size*SCALE))
    return ImageFont.load_default()
def txt_center(text,x,y,size,fill,stroke=None,bold=True,maxwidth=None):
    f=font(size,bold)
    bounds=d.textbbox((0,0),text,font=f,stroke_width=0)
    if maxwidth is not None:
        while (bounds[2]-bounds[0]) > maxwidth*SCALE and size>5:
            size-=0.5
            f=font(size,bold)
            bounds=d.textbbox((0,0),text,font=f)
    drawx=x*SCALE-(bounds[2]-bounds[0])/2-bounds[0]
    drawy=y*SCALE-bounds[1]
    d.text((int(drawx),int(drawy)),text,font=f,fill=fill,
           stroke_width=(SCALE//2 if stroke else 0),stroke_fill=stroke)
# Base: pixel stone wall with bevel
box(0,0,175,127,"#161620")
for yy in range(0,128,7):
    for xx in range((yy//7 % 2)*7,176,14):
        base=random.choice(["#222433","#292939","#252738"])
        box(xx,yy,min(175,xx+13),min(127,yy+6),base)
        line([(xx,yy),(min(175,xx+12),yy)],"#39364b",1)
box(0,0,175,127,None,"#655978",2)
box(2,2,173,125,None,"#12111d",2)
# Header
box(3,3,172,26,"#171521")
box(5,4,170,24,"#24202a","#805d35",1)
box(8,6,167,22,"#17151f")
# golden crown in header
poly([(80,5),(83,8),(88,3),(93,8),(96,5),(94,12),(82,12)],"#efab32")
poly([(84,8),(88,5),(92,8),(91,10),(85,10)],"#fff4a5")
box(83,12,93,13,"#ecbb54")
# Title
txt_center("ESCOLHA SEU REINO",88,15.5,10.4,"#ffdf6d","#513117",True,163)
line([(7,26),(168,26)],"#ffd069",1)
# 3 panels, aligned with 3-slot regions 7..61, 61..115, 115..169
panels = [
    {"x":5,"name":"INFERNO","outer":"#d82d23","glow":"#ff8545","bg1":(90,14,24),"bg2":(239,62,15),"button":"#a72719","accent":"#ffac35"},
    {"x":61,"name":"PURGATÓRIO","outer":"#a04cfd","glow":"#e4aaff","bg1":(23,16,52),"bg2":(96,42,148),"button":"#56329c","accent":"#cf90ff"},
    {"x":117,"name":"CÉU","outer":"#f2bd50","glow":"#e9f5ff","bg1":(16,78,140),"bg2":(71,179,245),"button":"#1569bd","accent":"#ffe69c"},
]
for p in panels:
    x=p["x"]; right=x+53
    box(x,29,right,122,"#11131f",p["outer"],2)
    box(x+2,31,right-2,120,"#1b1b28",p["glow"],1)
    # name label
    box(x+4,32,right-4,43,"#171827")
    line([(x+4,43),(right-4,43)],p["outer"],1)
    txt_center(p["name"],x+26.5,34.1,8.6,"#fff8df","#181121",True,47)
    # gradient illustration area
    for yy in range(45,99):
        a=(yy-45)/54
        rgb=tuple(round(c1*(1-a)+c2*a) for c1,c2 in zip(p["bg1"],p["bg2"]))
        line([(x+4,yy),(right-4,yy)],rgb,1)
    box(x+3,44,right-3,101,None,"#3b3447",1)
    # button
    box(x+4,106,right-4,117,p["button"],p["glow"],1)
    line([(x+6,108),(right-6,108)],p["glow"],1)
    txt_center("ESCOLHER",x+26.5,109,8,"#ffffff","#101021",True,48)
    line([(x+5,119),(right-5,119)],p["outer"],1)
# INFERNO art
x=5
# moon and distant peaks
circle((21,48,42,69),"#fa542b")
circle((25,52,38,65),"#ec3e28")
poly([(9,86),(12,72),(17,78),(20,68),(25,78),(29,67),(34,77),(42,69),(49,84),(55,74),(58,101),(9,101)],"#411824")
# castle stepped dark silhouette
box(15,71,51,100,"#28212c")
box(17,64,25,100,"#25232d")
box(39,64,48,100,"#25232d")
poly([(16,65),(21,59),(26,65)],"#191c27")
poly([(38,65),(43,59),(49,65)],"#191c27")
box(23,61,41,100,"#211f29")
poly([(24,61),(32,54),(40,61)],"#171d28")
# horns, glowing eyes
poly([(23,61),(19,53),(27,57),(32,65)],"#201b24")
poly([(41,61),(45,53),(37,57),(32,65)],"#201b24")
box(26,69,29,71,"#ffb74b")
box(35,69,38,71,"#ffb74b")
# huge fiery portal
box(26,82,39,98,"#78211b")
poly([(26,83),(32,77),(39,83),(39,98),(26,98)],"#ff7e1f")
poly([(29,84),(32,80),(36,85),(36,98),(29,98)],"#ffe26d")
poly([(30,91),(34,84),(34,98),(30,98)],"#ffffff")
# lava tiles
for y in range(99,102):
    line([(9,y),(55,y)],"#ffad28" if y%2 else "#f65a17")
# embers
for xx,yy in [(12,53),(18,48),(50,58),(53,67),(12,78)]:
    box(xx,yy,xx+1,yy+1,"#ffc45f")

# PURGATORIO art
x=61
circle((95,48,107,60),"#e1dcf5")
circle((99,46,110,58),"#362658")
# distant towers
poly([(65,93),(70,73),(73,82),(78,64),(81,83),(88,53),(94,82),(101,66),(106,84),(112,70),(114,101)],"#28243e")
# gothic church
box(76,71,100,101,"#2a253e")
box(70,73,80,101,"#28243b")
box(96,73,106,101,"#28243b")
poly([(69,74),(75,61),(81,74)],"#262137")
poly([(95,74),(101,61),(107,74)],"#262137")
poly([(81,72),(88,51),(95,72)],"#1f1e36")
box(84,65,92,100,"#393054")
# central stained-glass
circle((84,68,92,76),"#c78aff")
poly([(88,68),(90,72),(88,76),(86,72)],"#ffc8ff")
# purple portal
poly([(79,99),(79,84),(88,76),(97,84),(97,99)],"#b753ff")
poly([(82,98),(82,86),(88,80),(94,86),(94,98)],"#36216b")
circle((84,85,92,94),"#8840ea")
circle((86,87,90,91),"#dab5ff")
for yy in (94,98,100):
    line([(71+(yy-94)*2,yy),(105-(yy-94)*2,yy)],"#b47bd5")
# purple flames
for px in (71,105):
    poly([(px-2,87),(px,82),(px+1,86),(px,84),(px+2,90),(px,93),(px-2,93)],"#b56aff")

# CEU art
x=117
for cx,cy in [(129,52),(160,57),(138,61)]:
    circle((cx-5,cy-2,cx+6,cy+3),"#dff7ff")
    circle((cx-2,cy-4,cx+3,cy+3),"#ffffff")
# halo
circle((138,48,153,53),None,"#ffdd76",1)
# wings
poly([(135,76),(120,68),(124,76),(120,80),(135,84)],"#f3f7fb")
poly([(149,76),(164,68),(160,76),(164,80),(149,84)],"#f3f7fb")
for tx in (123,157):
    line([(tx,75),(143,81)],"#c9d9e7")
# temple white stone
box(129,75,158,99,"#edf8fc")
box(136,64,152,99,"#f7fbfd")
poly([(135,66),(144,57),(153,66)],"#ffcb64")
box(140,62,148,99,"#fff8e9")
# columns
for xx in (129,135,152,158):
    box(xx,78,xx+3,99,"#eef2fb")
    line([(xx,78),(xx+3,78)],"#e4c063")
# central gate
poly([(138,99),(138,86),(144,79),(150,86),(150,99)],"#d5942a")
poly([(140,98),(140,86),(144,82),(148,86),(148,98)],"#fff2b7")
poly([(143,97),(143,85),(146,88),(146,97)],"#ffffff")
# columns and steps
for yy in (99,100,101):
    line([(125,yy),(162,yy)],"#eedfa5")
# corner stone ornaments
for x in [5,61,117]:
    box(x+3,30,x+7,31,"#ffffff")
    box(x+46,120,x+50,121,"#ffffff")
# Bottom instruction strip
box(4,124,171,127,"#171620")
txt_center("TRÊS REINOS • UMA ETERNIDADE",88,123.5,6.5,"#ead6a8",None,True,165)

# Resample to native dimensions using high-quality small text antialias.
small = im.resize((W,H),Image.Resampling.LANCZOS)
outdir=ROOT / "assets" / "aeternum" / "textures" / "font"
outdir.mkdir(parents=True,exist_ok=True)
small.save(outdir/"reinos.png",optimize=True)
# 4x nearest is a real-size pixel-perfect presentation of how the GUI appears in-game.
small.resize((W*5,H*5),Image.Resampling.NEAREST).save(ROOT/"PREVIA_GUI.png",optimize=True)

fontdir=ROOT/"assets"/"aeternum"/"font"
fontdir.mkdir(parents=True,exist_ok=True)
(fontdir/"gui.json").write_text(json.dumps({"providers":[
    {"type":"space","advances":{chr(0xe100):-8}},
    {"type":"bitmap","file":"aeternum:font/reinos.png","ascent":13,"height":128,"chars":[chr(0xe101)]}
]},ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"pack.mcmeta").write_text(json.dumps({"pack":{"pack_format":34,
    "description":"AETERNUM RankUP - Menu de Reinos (Nitido v2)"}},ensure_ascii=False,indent=2),encoding="utf-8")
pack=ROOT/"AETERNUM_Reinos_GUI_Pack.zip"
with zipfile.ZipFile(pack,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in [ROOT/"pack.mcmeta",fontdir/"gui.json",outdir/"reinos.png"]:
        z.write(p,p.relative_to(ROOT).as_posix())
print("SUCCESS",pack,pack.stat().st_size,(outdir/"reinos.png").stat().st_size)
