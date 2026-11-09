import sys
from xml.sax.saxutils import escape as e

BG='#f6f5f2'; PANEL='#ffffff'; INK='#1f2328'; MUTED='#5b6370'; LINE='#d6d3cc'
NAVY='#1d3557'; NAVYBG='#eaf0f8'; ACC='#d9580a'; ACCBG='#fdf0e6'
DONE='#2e7d32'; DOING='#b86e00'; PLAN='#6b7280'
MONO="Consolas,'D2Coding',monospace"
W, H = 1200, 900
o=[]
def rect(x,y,w,h,fill,stroke=None,sw=1,rx=7,dash=None):
    a=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: a+=f' stroke-dasharray="{dash}"'
    o.append(a+'/>')
def text(x,y,s,size=13,fill=INK,weight=None,anchor=None,family=None):
    a=f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"'
    if weight: a+=f' font-weight="{weight}"'
    if anchor: a+=f' text-anchor="{anchor}"'
    if family: a+=f' font-family="{family}"'
    o.append(a+f'>{e(s)}</text>')
def spans(x,y,parts):
    a=f'<text x="{x}" y="{y}">'
    for i,(t,size,fill,weight) in enumerate(parts):
        a+=f'<tspan{" dx=\"6\"" if i else ""} font-size="{size}" fill="{fill}"{f" font-weight=\"{weight}\"" if weight else ""}>{e(t)}</tspan>'
    o.append(a+'</text>')
def arrow(x1,x2,y,color=MUTED):
    o.append(f'<line x1="{x1}" y1="{y}" x2="{x2-7}" y2="{y}" stroke="{color}" stroke-width="1.6"/>')
    o.append(f'<polygon points="{x2},{y} {x2-8},{y-4.5} {x2-8},{y+4.5}" fill="{color}"/>')

rect(0,0,W,H,BG,rx=0)
text(40,48,'선형추진기개발팀 업무 — 모형시험 DB 기반 AI화 흐름',24,INK,'700')
text(40,76,'업무는 모형시험 DB 기반 계산 프로그램의 기능으로 처리하고, AI 챗봇은 그 기능을 도구로 불러 씁니다.',14,MUTED)

# ── 구현된 기능 박스
PX,PY,PW,PH=40,100,1120,250
rect(PX,PY,PW,PH,PANEL,NAVY,2,9)
spans(PX+16,PY+30,[('계산 프로그램에 현재 구현된 기능',15,NAVY,'700'),('2026-11-09 기준',12,MUTED,None)])
def feat(x,y,w,name,detail,doing=False):
    if doing:
        rect(x,y,w,50,PANEL,DOING,1.2,6,'5 4')
        spans(x+10,y+21,[(name,13.5,INK,'600'),('· 진행 중',12,DOING,'700')])
    else:
        rect(x,y,w,50,NAVYBG,rx=6)
        text(x+10,y+21,name,13.5,INK,'600')
    text(x+10,y+40,detail,12,MUTED)
gy=PY+58; fy=gy+12
c1x=PX+16; c2x=c1x+220+16; c3x=c2x+548+16
text(c1x,gy,'모형시험',12.5,MUTED,'700'); text(c2x,gy,'설계 계산',12.5,MUTED,'700'); text(c3x,gy,'산출물 · 챗봇',12.5,MUTED,'700')
feat(c1x,fy,220,'모형시험 해석 DB','POW · 자항 · 반류 · 풍동 · 저항')
calc=[('Speed Power · EEDI Speed','시험 기반 속도·마력'),('Rudder Torque','케이스 · PDF 양식 시트 · 유사선 초기설계'),
      ('Propeller Weight/MOI','ProDes 엔진 · 선급 Rule Check'),('Stock Propeller','설계점 · 후보 · 중량'),
      ('LRM CAL · One Shaft · M&S','엔진 한계선 · 단축 운항')]
