"""모형시험 DB 중심 순환 그림(프로그램화 → 도구 → 챗봇 실행 → 결과 축적)을 SVG로 만든다.
사용: python make_svg.py team_ai_flow.svg
"""
import math, sys
from xml.sax.saxutils import escape as e

BG = '#f6f5f2'; PANEL = '#ffffff'; INK = '#1f2328'; MUTED = '#5b6370'; LINE = '#c9c5bc'
NAVY = '#1d3557'; NAVYBG = '#eaf0f8'; ACC = '#d9580a'; ACCBG = '#fdf0e6'
DASH = '5 4'
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

def head(x, y, dx, dy, color, size=11):
    """(x,y)에서 (dx,dy) 방향을 가리키는 화살촉."""
    n = math.hypot(dx, dy); ux, uy = dx / n, dy / n
    bx, by = x - ux * size, y - uy * size
    px, py = -uy * size * 0.55, ux * size * 0.55
    o.append(f'<polygon points="{x:.1f},{y:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{color}"/>')

# ── 제목
text(40, 48, '모형시험 DB 중심 업무 프로그램화와 챗봇 순환', 24, INK, '700')
text(40, 76, '모형시험 DB에서 파생되는 작업을 프로그램 기능으로 만들고, 기능마다 챗봇 도구를 붙여 실행합니다. 결과는 다시 쌓여 다음 작업의 바탕이 됩니다.', 14, MUTED)

# ── 순환 고리
CX, CY, R = 400, 420, 232
BW, BH = 250, 80
stages = [  # (각도, 제목, 설명, 채움, 테두리, 제목색, 설명색)
    (-90, '① 파생 작업 프로그램화', '시험 결과에서 나오는 계산을 기능으로', NAVYBG, NAVY, NAVY, MUTED),
    (0,   '② 기능마다 도구 붙이기', '챗봇이 부를 수 있게 등록', ACCBG, ACC, ACC, MUTED),
    (90,  '③ 챗봇이 도구 실행', '질문 → 도구 실행 → 결과로 답', ACC, ACC, '#ffffff', '#ffe3cf'),
    (180, '④ 결과 저장 · 축적', '사용자 Apply → 케이스·산출물 기록', NAVYBG, NAVY, NAVY, MUTED),
]
# 바탕 고리
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#dfe5ee" stroke-width="26"/>')
# 호: 각 상자 사이 (시계 방향)
arcs = [(-53, -15), (15, 53), (127, 165), (195, 233)]
for a0, a1 in arcs:
    p0 = (CX + R * math.cos(math.radians(a0)), CY + R * math.sin(math.radians(a0)))
    p1 = (CX + R * math.cos(math.radians(a1)), CY + R * math.sin(math.radians(a1)))
    o.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{R},{R} 0 0 1 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{NAVY}" stroke-width="3"/>')
    t = math.radians(a1)
    head(p1[0] + 4 * -math.sin(t), p1[1] + 4 * math.cos(t), -math.sin(t), math.cos(t), NAVY, 14)

# ④ → ① 호 옆 설명
text(CX - 250, CY - 178, '쌓인 결과로', 12.5, NAVY, '700', 'middle')
text(CX - 250, CY - 160, '다음 파생 작업', 12.5, NAVY, '700', 'middle')

# 가운데 모형시험 DB
o.append(f'<circle cx="{CX}" cy="{CY}" r="96" fill="{NAVY}"/>')
text(CX, CY - 12, '모형시험 DB', 20, '#ffffff', '700', 'middle')
text(CX, CY + 14, 'POW · 자항 · 반류', 12.5, '#c9d6e8', None, 'middle')
text(CX, CY + 33, '풍동 · 저항', 12.5, '#c9d6e8', None, 'middle')

stage_box = {}
for ang, title, desc, fill, stroke, tc, dc in stages:
    bx = CX + R * math.cos(math.radians(ang)) - BW / 2
    by = CY + R * math.sin(math.radians(ang)) - BH / 2
    rect(bx, by, BW, BH, fill, stroke, 1.6, 9)
    text(bx + BW / 2, by + 33, title, 15.5, tc, '700', 'middle')
    text(bx + BW / 2, by + 56, desc, 12.5, dc, None, 'middle')
    stage_box[ang] = (bx, by)

# ── 오른쪽: 지금 프로그램화된 작업
PX, PY, PW = 800, 128, 360
feats = [
    ('Speed Power · EEDI Speed', '시험 기반 속도·마력'),
    ('Rudder Torque', '케이스 · PDF 양식 시트 · 유사선 초기설계'),
    ('Propeller Weight/MOI', 'ProDes 엔진 · 선급 Rule Check'),
    ('Stock Propeller', '설계점 · 후보 · 중량'),
    ('LRM CAL · One Shaft · M&S', '엔진 한계선 · 단축 운항'),
    ('Deliverables 제공 기록', '값 · 날짜 · 받는 곳 · 엑셀/PDF'),
]
FH, FG = 48, 8
PH = 74 + (len(feats) + 1) * (FH + FG) + 8
rect(PX, PY, PW, PH, PANEL, NAVY, 2, 10)
text(PX + 18, PY + 32, '지금 프로그램화된 작업', 16, NAVY, '700')
text(PX + 18, PY + 54, '모두 모형시험 DB를 입력으로 쓰고, 각각 챗봇 도구를 붙임', 12, MUTED)
fy = PY + 74
for name, detail in feats:
    rect(PX + 16, fy, PW - 32, FH, NAVYBG, rx=6)
    text(PX + 28, fy + 20, name, 13.5, INK, '600')
    text(PX + 28, fy + 38, detail, 12, MUTED)
    fy += FH + FG
rect(PX + 16, fy, PW - 32, FH, PANEL, MUTED, 1.2, 6, DASH)
text(PX + 28, fy + 20, '+ 다음 파생 작업', 13.5, MUTED, '700')
text(PX + 28, fy + 38, '같은 방식으로 기능화 → 도구 추가', 12, MUTED)

# ① 상자 → 패널 연결
bx, by = stage_box[-90]
y1 = by + BH / 2
o.append(f'<line x1="{bx+BW+6:.1f}" y1="{y1:.1f}" x2="{PX-10}" y2="{y1:.1f}" stroke="{NAVY}" stroke-width="1.6" stroke-dasharray="{DASH}"/>')
head(PX - 2, y1, 1, 0, NAVY, 10)
text((bx + BW + PX) / 2, y1 - 8, '지금까지 구현', 12, NAVY, '700', 'middle')

H = max(PY + PH, CY + R + BH / 2) + 50
text(40, H - 22, '2026-11-09 기준 구현 상태.', 12, MUTED)
H = int(H)
svg_head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="\'Malgun Gothic\',\'Noto Sans KR\',\'Apple SD Gothic Neo\',sans-serif">\n'
            '<title>모형시험 DB 중심 업무 프로그램화와 챗봇 순환</title>\n'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>\n')
open(sys.argv[1], 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg_head + '\n'.join(o) + '\n</svg>\n')
print(H)
