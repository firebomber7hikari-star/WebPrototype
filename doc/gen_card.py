"""Generate a black-and-white class card as SVG.

Usage: python3 gen_card.py <warrior|rogue|mage> out.svg
"""
import math, sys
def star(cx, cy, R, r=None):
    r = r or R*0.42
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5
        rr=R if i%2==0 else r
        pts.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}"/>'

X0,Y0,W,H=169,32,686,960
X1,Y1=X0+W,Y0+H
B,Wh="#000","#fff"
s=[]
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">')
s.append(f'<rect width="1024" height="1024" fill="{Wh}"/>')
# card body
s.append(f'<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="38" fill="{Wh}" stroke="{B}" stroke-width="10"/>')
s.append(f'<rect x="{X0+18}" y="{Y0+18}" width="{W-36}" height="{H-36}" rx="24" fill="none" stroke="{B}" stroke-width="3"/>')

# ---- top band: attack ----
ay=112
s.append(f'<circle cx="{X0+78}" cy="{ay}" r="44" fill="{B}"/>')
# sword icon (white), diagonal
s.append(f'<g transform="translate({X0+78},{ay}) rotate(45)" fill="{Wh}">'
         '<polygon points="-5,-34 5,-34 5,8 -5,8"/><polygon points="-5,-34 0,-42 5,-34"/>'
         '<rect x="-17" y="8" width="34" height="6" rx="2"/><rect x="-3.5" y="14" width="7" height="14"/><circle cx="0" cy="31" r="5"/></g>')
s.append(f'<text x="{X0+78}" y="{ay+66}" font-family="Georgia,serif" font-size="17" font-weight="bold" text-anchor="middle" letter-spacing="3">ATK</text>')
s.append(f'<g fill="{B}">')
for i in range(6):
    s.append(star(X0+175+i*80, ay, 31))
s.append('</g>')

# divider helper
def divider(y):
    out=[f'<line x1="{X0+40}" y1="{y}" x2="{512-26}" y2="{y}" stroke="{B}" stroke-width="3"/>',
         f'<line x1="{512+26}" y1="{y}" x2="{X1-40}" y2="{y}" stroke="{B}" stroke-width="3"/>',
         f'<line x1="{X0+40}" y1="{y+7}" x2="{512-26}" y2="{y+7}" stroke="{B}" stroke-width="1"/>',
         f'<line x1="{512+26}" y1="{y+7}" x2="{X1-40}" y2="{y+7}" stroke="{B}" stroke-width="1"/>',
         f'<rect x="{512-11}" y="{y-8}" width="22" height="22" transform="rotate(45 512 {y+3})" fill="{B}"/>',
         f'<circle cx="{X0+40}" cy="{y+3}" r="4" fill="{B}"/><circle cx="{X1-40}" cy="{y+3}" r="4" fill="{B}"/>']
    return "".join(out)
s.append(divider(196))