for i,(n,d) in enumerate(calc):
    feat(c2x+(i%2)*278, fy+(i//2)*58, 270, n, d)
feat(c3x,fy,288,'Deliverables 제공 기록','값 · 날짜 · 받는 곳 · 엑셀/PDF')
feat(c3x,fy+58,288,'AI 챗봇','계산·조회 도구 호출, 화면 이동',doing=True)

# ── 흐름
TX,TW=40,330; AX1=TX+TW; PRX,PRW=410,350; AIX,AIW=800,360
hy=PY+PH+44
text(TX,hy,'팀 업무',14,MUTED,'700'); text(PRX,hy,'프로그램 기능',14,NAVY,'700'); text(AIX,hy,'AI 챗봇 도구',14,ACC,'700')
text(TX,hy+19,'업무표 항목',12,MUTED); text(PRX,hy+19,'모형시험 DB와 계산',12,MUTED); text(AIX,hy+19,'질문 → 도구 호출 → 답',12,MUTED)
rows=[
 ('done','구현','추진기 중량 추정 · Rule Check','Propeller Weight/MOI · Stock Propeller','ProDes 엔진 · 선급 Rule Check','propeller_moi · stock_propeller','중량·MOI 계산, Stock 후보 조회',True),
 ('doing','개선 중','Rudder Torque · S/G 용량 산정','Rudder Torque','케이스 · PDF 양식 시트 · 유사선 초기설계','calc_rudder_torque · rudder_torque_pdf','토크 계산, 시트 PDF 출력',True),
 ('doing','일부','표준선 프로모션 지원','모형시험 DB · Speed Power','발표자료 제작 기능은 계획','compare_speed_power','시험 결과 조회, 속도·마력 비교 그래프',True),
 ('plan','계획','선형/추진기 개발 일정 검토','개발 일정 검토 (추가)','입력 필요: 단계별 표준 리드타임','계획','Key Event 날짜 → 착수 필요시점 역산',False),
 ('plan','계획','모형시험 비용 Check-List','비용 Check-List (추가)','입력 필요: 지급 단계별 필요 문서','계획','시험 건별 필요 문서·품의 안내',False),
]
SC={'done':DONE,'doing':DOING,'plan':PLAN}
RH,RG=56,10; ry=hy+34
for st,lbl,task,pn,pd,an,ad,tool in rows:
    c=SC[st]; dash=None if st!='plan' else '5 4'
    rect(TX,ry,TW,RH,PANEL,LINE,1,7)
    rect(TX,ry,6,RH,c,rx=2)
    text(TX+20,ry+34,task,15,INK,'600')
    text(TX+TW-14,ry+22,lbl,12,c,'700','end')
    arrow(AX1+6,PRX-6,ry+RH/2)
    rect(PRX,ry,PRW,RH,NAVYBG,NAVY,1.2,7,dash)
    text(PRX+14,ry+23,pn,14,INK,'600'); text(PRX+14,ry+43,pd,12,MUTED)
    arrow(PRX+PRW+6,AIX-6,ry+RH/2)
    rect(AIX,ry,AIW,RH,ACCBG,ACC,1.2,7,dash)
    if tool: text(AIX+14,ry+23,an,13,INK,'700',family=MONO)
    else: text(AIX+14,ry+23,an,14,INK,'600')
    text(AIX+14,ry+43,ad,12,MUTED)
    ry+=RH+RG

# ── 원칙
ry+=10
rect(40,ry,1120,40,PANEL,LINE,1,7)
spans(56,ry+25,[('챗봇 원칙',13.5,ACC,'700'),('— 숫자는 프로그램 계산 결과로만 답하고, 저장은 사용자가 Apply로 확정합니다. (사내 LLM 게이트웨이, Gemma 4 31B)',13.5,INK,None)])

# ── 진행 단계
ry+=62
text(40,ry+19,'진행 단계',13.5,MUTED,'700')
chips=[('① 계산 기능 프로그램 이식',190,DONE,None,PANEL),('② 데이터·화면 정리',150,DOING,None,PANEL),
       ('③ 챗봇 도구화',118,DOING,None,PANEL),('④ 일정 검토·비용 체크리스트 추가',236,MUTED,'5 4',PANEL)]
x=116
for i,(s,w,c,d,f) in enumerate(chips):
    rect(x,ry,w,28,f,c if d is None else LINE,1.2,14,d)
    text(x+w/2,ry+19,s,13,c,'600' if d is None else None,'middle')
    x+=w
    if i<len(chips)-1:
        arrow(x+8,x+26,ry+14); x+=34

ry+=60
text(40,ry,'2026-11-09 기준 프로그램 상태. 원 표 7건 중 개발 보고서 작성과 Full Specification 검토는 프로그램과 연결이 약해 제외했습니다.',12,MUTED)
H=int(ry+28)
o[0]=f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>'
head=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="\'Malgun Gothic\',\'Noto Sans KR\',\'Apple SD Gothic Neo\',sans-serif">\n'
      '<title>선형추진기개발팀 업무 — 모형시험 DB 기반 AI화 흐름</title>\n')
open(sys.argv[1],'w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n'+head+'\n'.join(o)+'\n</svg>\n')
print(H)
