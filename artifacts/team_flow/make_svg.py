"""모형시험 DB · 프로그램 기능 · AI 에이전트 세 축을 감고 도는 순환 그림을 SVG로 만든다.
사용: python make_svg.py team_ai_flow.svg
"""
import sys
from xml.sax.saxutils import escape as e

BG = '#f6f5f2'; PANEL = '#ffffff'; INK = '#1f2328'; MUTED = '#5b6370'
NAVY = '#1d3557'; NAVYBG = '#eaf0f8'; ACC = '#d9580a'; ACCBG = '#fdf0e6'
TRACK = '#dfe5ee'
W = 1440
o = []

def rect(x, y, w, h, fill, stroke=None, sw=1, rx=7):
    a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
    o.append(a + '/>')

def text(x, y, s, size=13, fill=INK, weight=None, anchor='middle'):
    a = f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"'
    if weight: a += f' font-weight="{weight}"'
    if anchor: a += f' text-anchor="{anchor}"'
    o.append(a + f'>{e(s)}</text>')

def path(d, color, sw=3):
    o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>')

def head(x, y, direction, color, size=14):
    """수평 화살촉. direction: +1 오른쪽, -1 왼쪽."""
    b = x - direction * size
    o.append(f'<polygon points="{x:.1f},{y} {b:.1f},{y - size*0.55:.1f} {b:.1f},{y + size*0.55:.1f}" fill="{color}"/>')

# ── 제목
text(40, 48, '모형시험 DB · 프로그램 기능 · AI 에이전트, 세 축으로 도는 업무 프로그램화', 24, INK, '700', None)
text(40, 76, '모형시험 DB에서 파생되는 작업을 프로그램 기능으로 만들고 도구를 붙이면, 사용자가 묻고 AI 에이전트가 실행합니다. 사용자가 결과를 보고 Apply하면 다시 DB에 쌓입니다.', 14, MUTED, None, None)

# ── 세 축과 벨트
LX, MX, RX = 235, 600, 965
CY, R = 330, 180
TOP, BOT = CY - R, CY + R
o.append(f'<path d="M{LX},{TOP} L{RX},{TOP} A{R},{R} 0 0 1 {RX},{BOT} L{LX},{BOT} A{R},{R} 0 0 1 {LX},{TOP} Z" '
         f'fill="none" stroke="{TRACK}" stroke-width="28"/>')

BW, BH = 240, 72
B1, B2 = (LX + MX) / 2, (MX + RX) / 2   # 위·아래 상자 가운데 x
g = 7
L1, R1 = B1 - BW / 2 - g, B1 + BW / 2 + g
L2, R2 = B2 - BW / 2 - g, B2 + BW / 2 + g
# ④ → 왼쪽 축 → ①
path(f'M{L1:.1f},{BOT} L{LX},{BOT} A{R},{R} 0 0 1 {LX},{TOP} L{L1 - 6:.1f},{TOP}', NAVY)
head(L1, TOP, +1, NAVY)
# ① → ②
path(f'M{R1:.1f},{TOP} L{L2 - 6:.1f},{TOP}', NAVY)
head(L2, TOP, +1, NAVY)
# ② → 오른쪽 축 → ③
path(f'M{R2:.1f},{TOP} L{RX},{TOP} A{R},{R} 0 0 1 {RX},{BOT} L{R2 + 6:.1f},{BOT}', ACC)
head(R2, BOT, -1, ACC)
# ③ → ④
path(f'M{L2:.1f},{BOT} L{R1 + 6:.1f},{BOT}', ACC)
head(R1, BOT, -1, ACC)

# 데이터 축: 모형시험 DB
o.append(f'<circle cx="{LX}" cy="{CY}" r="115" fill="{NAVY}"/>')
text(LX, CY - 40, '데이터 축', 12.5, '#c9d6e8', '700')
text(LX, CY - 10, '모형시험 DB', 22, '#ffffff', '700')
text(LX, CY + 18, 'POW · 자항 · 반류', 13, '#c9d6e8')
text(LX, CY + 38, '풍동 · 저항', 13, '#c9d6e8')