# ---- art: class bust, side profile facing right ----
cx,cy,R=512,513,272
s.append(f'<defs><clipPath id="art"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="{R+14}" fill="none" stroke="{B}" stroke-width="2"/>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="{R+6}" fill="none" stroke="{B}" stroke-width="1" stroke-dasharray="4 8"/>')
FIGS={}
FIGS["warrior"]=[
 # sword grip over the back
 '<g transform="translate(-120,-30) rotate(-18)"><rect x="-9" y="-150" width="18" height="120" rx="4"/>'
   '<rect x="-44" y="-36" width="88" height="16" rx="5"/><circle cx="0" cy="-160" r="16"/>'
   '<path d="M-9,-130 L9,-120 M-9,-105 L9,-95 M-9,-80 L9,-70 M-9,-55 L9,-45" stroke="#fff" stroke-width="3"/></g>',
 # cape / back
 '<path d="M-60,20 C-140,40 -200,120 -230,300 L40,300 Z"/>',
 # torso
 '<path d="M-60,10 L55,10 C90,40 150,90 170,170 L190,300 L-200,300 C-190,160 -130,60 -60,10 Z"/>',
 # chest plate lines
 '<path d="M60,40 C110,90 135,170 140,300" stroke="#fff" stroke-width="5" fill="none"/>',
 '<path d="M30,120 C70,140 100,180 110,300" stroke="#fff" stroke-width="2" fill="none"/>',
 # neck
 '<path d="M-48,-40 L46,-30 L58,20 L-58,20 Z"/>',
 # gorget
 '<path d="M-70,0 C-20,-20 40,-14 75,10 L80,40 C40,20 -20,18 -78,36 Z" stroke="#fff" stroke-width="4"/>',
 # pauldron (layered)
 '<path d="M-150,80 C-130,-10 30,-20 60,70 C20,100 -90,110 -150,80 Z" stroke="#fff" stroke-width="5"/>',
 '<path d="M-160,120 C-120,90 20,100 60,110" stroke="#fff" stroke-width="4" fill="none"/>',
 '<path d="M-168,160 C-120,130 20,140 66,150" stroke="#fff" stroke-width="4" fill="none"/>',
 '<circle cx="-50" cy="40" r="7" fill="#fff"/><circle cx="0" cy="45" r="7" fill="#fff"/>',
 # back of head / neck guard
 '<path d="M-106,-76 L-40,-84 L-30,-20 L-56,20 L-110,30 Z"/>',
 # face profile
 '<path d="M-30,-150 L70,-150 L78,-118 L84,-100 L112,-74 L106,-66 L90,-62 L94,-50 L88,-44 L92,-36 '
   'L86,-22 C80,-8 70,-4 52,-4 L40,-2 L-48,-2 Z"/>',
 '<path d="M62,-98 L82,-96" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
 # helmet dome with brim + cheek guard
 '<path d="M-100,-110 C-110,-250 80,-270 92,-128 L96,-114 L60,-114 L56,-80 C50,-50 40,-36 22,-30 '
   'L-10,-30 C-6,-60 -20,-80 -60,-80 L-104,-70 Z" stroke="#fff" stroke-width="5"/>',
 '<path d="M-98,-128 C-60,-140 40,-140 92,-130" stroke="#fff" stroke-width="5" fill="none"/>',
 '<path d="M-6,-226 L-6,-136" stroke="#fff" stroke-width="3"/>',
 '<circle cx="-70" cy="-120" r="4" fill="#fff"/><circle cx="-30" cy="-124" r="4" fill="#fff"/><circle cx="20" cy="-124" r="4" fill="#fff"/><circle cx="60" cy="-122" r="4" fill="#fff"/>',
 '<circle cx="20" cy="-62" r="7" fill="#fff"/>',
 # plume
 '<path d="M-10,-232 C-30,-290 -150,-280 -190,-170 C-170,-130 -150,-120 -140,-110 C-140,-180 -90,-220 -20,-210 Z"/>',
 '<path d="M-30,-242 C-100,-250 -150,-210 -168,-150 M-40,-228 C-100,-230 -135,-195 -150,-140" stroke="#fff" stroke-width="3" fill="none"/>',
]
FIGS["rogue"]=[
 # dagger hilts crossed behind the back
 '<g transform="translate(-105,-20) rotate(-28)"><rect x="-8" y="-120" width="16" height="96" rx="4"/>'
   '<path d="M-34,-20 C-20,-34 20,-34 34,-20 L34,-12 L-34,-12 Z"/><circle cx="0" cy="-128" r="13"/></g>',
 '<g transform="translate(-140,10) rotate(-58)"><rect x="-8" y="-120" width="16" height="96" rx="4"/>'
   '<path d="M-34,-20 C-20,-34 20,-34 34,-20 L34,-12 L-34,-12 Z"/><circle cx="0" cy="-128" r="13"/></g>',
 # hood tail
 '<path d="M-100,-160 C-175,-120 -200,-30 -185,60 L-100,40 Z"/>',
 # torso
 '<path d="M-80,10 L60,10 C95,40 140,100 160,170 L180,300 L-210,300 C-200,160 -150,60 -80,10 Z"/>',
 # cloak edge over the shoulder
 '<path d="M-40,-10 C-110,60 -150,170 -160,300" stroke="#fff" stroke-width="5" fill="none"/>',
 '<path d="M66,30 C100,90 118,160 124,300" stroke="#fff" stroke-width="4" fill="none"/>',
 # bandolier with throwing knives
 '<path d="M-120,80 L110,250" stroke="#fff" stroke-width="30"/>',
 '<path d="M-120,80 L110,250" stroke="#000" stroke-width="20"/>',
 '<g fill="#fff"><path d="M-70,100 l14,10 l-34,50 Z"/><path d="M-20,137 l14,10 l-34,50 Z"/><path d="M30,174 l14,10 l-34,50 Z"/></g>',
 '<rect x="58" y="196" width="34" height="30" transform="rotate(36 75 211)" stroke="#fff" stroke-width="5"/>',
 # hood
 '<path d="M-118,-60 C-150,-200 -40,-272 50,-232 C104,-206 112,-150 102,-110 L92,-60 C86,-20 70,0 60,14 L-90,24 Z"/>',
 # face profile (masked below the eyes)
 '<path d="M58,-150 L82,-112 L90,-98 L118,-76 L102,-64 L106,-40 L92,-14 L56,2 Z"/>',
 # hood rim overhanging the brow
 '<path d="M30,-222 C86,-206 100,-160 90,-120 C70,-128 60,-150 58,-150" stroke="#fff" stroke-width="5" fill="none"/>',
 # sly eye
 '<path d="M64,-108 L94,-103 L70,-97 Z" fill="#fff"/>',
 # mask line and folds
 '<path d="M58,-86 L112,-80" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
 # hood folds
 '<path d="M-60,-224 C-110,-180 -110,-110 -96,-50 M-20,-246 C-60,-190 -60,-120 -40,-60" stroke="#fff" stroke-width="3" fill="none"/>',
]

