from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent; A=R/'assets';A.mkdir(exist_ok=True)
F='/System/Library/Fonts/STHeiti Light.ttc'
def font(s):return ImageFont.truetype(F,s)
def base(title,sub,h=820):
 im=Image.new('RGB',(1600,h),'#f7f9fc');d=ImageDraw.Draw(im);d.text((65,43),title,font=font(46),fill='#15253a');d.text((65,112),sub,font=font(27),fill='#53667e');return im,d
def box(d,xy,title,lines,color='#e7effc'):
 d.rounded_rectangle(xy,radius=22,fill=color,outline='#ccd7e5',width=2);x,y,xx,yy=xy;d.text((x+24,y+22),title,font=font(32),fill='#16375d')
 for j,s in enumerate(lines):d.text((x+24,y+78+j*42),s,font=font(25),fill='#34475f')
def arrow(d,x,y,xx,yy):
 d.line((x,y,xx,yy),fill='#4b76bd',width=5);d.polygon([(xx,yy),(xx-14,yy-9),(xx-14,yy+9)],fill='#4b76bd')
im,d=base('同一个任务，费用来自完整调用过程','Pi / Claude Code / OpenCode 同用 Opus 5.5')
box(d,(60,195,480,470),'客户端',['Pi / Claude Code','OpenCode','系统提示＋工具定义＋用户任务'])
box(d,(575,195,1000,470),'MaxRouter · 模型 API',['Messages / Responses 协议','每轮返回回答或工具调用','保留真实 usage，不本地估算'])
box(d,(1095,195,1535,470),'本地工具与项目副本',['客户端执行读取与编辑','只修改 README','工具结果进入下一轮输入'])
arrow(d,485,310,570,310);arrow(d,1005,310,1090,310)
d.line((1300,477,1300,535,280,535,280,477),fill='#4b76bd',width=4);d.text((490,548),'多轮交互：前一轮工具结果会成为后续输入',font=font(27),fill='#34475f')
box(d,(60,635,1535,770),'整个任务统一核对',['累计输入、输出、缓存读取/写入  →  请求消费记录  →  专用 Key 总额与实际扣费'],'#e3f2ed')
im.save(A/'context-cost-flow.png')
im,d=base('先证明任务完成，再比较费用','文档任务的验收：命令有来源、范围没越界、结果不夸大',850)
steps=[('1 · 同一起点',['同一项目版本','相同任务提示']),('2 · 查找依据',['package.json / 锁文件','Vite 配置 / 原 README']),('3 · 完成修改',['只补本地开发说明','不修改代码或依赖']),('4 · 独立验收',['核对全部真实命令','原有说明与文件哈希']),('5 · 核实结果',['基线类型检查和测试','不伪造 Agent 执行通过']),('6 · 对账',['全轮输入输出与缓存','全部实际费用纳入'])]
for j,(title,lines)in enumerate(steps):
 row=j//3;col=j%3;x=60+col*510;y=195+row*285;box(d,(x,y,x+450,y+220),title,lines,'#e7effc'if row==0 else'#e3f2ed')
 if col<2:arrow(d,x+455,y+110,x+505,y+110)
d.text((65,780),'未完成、超范围或对账失败，都不能当作“省费成功案例”。',font=font(28),fill='#7b3c2b');im.save(A/'task-acceptance-flow.png')
print('created 2 original diagrams')
import json
S=json.loads((R/'project-comparison.json').read_text())
im,d=base('同用 Opus 5.5，本次 Pi 的费用更低','同一项目任务、最终验收通过；Pi 费用包含审校修正',930)
d.text((420,177),'累计输入 Token',font=font(29),fill='#53667e');d.text((1160,177),'实际扣费（USD）',font=font(29),fill='#53667e')
labels={'pi':'Pi 1.5.0','claude':'Claude Code 2.1.308','opencode':'OpenCode 1.19.5','codex':'Codex 0.154.0'}
T=[x for x in S['task_results'] if x['model']=='anthropic-claude-opus-5.5']
for j,x in enumerate(T):
 y=246+j*183
 if x['client']=='codex':d.rounded_rectangle((45,y-25,1550,y+135),radius=20,fill='#edf0f5')
 d.text((65,y),labels[x['client']],font=font(31),fill='#162a44')
 model='GPT 6.1 Sol（不同模型）'if x['client']=='codex'else'Opus 5.5'
 d.text((65,y+47),model,font=font(24),fill='#53667e')
 if x['client']=='claude':d.text((65,y+83),'本地结构适配',font=font(23),fill='#795932')
 else:d.text((65,y+83),str(x['calls'])+' 次调用'+('，含修正'if x['client']=='pi'else''),font=font(23),fill='#53667e')
 w=570*x['input_tokens']/max(t['input_tokens']for t in T);d.rounded_rectangle((420,y+4,420+w,y+39),radius=7,fill='#497ec8');d.text((420+w+12,y-1),f"{x['input_tokens']:,}",font=font(27),fill='#16375d')
 d.text((420,y+55),f"输出 {x['output_tokens']:,} · 缓存读 {x['cache_read_tokens']:,} / 写 {x['cache_write_tokens']:,}",font=font(23),fill='#53667e')
 usd=float(x['actual_usd']);cw=350*usd/max(float(t['actual_usd'])for t in T);d.rounded_rectangle((1160,y+4,1160+cw,y+39),radius=7,fill='#3a9e81');d.text((1160,y+54),'$'+x['actual_usd'],font=font(29),fill='#1f644f')
d.text((65,845),'输入已含缓存，不重复相加。每款仅一个任务；实际优惠与缓存命中不同，不作固定排名。',font=font(25),fill='#53667e')
im.save(A/'project-results.png');print('created measured results chart from verified JSON')
