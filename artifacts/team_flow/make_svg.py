"""모형시험 DB 중심 프로그램화 → 챗봇 도구 연결 그림을 SVG로 만든다.
사용: python make_svg.py team_ai_flow.svg
"""
import sys
from xml.sax.saxutils import escape as e

BG = '#f6f5f2'; PANEL = '#ffffff'; INK = '#1f2328'; MUTED = '#5b6370'; LINE = '#c9c5bc'
NAVY = '#1d3557'; NAVYBG = '#eaf0f8'; ACC = '#d9580a'; ACCBG = '#fdf0e6'
MONO = "Consolas,'D2Coding',monospace"
DASH = '5 4'
W = 1200
o = []

def rect(x, y, w, h, fill, stroke=None, sw=1, rx=7, dash=None):
    a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: a += f' stroke-dasharray="{dash}"'
    o.append(a + '/>')

def text(x, y, s, size=13, fill=INK, weight=None, anchor=None, family=None):
    a = f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"'
    if weight: a += f' font-weight="{weight}"'
    if anchor: a += f' text-anchor="{anchor}"'
    if family: a += f' font-family="{family}"'
    o.append(a + f'>{e(s)}</text>')

def arrow(x1, x2, y, color=MUTED, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x1}" y1="{y}" x2="{x2-7}" y2="{y}" stroke="{color}" stroke-width="1.6"{d}/>')
    o.append(f'<polygon points="{x2},{y} {x2-8},{y-4.5} {x2-8},{y+4.5}" fill="{color}"/>')

# 열 위치
DBX, DBW = 40, 190
FX, FW = 300, 300
TX, TW = 630, 280
CX, CW = 980, 180

# (기능, 설명, 도구 줄들, 상태) 상태: 'on' 도구 연결됨, 'todo' 도구 연결 예정, 'new' 추가할 작업
rows = [
    ('시험 결과 조회 · 그래프', 'POW · 자항 · 풍동 곡선', ['wind_chart'], 'on'),
    ('Speed Power · EEDI Speed', '시험 기반 속도·마력', ['compare_speed_power'], 'on'),
    ('Rudder Torque', '케이스 · PDF 양식 시트 · 유사선 초기설계', ['calc_rudder_torque', 'rudder_torque · rudder_torque_pdf'], 'on'),
    ('Propeller Weight/MOI', 'ProDes 엔진 · 선급 Rule Check', ['propeller_moi'], 'on'),
    ('Stock Propeller', '설계점 · 후보 · 중량', ['stock_propeller'], 'on'),
    ('LRM CAL · One Shaft · M&S', '엔진 한계선 · 단축 운항', ['도구 연결 예정'], 'todo'),
    ('Deliverables 제공 기록', '값 · 날짜 · 받는 곳 · 엑셀/PDF', ['도구 연결 예정'], 'todo'),
    ('+ 파생 작업 추가', '모형시험 DB에서 나오는 다음 작업', ['+ 도구 추가'], 'new'),
]

rect(0, 0, W, 10, BG, rx=0)  # 자리표시 — 아래에서 높이 확정 후 교체
text(40, 48, '모형시험 DB 중심 프로그램화와 챗봇 도구 연결', 24, INK, '700')
text(40, 76, '모형시험 DB에서 파생되는 작업을 모두 프로그램 기능으로 만들고, 기능마다 도구를 붙여 챗봇이 각각 실행하게 합니다.', 14, MUTED)

HY = 124
text(DBX, HY, '① 기반 데이터', 14, NAVY, '700')
text(FX, HY, '② 프로그램화한 작업', 14, NAVY, '700')
text(TX, HY, '③ 기능별 챗봇 도구', 14, ACC, '700')
text(CX, HY, '④ AI 챗봇', 14, ACC, '700')

RH, RG = 56, 10
Y0 = HY + 22
Y1 = Y0 + len(rows) * (RH + RG) - RG

# ① 모형시험 DB
rect(DBX, Y0, DBW, Y1 - Y0, NAVY, rx=10)
cx = DBX + DBW / 2
text(cx, Y0 + 44, '모형시험 DB', 21, '#ffffff', '700', 'middle')
text(cx, Y0 + 66, '해석 결과', 12.5, '#c9d6e8', None, 'middle')
items = ['POW', '자항', '반류', '풍동', '저항']
iy = Y0 + (Y1 - Y0) / 2 - (len(items) * 46 - 10) / 2
for it in items:
    rect(DBX + 24, iy, DBW - 48, 36, '#2b4a75', rx=6)
    text(cx, iy + 23, it, 14, '#ffffff', '600', 'middle')
    iy += 46
