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

# ---- art: warrior bust, side profile facing right ----
cx,cy,R=512,513,272
s.append(f'<defs><clipPath id="art"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="{R+14}" fill="none" stroke="{B}" stroke-width="2"/>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="{R+6}" fill="none" stroke="{B}" stroke-width="1" stroke-dasharray="4 8"/>')
fig=[
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
open(sys.argv[1],'w').write("\n".join(s))
