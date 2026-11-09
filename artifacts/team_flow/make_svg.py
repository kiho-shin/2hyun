"""모형시험 DB(데이터 축)와 AI 에이전트(실행 축) 두 축으로 도는 순환 그림을 SVG로 만든다.
사용: python make_svg.py team_ai_flow.svg
"""
import sys
from xml.sax.saxutils import escape as e

BG = '#f6f5f2'; PANEL = '#ffffff'; INK = '#1f2328'; MUTED = '#5b6370'
NAVY = '#1d3557'; NAVYBG = '#eaf0f8'; ACC = '#d9580a'; ACCBG = '#fdf0e6'
TRACK = '#dfe5ee'; DASH = '5 4'
W = 1200
o = []

def rect(x, y, w, h, fill, stroke=None, sw=1, rx=7, dash=None):
    a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: a += f' stroke-dasharray="{dash}"'
    o.append(a + '/>')

def text(x, y, s, size=13, fill=INK, weight=None, anchor=None):
    a = f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"'
    if weight: a += f' font-weight="{weight}"'
    if anchor: a += f' text-anchor="{anchor}"'
    o.append(a + f'>{e(s)}</text>')

def path(d, color, sw=3):
    o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>')

def head(x, y, direction, color, size=14):
    """수평 화살촉. direction: +1 오른쪽, -1 왼쪽."""
    b = x - direction * size
    o.append(f'<polygon points="{x},{y} {b},{y - size*0.55:.1f} {b},{y + size*0.55:.1f}" fill="{color}"/>')

# ── 제목
text(40, 48, '모형시험 DB와 AI 에이전트, 두 축으로 도는 업무 프로그램화', 24, INK, '700')
text(40, 76, '모형시험 DB에서 파생되는 작업을 프로그램 기능으로 만들고 도구를 붙이면, AI 에이전트가 실행하고 결과는 다시 DB에 쌓입니다.', 14, MUTED)

# ── 두 축과 벨트
LX, RX, CY, R = 230, 970, 335, 170
TOP, BOT = CY - R, CY + R
o.append(f'<path d="M{LX},{TOP} L{RX},{TOP} A{R},{R} 0 0 1 {RX},{BOT} L{LX},{BOT} A{R},{R} 0 0 1 {LX},{TOP} Z" '
         f'fill="none" stroke="{TRACK}" stroke-width="28"/>')

BW, BH = 240, 72
B1, B2 = 445, 755          # 위·아래 상자 가운데 x
gap = 7
# ④ → (왼쪽 축을 돌아) → ①
path(f'M{B1 - BW/2 - gap},{BOT} L{LX},{BOT} A{R},{R} 0 0 1 {LX},{TOP} L{B1 - BW/2 - gap - 6},{TOP}', NAVY)
head(B1 - BW/2 - gap, TOP, +1, NAVY)
# ① → ②
path(f'M{B1 + BW/2 + gap},{TOP} L{B2 - BW/2 - gap - 6},{TOP}', NAVY)
head(B2 - BW/2 - gap, TOP, +1, NAVY)
# ② → (오른쪽 축을 돌아) → ③
path(f'M{B2 + BW/2 + gap},{TOP} L{RX},{TOP} A{R},{R} 0 0 1 {RX},{BOT} L{B2 + BW/2 + gap + 6},{BOT}', ACC)
head(B2 + BW/2 + gap, BOT, -1, ACC)
# ③ → ④
path(f'M{B2 - BW/2 - gap},{BOT} L{B1 + BW/2 + gap + 6},{BOT}', ACC)
head(B1 + BW/2 + gap, BOT, -1, ACC)

# 데이터 축
o.append(f'<circle cx="{LX}" cy="{CY}" r="118" fill="{NAVY}"/>')
text(LX, CY - 40, '데이터 축', 12.5, '#c9d6e8', '700', 'middle')
text(LX, CY - 10, '모형시험 DB', 22, '#ffffff', '700', 'middle')
text(LX, CY + 18, 'POW · 자항 · 반류', 13, '#c9d6e8', None, 'middle')
text(LX, CY + 38, '풍동 · 저항', 13, '#c9d6e8', None, 'middle')

# 실행 축
o.append(f'<circle cx="{RX}" cy="{CY}" r="118" fill="{ACC}"/>')
text(RX, CY - 40, '실행 축', 12.5, '#ffe3cf', '700', 'middle')
text(RX, CY - 10, 'AI 에이전트', 22, '#ffffff', '700', 'middle')
text(RX, CY + 18, '사내 LLM', 13, '#ffe3cf', None, 'middle')
text(RX, CY + 38, 'Gemma 4 31B', 13, '#ffe3cf', None, 'middle')

# 벨트 위 단계 상자
def stage(cx, cy, title, desc, fill, stroke, tc):
    rect(cx - BW / 2, cy - BH / 2, BW, BH, fill, stroke, 1.6, 9)
    text(cx, cy - 4, title, 15.5, tc, '700', 'middle')
    text(cx, cy + 20, desc, 12.5, MUTED, None, 'middle')

stage(B1, TOP, '① 파생 작업 프로그램화', '시험 결과에서 나오는 계산을 기능으로', NAVYBG, NAVY, NAVY)
stage(B2, TOP, '② 기능마다 도구 붙이기', '에이전트가 부를 수 있게 등록', ACCBG, ACC, ACC)
stage(B2, BOT, '③ 에이전트가 도구 실행', '질문 → 도구 실행 → 결과로 답', ACCBG, ACC, ACC)
stage(B1, BOT, '④ 결과 저장 · 축적', '사용자 Apply → 케이스·산출물 기록', NAVYBG, NAVY, NAVY)

# ── 두 축 사이: 지금 프로그램화된 기능
PX, PW = 372, 456
feats = ['Speed Power · EEDI', 'Rudder Torque', 'Propeller Weight/MOI', 'Stock Propeller',
         'LRM CAL · One Shaft · M&S', 'Deliverables 제공 기록']
CH, CG = 34, 8
PH = 52 + 4 * (CH + CG) - CG + 14
PY = CY - PH / 2
rect(PX, PY, PW, PH, PANEL, NAVY, 1.6, 10)
text(PX + PW / 2, PY + 30, '지금 프로그램화된 기능', 15, NAVY, '700', 'middle')
colw = (PW - 32 - 10) / 2
y = PY + 52
for i, f in enumerate(feats):
    x = PX + 16 + (i % 2) * (colw + 10)
    rect(x, y + (i // 2) * (CH + CG), colw, CH, NAVYBG, rx=6)
    text(x + colw / 2, y + (i // 2) * (CH + CG) + 22, f, 12.5, INK, '600', 'middle')
y += 3 * (CH + CG)
rect(PX + 16, y, PW - 32, CH, PANEL, MUTED, 1.2, 6, DASH)
text(PX + PW / 2, y + 22, '+ 다음 파생 작업도 같은 방식으로', 12.5, MUTED, '700', 'middle')

H = BOT + BH / 2 + 62
text(40, H - 24, '2026-11-09 기준 구현 상태.', 12, MUTED)
H = int(H)
svg_head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="\'Malgun Gothic\',\'Noto Sans KR\',\'Apple SD Gothic Neo\',sans-serif">\n'
            '<title>모형시험 DB와 AI 에이전트, 두 축으로 도는 업무 프로그램화</title>\n'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>\n')
open(sys.argv[1], 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg_head + '\n'.join(o) + '\n</svg>\n')
print(H)