# 기능 축: 프로그램 기능
o.append(f'<circle cx="{MX}" cy="{CY}" r="140" fill="{PANEL}" stroke="{NAVY}" stroke-width="3"/>')
text(MX, CY - 92, '기능 축', 12.5, MUTED, '700')
text(MX, CY - 66, '프로그램 기능', 20, NAVY, '700')
feats = ['Speed Power · EEDI', 'Rudder Torque', 'Propeller Weight/MOI', 'Stock Propeller',
         'LRM CAL · One Shaft · M&S', 'Deliverables 제공 기록']
for i, f in enumerate(feats):
    text(MX, CY - 36 + i * 20, f, 13, INK, '600')
text(MX, CY + 92, '+ 다음 파생 작업', 13, MUTED, '700')

# 실행 축: AI 에이전트
o.append(f'<circle cx="{RX}" cy="{CY}" r="115" fill="{ACC}"/>')
text(RX, CY - 40, '실행 축', 12.5, '#ffe3cf', '700')
text(RX, CY - 10, 'AI 에이전트', 22, '#ffffff', '700')
text(RX, CY + 18, '사내 LLM', 13, '#ffe3cf')
text(RX, CY + 38, 'Gemma 4 31B', 13, '#ffe3cf')

# 사용자
UX = 1330; PERSON = '#3b4350'
o.append(f'<circle cx="{UX}" cy="{CY - 58}" r="24" fill="{PERSON}"/>')
o.append(f'<path d="M{UX - 44},{CY + 14} Q{UX - 44},{CY - 26} {UX},{CY - 26} Q{UX + 44},{CY - 26} {UX + 44},{CY + 14} Z" fill="{PERSON}"/>')
text(UX, CY + 44, '사용자', 19, INK, '700')
text(UX, CY + 66, '화면 · 채팅으로', 12.5, MUTED)
text(UX, CY + 84, '묻고, 보고, Apply', 12.5, MUTED)
AE = RX + 115 + 8          # 에이전트 원 오른쪽 끝 + 여백
UE = UX - 60               # 사용자 왼쪽 끝
path(f'M{UE},{CY - 22} L{AE + 6},{CY - 22}', PERSON, 2.2)
head(AE, CY - 22, -1, PERSON, 12)
text((AE + UE) / 2 + 30, CY - 32, '질문', 12.5, PERSON, '700')
path(f'M{AE},{CY + 22} L{UE - 6},{CY + 22}', PERSON, 2.2)
head(UE, CY + 22, +1, PERSON, 12)
text((AE + UE) / 2 + 30, CY + 42, '결과 확인', 12.5, PERSON, '700')

# 벨트 위 단계 상자
def stage(cx, cy, title, desc, fill, stroke, tc):
    rect(cx - BW / 2, cy - BH / 2, BW, BH, fill, stroke, 1.6, 9)
    text(cx, cy - 4, title, 15.5, tc, '700')
    text(cx, cy + 20, desc, 12.5, MUTED)

stage(B1, TOP, '① 파생 작업 프로그램화', '시험 결과에서 나오는 계산을 기능으로', NAVYBG, NAVY, NAVY)
stage(B2, TOP, '② 기능마다 도구 붙이기', '에이전트가 부를 수 있게 등록', ACCBG, ACC, ACC)
stage(B2, BOT, '③ 에이전트가 도구 실행', '질문 → 도구 실행 → 결과로 답', ACCBG, ACC, ACC)
stage(B1, BOT, '④ 결과 저장 · 축적', '사용자 Apply → 케이스·산출물 기록', NAVYBG, NAVY, NAVY)

H = BOT + BH / 2 + 62
text(40, H - 24, '2026-11-09 기준 구현 상태.', 12, MUTED, None, None)
H = int(H)
svg_head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="\'Malgun Gothic\',\'Noto Sans KR\',\'Apple SD Gothic Neo\',sans-serif">\n'
            '<title>모형시험 DB · 프로그램 기능 · AI 에이전트 순환</title>\n'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>\n')
open(sys.argv[1], 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg_head + '\n'.join(o) + '\n</svg>\n')
print(H)