text(cx, Y1 - 40, '모든 계산의', 12.5, '#c9d6e8', None, 'middle')
text(cx, Y1 - 22, '공통 입력', 12.5, '#c9d6e8', None, 'middle')

# ④ AI 챗봇
rect(CX, Y0, CW, Y1 - Y0, ACC, rx=10)
ccx = CX + CW / 2
text(ccx, Y0 + 44, 'AI 챗봇', 21, '#ffffff', '700', 'middle')
text(ccx, Y0 + 66, '사내 LLM · Gemma 4 31B', 12, '#ffe3cf', None, 'middle')
sy = Y0 + 120
steps = ['질문', '도구 실행', '프로그램 결과로 답']
for i, s in enumerate(steps):
    rect(CX + 16, sy, CW - 32, 36, '#ffffff', rx=6)
    text(ccx, sy + 23, s, 13.5, ACC, '700', 'middle')
    sy += 36
    if i < len(steps) - 1:
        o.append(f'<polygon points="{ccx},{sy+14} {ccx-6},{sy+5} {ccx+6},{sy+5}" fill="#ffffff"/>')
        sy += 18
sy += 30
for line in ['숫자는 계산 결과로만', '저장은 사용자가 Apply']:
    text(ccx, sy, line, 12.5, '#ffffff', None, 'middle'); sy += 20
sy += 18
text(ccx, sy, '공통 도구', 12, '#ffe3cf', '700', 'middle')
rect(CX + 16, sy + 10, CW - 32, 30, '#c24d07', rx=6)
text(ccx, sy + 30, 'open_screen', 12.5, '#ffffff', '700', 'middle', MONO)
text(ccx, sy + 58, '화면 이동', 12, '#ffe3cf', None, 'middle')

# ②③ 행
y = Y0
for name, detail, tools, st in rows:
    mid = y + RH / 2
    dash = None if st == 'on' else DASH
    arrow(DBX + DBW + 6, FX - 6, mid, NAVY, None if st != 'new' else DASH)
    if st == 'new':
        rect(FX, y, FW, RH, PANEL, MUTED, 1.2, 7, DASH)
        text(FX + 14, y + 24, name, 14, MUTED, '700')
        text(FX + 14, y + 43, detail, 12, MUTED)
    else:
        rect(FX, y, FW, RH, NAVYBG, NAVY, 1.2, 7)
        text(FX + 14, y + 24, name, 14, INK, '600')
        text(FX + 14, y + 43, detail, 12, MUTED)
    arrow(FX + FW + 4, TX - 4, mid, ACC if st == 'on' else MUTED, dash)
    if st == 'on':
        rect(TX, y, TW, RH, ACCBG, ACC, 1.2, 7)
        if len(tools) == 1:
            text(TX + 14, mid + 5, tools[0], 13, INK, '700', family=MONO)
        else:
            text(TX + 14, y + 24, tools[0], 12.5, INK, '700', family=MONO)
            text(TX + 14, y + 43, tools[1], 12.5, INK, '700', family=MONO)
    else:
        rect(TX, y, TW, RH, PANEL, MUTED, 1.2, 7, DASH)
        text(TX + 14, mid + 5, tools[0], 13, MUTED, '600')
    arrow(TX + TW + 6, CX - 6, mid, ACC if st == 'on' else MUTED, dash)
    y += RH + RG

# 범례 · 각주
ly = Y1 + 34
rect(40, ly - 12, 26, 16, NAVYBG, NAVY, 1.2, 4)
text(74, ly + 1, '구현됨', 12.5, MUTED)
rect(140, ly - 12, 26, 16, PANEL, MUTED, 1.2, 4, DASH)
text(174, ly + 1, '도구 연결 · 작업 추가 예정', 12.5, MUTED)
text(40, ly + 28, '2026-11-09 기준 구현 상태. 도구 이름은 현재 코드의 챗봇 도구.', 12, MUTED)

H = ly + 48
o[0] = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>'
head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="\'Malgun Gothic\',\'Noto Sans KR\',\'Apple SD Gothic Neo\',sans-serif">\n'
        '<title>모형시험 DB 중심 프로그램화와 챗봇 도구 연결</title>\n')
open(sys.argv[1], 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + head + '\n'.join(o) + '\n</svg>\n')
print(H)