FIGS["mage"]=[
 # staff with orb
 '<rect x="176" y="-10" width="20" height="320" rx="6" stroke="#fff" stroke-width="5"/>',
 '<path d="M186,-10 C150,-30 150,-80 170,-90 M186,-10 C222,-30 222,-80 202,-90" stroke="#000" stroke-width="10" fill="none"/>',
 '<circle cx="186" cy="-58" r="30" stroke="#fff" stroke-width="5"/>',
 '<circle cx="186" cy="-58" r="16" fill="#fff"/>',
 '<path d="M186,-108 L186,-96 M136,-58 L148,-58 M224,-58 L236,-58 M150,-94 L158,-86 M222,-94 L214,-86" stroke="#000" stroke-width="4" stroke-linecap="round"/>',
 # robe
 '<path d="M-80,10 L60,10 C100,40 150,100 166,170 L176,300 L-210,300 C-200,160 -150,60 -80,10 Z"/>',
 '<path d="M-40,0 C-110,70 -150,170 -160,300" stroke="#fff" stroke-width="5" fill="none"/>',
 '<path d="M-70,30 C-120,100 -140,200 -146,300" stroke="#fff" stroke-width="2" fill="none"/>',
 # high collar
 '<path d="M-100,40 L-120,-60 L-60,-20 L-40,30 Z" stroke="#fff" stroke-width="4"/>',
 # hand on the staff
 '<path d="M148,150 C160,128 202,128 206,150 L206,190 C190,200 160,200 148,190 Z" stroke="#fff" stroke-width="5"/>',
 '<path d="M154,164 L200,164 M154,178 L200,178" stroke="#fff" stroke-width="3"/>',
 # head and face profile
 '<path d="M-70,-120 L70,-120 L78,-100 L104,-76 L86,-66 L84,-56 L-60,-20 Z"/>',
 '<path d="M60,-100 L80,-98" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
 # long beard
 '<path d="M-30,-70 C20,-70 60,-62 84,-56 C104,-30 104,30 84,90 C70,140 50,180 30,230 C20,150 -10,60 -30,-20 Z" stroke="#fff" stroke-width="5"/>',
 '<path d="M40,-40 C64,20 60,90 40,170 M10,-30 C34,30 34,100 26,150 M70,-20 C84,30 80,80 66,120" stroke="#fff" stroke-width="3" fill="none"/>',
 '<path d="M50,-58 C70,-60 92,-52 100,-36" stroke="#fff" stroke-width="4" fill="none"/>',
 # hat cone with bent tip
 '<path d="M-96,-128 L72,-134 C40,-180 0,-220 -50,-242 C-96,-262 -150,-252 -172,-222 C-130,-228 -104,-200 -96,-128 Z"/>',
 # hat brim
 '<path d="M-160,-118 C-70,-150 110,-150 168,-116 C110,-102 -70,-100 -160,-118 Z" stroke="#fff" stroke-width="5"/>',
 '<path d="M-94,-142 C-30,-152 30,-152 74,-146" stroke="#fff" stroke-width="10" fill="none"/>',
 '<g fill="#fff">'+star(-36,-184,16)+'</g>',
 '<path d="M10,-206 a14,14 0 1,0 16,22 a10,10 0 1,1 -14,-19 Z" fill="#fff"/>',
]

cls=sys.argv[1]; fig=FIGS[cls]
s.append(f'<g clip-path="url(#art)"><g transform="translate({cx+10},{cy+10}) scale(1.05)" fill="{B}" stroke-linejoin="round">'+"".join(fig)+'</g></g>')

# ---- bottom band: defense ----
s.append(divider(830))
dy=Y1-84
s.append(f'<circle cx="{X1-78}" cy="{dy}" r="44" fill="{B}"/>')
s.append(f'<g transform="translate({X1-78},{dy})" fill="{Wh}">'
         '<path d="M0,-30 L24,-21 C24,6 16,20 0,30 C-16,20 -24,6 -24,-21 Z"/>'
         f'<path d="M0,-20 L0,20 M-14,-6 L14,-6" stroke="{B}" stroke-width="4"/></g>')
s.append(f'<text x="{X1-78}" y="{dy-54}" font-family="Georgia,serif" font-size="17" font-weight="bold" text-anchor="middle" letter-spacing="3">DEF</text>')
s.append(f'<g fill="{B}">')
for i in range(6):
    s.append(star(X1-175-i*80, dy, 31))
s.append('</g>')
s.append('</svg>')
open(sys.argv[2],'w').write("\n".join(s))
