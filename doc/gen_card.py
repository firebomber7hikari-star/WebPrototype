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

# ---- art ----
cx,cy=512,466
s.append(f'<circle cx="{cx}" cy="{cy}" r="252" fill="none" stroke="{B}" stroke-width="2"/>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="240" fill="none" stroke="{B}" stroke-width="1" stroke-dasharray="4 8"/>')
s.append(f'<line x1="{cx-200}" y1="{cy+232}" x2="{cx+200}" y2="{cy+232}" stroke="{B}" stroke-width="4" stroke-linecap="round"/>')
g=f'<g transform="translate({cx},{cy+8})" fill="{B}" stroke-linejoin="round">'
fig=[
 # cape
 '<path d="M-30,-118 C-95,-80 -120,40 -150,210 L-60,200 C-55,110 -40,10 -10,-100 Z"/>',
 # sword (far hand, raised behind)
 '<g transform="translate(-58,-120) rotate(-28)">'
   '<polygon points="-8,-20 8,-20 8,-150 0,-168 -8,-150"/>'
   '<line x1="0" y1="-30" x2="0" y2="-145" stroke="#fff" stroke-width="2"/>'
   '<rect x="-30" y="-22" width="60" height="11" rx="4"/><rect x="-6" y="-12" width="12" height="34"/><circle cx="0" cy="26" r="9"/></g>',
 # far arm
 '<path d="M-10,-112 L-62,-140 L-48,-160 L5,-128 Z"/>',
 # legs
 '<path d="M-28,20 L-62,135 L-70,212 L-28,214 L-30,150 L5,40 Z"/>',
 '<path d="M-72,206 L-22,206 L-18,226 L-80,226 Z"/>',
 '<path d="M5,20 L58,120 L70,206 L108,208 L92,118 L42,15 Z"/>',
 '<path d="M64,200 L118,204 L128,226 L60,226 Z"/>',
 # torso
 '<path d="M-38,-122 C-10,-140 45,-138 62,-118 C78,-70 60,-20 50,25 L-40,25 C-48,-20 -52,-80 -38,-122 Z"/>',
 # belt
 '<rect x="-46" y="14" width="102" height="18" rx="3"/>',
 '<rect x="2" y="16" width="16" height="14" fill="none" stroke="#fff" stroke-width="3"/>',
 # tassets
 '<path d="M-44,32 L56,32 L66,72 L-50,72 Z"/>',
 '<line x1="6" y1="34" x2="8" y2="70" stroke="#fff" stroke-width="3"/>',
 # neck & helmet
 '<rect x="-2" y="-152" width="34" height="34"/>',
 '<path d="M-28,-170 C-30,-235 50,-250 66,-195 L74,-160 L56,-160 L54,-140 L-20,-140 C-30,-148 -30,-160 -28,-170 Z"/>',
 # plume
 '<path d="M-5,-232 C-60,-262 -110,-230 -120,-180 C-95,-210 -55,-215 -20,-205 Z"/>',
 # helmet details (white)
 '<path d="M20,-188 L68,-188" stroke="#fff" stroke-width="7" stroke-linecap="round"/>',
 '<path d="M-24,-200 C0,-208 30,-210 62,-205" stroke="#fff" stroke-width="3" fill="none"/>',
 
 # shoulder pauldron
 '<path d="M-30,-128 C-20,-150 40,-150 52,-118 C40,-102 -10,-100 -30,-128 Z" stroke="#fff" stroke-width="4"/>',
 # shield on near arm (front)
 '<circle cx="78" cy="-40" r="88" stroke="#fff" stroke-width="5"/>',
 '<circle cx="78" cy="-40" r="70" fill="none" stroke="#fff" stroke-width="3"/>',
 '<circle cx="78" cy="-40" r="18" fill="#fff"/><circle cx="78" cy="-40" r="8"/>',
 '<path d="M78,-110 L78,-58 M78,-22 L78,30 M8,-40 L60,-40 M96,-40 L148,-40" stroke="#fff" stroke-width="3"/>',
]
s.append(g+"".join(fig)+'</g>')

# name plate
s.append(divider(740))
s.append(f'<text x="512" y="798" font-family="Georgia,serif" font-size="40" font-weight="bold" text-anchor="middle" letter-spacing="12">WARRIOR</text>')

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
