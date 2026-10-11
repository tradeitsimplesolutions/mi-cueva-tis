# Genera index.html (landing del kit) y guia-dia-0.html (versión imprimible / PDF)
import json, html, re
R = lambda f: open(f, encoding='utf-8').read()
PROMPT = R('src_prompt_dia1.txt')
DIRECTOR = R('src_director.txt')
SKILLS = R('src_skills.txt')
METODO = R('src_metodo.txt')
SKILL_DIAG = ('---\nname: diagnostico\ndescription: Convierte mi experiencia de trading en sistema: '
              'entrevista de 10 preguntas, diagnóstico profesional, hipótesis comprobables, mis 3 primeras '
              'skills, mi primer agente investigador y un plan de 7 días. Úsala cuando escriba /diagnostico.\n---\n\n' + PROMPT)
IDEA = ('Director, esta es mi idea: Compro ___ cuando ___. Salgo cuando ___. Stop: ___. Horario: ___.\n'
        'Pásala por las fases 01 a 03 y guarda la ficha en fichas/')

ZIP = 'https://tradeitsimplesolutions.github.io/mi-cueva-tis/mi-cueva-tis.zip'
CUEVA = 'https://tradeitsimplesolutions.github.io/mi-cueva-tis/'
TESTER = 'https://tradeitsimplesolutions.github.io/mega-cueva-tester/'
PDF = 'Tu_Dia_0_Reto_Cueva.pdf'

def esc(s): return html.escape(s, quote=False)
def data(id_, txt): return f'<script type="application/json" id="{id_}">{json.dumps(txt, ensure_ascii=False).replace("</", "<\\/")}</script>'

CSS_BASE = r'''
:root{
  --bg:#0a0806;--bg2:#13100c;--bg3:#1c1711;--line:#3a3025;--line2:#251f18;
  --muted:#a0948a;--cream:#efe6d5;--cream2:#d9cdb8;
  --gold:#f2b544;--gold2:#d9a441;--golddim:rgba(242,181,68,.14);--green:#2ecc6a;
  --display:'Unbounded',sans-serif;--body:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--cream);font-family:var(--body);line-height:1.55;font-size:16px;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.wrap{width:min(1180px,calc(100% - 32px));margin:0 auto}
.mono{font-family:var(--mono)}
.gold{color:var(--gold)}
.label{font-family:var(--mono);font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:0}
h1,h2,h3{font-family:var(--display);letter-spacing:-.03em;margin:0;line-height:1.05;text-wrap:balance}
h2{font-size:clamp(30px,4.6vw,56px)}
h3{font-size:clamp(20px,2.2vw,26px);line-height:1.15}
p{margin:0}
.grid-bg{position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(rgba(242,181,68,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(242,181,68,.06) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 70% 40%,#000 10%,transparent 70%);-webkit-mask-image:radial-gradient(ellipse at 70% 40%,#000 10%,transparent 70%)}

/* top */
.top{position:sticky;top:0;z-index:40;background:rgba(10,8,6,.88);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line2)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;height:62px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand img{height:30px;width:auto}
.brand span{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--cream2)}
.nav{display:flex;gap:4px}
.nav a{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-decoration:none;padding:8px 12px;border-radius:999px;border:1px solid transparent}
.nav a:hover{color:var(--gold);border-color:var(--line)}
.status{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.status i{width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 14px var(--gold);animation:pulse 1.8s infinite}
@keyframes pulse{50%{opacity:.35}}

/* hero */
.hero{position:relative;overflow:hidden;padding:72px 0 64px;border-bottom:1px solid var(--line2)}
.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 75% 35%,rgba(242,181,68,.16),transparent 38%);pointer-events:none}
.hero .wrap{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.hero h1{font-size:clamp(40px,6.4vw,84px);font-weight:800;margin:20px 0 22px;letter-spacing:-.045em;line-height:.98}
.hero h1 em{font-style:normal;color:var(--gold)}
.hero .lead{font-size:clamp(17px,1.6vw,21px);color:var(--cream2);max-width:600px}
.eye{position:relative;aspect-ratio:1;border-radius:50%;overflow:hidden;box-shadow:0 0 0 1px rgba(242,181,68,.35),0 0 90px rgba(242,181,68,.18)}
.eye img{width:100%;height:100%;object-fit:cover}
.eye::after{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle,transparent 58%,rgba(10,8,6,.75) 100%)}
.eye-tag{position:absolute;left:50%;bottom:6%;transform:translateX(-50%);z-index:2;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;background:rgba(10,8,6,.85);border:1px solid rgba(242,181,68,.5);color:var(--cream);padding:7px 12px;border-radius:6px;white-space:nowrap}
.eye-tag b{color:var(--gold);font-weight:500}

.count{margin-top:34px;border:1px solid var(--line);background:linear-gradient(180deg,rgba(242,181,68,.06),transparent),var(--bg2);border-radius:14px;padding:18px 20px;max-width:560px}
.count .label{font-size:11px}
.cells{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}
.cell{text-align:center;border:1px solid var(--line2);border-radius:10px;padding:10px 4px;background:var(--bg)}
.cell b{display:block;font-family:var(--display);font-size:clamp(26px,4vw,40px);font-weight:800;color:var(--gold);line-height:1;font-variant-numeric:tabular-nums}
.cell span{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.count .when{margin-top:12px;font-size:14px;color:var(--muted)}
.ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;padding:14px 20px;border-radius:10px;border:1px solid var(--gold);background:var(--gold);color:#140f07;font-weight:700;cursor:pointer;transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translateY(-1px);box-shadow:0 8px 30px rgba(242,181,68,.25)}
.btn.ghost{background:transparent;color:var(--gold)}
.btn.sm{font-size:12px;padding:10px 14px}

/* sections */
section{padding:84px 0;border-bottom:1px solid var(--line2);position:relative}
.head{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;margin-bottom:36px}
.head p.sub{max-width:480px;color:var(--muted);font-size:16px}
.head .label{margin-bottom:14px}

/* first steps */
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.s3{border:1px solid var(--line);border-radius:14px;padding:22px;background:var(--bg2);position:relative}
.s3 .n{font-family:var(--mono);font-size:12px;color:var(--gold);letter-spacing:.14em}
.s3 h3{font-size:19px;margin:10px 0 8px}
.s3 p{color:var(--muted);font-size:15px}

/* tabs */
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}
.tab{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;background:var(--bg2);color:var(--muted);border:1px solid var(--line);padding:12px 16px;border-radius:999px;cursor:pointer;display:flex;align-items:center;gap:10px}
.tab b{font-family:var(--display);font-size:15px;color:var(--cream2);letter-spacing:0}
.tab[aria-selected="true"]{border-color:var(--gold);color:var(--gold);background:var(--golddim)}
.tab[aria-selected="true"] b{color:var(--gold)}
.panel[hidden]{display:none}
.day-intro{display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:center;margin-bottom:26px}
.big{font-family:var(--display);font-weight:900;font-size:clamp(70px,10vw,130px);line-height:.8;color:transparent;-webkit-text-stroke:1.5px rgba(242,181,68,.55);letter-spacing:-.06em}
.day-intro h3{font-size:clamp(24px,3vw,36px);margin:8px 0 10px}
.day-intro p{color:var(--cream2);max-width:720px}

.res{border:1px solid var(--line);border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.02),transparent),var(--bg2);padding:28px;margin-bottom:16px}
.res-top{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap;margin-bottom:20px}
.kind{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);border:1px solid rgba(242,181,68,.5);border-radius:999px;padding:5px 10px;margin-bottom:10px}
.res-top h3{max-width:640px}
.res-top .acts{display:flex;gap:8px;flex-wrap:wrap}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.box{border:1px solid var(--line2);border-radius:12px;padding:18px 20px;background:rgba(10,8,6,.5)}
.box .label{font-size:11px;margin-bottom:10px}
.box ul,.box ol{margin:0;padding-left:20px;color:var(--cream2);font-size:15px}
.box li{margin:6px 0}
.box li::marker{color:var(--gold)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-size:13px;border:1px solid var(--line);border-radius:999px;padding:6px 12px;color:var(--cream2);background:var(--bg)}
kbd,code{font-family:var(--mono);font-size:.88em;background:var(--bg3);border:1px solid var(--line2);border-radius:5px;padding:1px 6px;color:var(--cream);word-break:break-word}

.code{margin-top:18px;border:1px solid var(--line);border-radius:12px;background:#070605;overflow:hidden}
.code-bar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 14px;border-bottom:1px solid var(--line2);font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.code-bar .dots{display:flex;gap:6px}.code-bar .dots i{width:9px;height:9px;border-radius:50%;background:var(--line)}
.code pre{margin:0;padding:18px;max-height:320px;overflow:auto;font-family:var(--mono);font-size:12.5px;line-height:1.6;color:var(--cream2);white-space:pre-wrap;word-break:break-word}
.code.open pre{max-height:none}
.more{background:none;border:0;color:var(--gold);font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;padding:0}
.copy{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;background:var(--gold);color:#140f07;border:0;border-radius:6px;padding:7px 11px;font-weight:700;cursor:pointer}
.copy.done{background:var(--green)}
.note{margin-top:14px;font-size:14px;color:var(--muted)}
.note b{color:var(--cream2)}

.rules4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:6px}
.r4{border:1px solid var(--line);border-radius:12px;padding:18px;background:var(--bg)}
.r4 b{display:block;font-family:var(--display);font-size:28px;color:var(--gold);line-height:1;margin-bottom:8px}
.r4 span{font-size:14px;color:var(--cream2)}
.phases{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.ph{border:1px solid var(--line2);border-radius:10px;padding:12px;font-size:14px;color:var(--cream2);background:var(--bg)}
.ph i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--gold);display:block;margin-bottom:4px;letter-spacing:.08em}

/* calendar */
.cal{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.cd{border:1px solid var(--line);border-radius:14px;padding:20px;background:var(--bg2);position:relative;overflow:hidden;min-height:220px;display:flex;flex-direction:column}
.cd .n{position:absolute;right:10px;top:2px;font-family:var(--display);font-weight:900;font-size:72px;color:rgba(242,181,68,.08);line-height:1}
.cd .d{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.cd h3{font-size:18px;margin:12px 0 8px}
.cd .f{font-size:13px;color:var(--muted)}
.cd .e{margin-top:auto;padding-top:12px;border-top:1px solid var(--line2);font-size:13px;color:var(--cream2)}
.cd .e::before{content:"Entregable → ";font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--green)}
.cd.live{border-color:rgba(242,181,68,.45)}

/* guía */
.guide{background:radial-gradient(circle at 20% 0%,rgba(242,181,68,.08),transparent 40%)}
.pages{display:flex;flex-direction:column;gap:22px}
.page{position:relative;border:1px solid var(--line);border-radius:18px;background:var(--bg2);padding:44px 48px;overflow:hidden}
.page::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(var(--gold),transparent)}
.pg-top{display:flex;justify-content:space-between;gap:16px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:22px}
.pg-top b{color:var(--gold);font-weight:500}
.page h3.ptitle{font-size:clamp(26px,3.4vw,40px);margin-bottom:16px}
.page p{color:var(--cream2);margin-bottom:12px;max-width:820px}
.letter{display:grid;grid-template-columns:240px 1fr;gap:36px;align-items:start}
.portrait{border-radius:14px;overflow:hidden;position:relative;border:1px solid rgba(242,181,68,.35)}
.portrait::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(10,8,6,.85))}
.portrait span{position:absolute;left:12px;bottom:10px;z-index:2;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.sign{font-family:var(--display);font-size:18px;color:var(--gold);margin-top:6px}
.check{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.check li{display:grid;grid-template-columns:26px 1fr;gap:12px;align-items:start;border:1px solid var(--line2);border-radius:10px;padding:12px 14px;background:rgba(10,8,6,.45)}
.check input{appearance:none;-webkit-appearance:none;width:22px;height:22px;border:1.5px solid var(--gold2);border-radius:6px;margin:1px 0 0;cursor:pointer;position:relative;background:transparent}
.check input:checked{background:var(--gold)}
.check input:checked::after{content:"✓";position:absolute;inset:0;display:grid;place-items:center;color:#140f07;font-weight:800;font-size:14px}
.check b{color:var(--cream)}
.check span{color:var(--cream2);font-size:15px}
.check small{display:block;color:var(--muted);font-size:13px;margin-top:2px}
.tag{display:inline-block;font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:2px}
.tag.y{background:var(--golddim);color:var(--gold)}.tag.n{background:rgba(239,68,68,.14);color:#f08a8a}.tag.o{background:rgba(160,148,138,.16);color:var(--muted)}
.ex{display:grid;gap:12px}
.exi{border:1px solid var(--line);border-radius:12px;padding:18px 20px;background:rgba(10,8,6,.45)}
.exi .h{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:6px}
.exi h4{margin:0;font-family:var(--display);font-size:17px}
.exi .t{font-family:var(--mono);font-size:11px;color:var(--gold);letter-spacing:.1em;text-transform:uppercase}
.exi p{font-size:15px;margin-bottom:6px}
.exi .out{font-size:14px;color:var(--muted)}
.exi .out b{color:var(--green);font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:500}
.fill{font-family:var(--mono);font-size:13px;color:var(--cream);background:var(--bg);border:1px dashed var(--line);border-radius:8px;padding:10px 12px;margin:8px 0}
.rem{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.rm{border:1px solid var(--line2);border-radius:12px;padding:16px 18px;background:rgba(10,8,6,.45)}
.rm b{display:block;font-family:var(--display);font-size:15px;margin-bottom:6px;color:var(--cream)}
.rm span{font-size:14px;color:var(--cream2)}
.rm strong{color:var(--cream)}
.vipbox{margin-top:16px;border:1px solid rgba(242,181,68,.5);border-radius:12px;padding:16px 18px;background:var(--golddim);font-size:15px;color:var(--cream2)}
.vipbox b{color:var(--gold)}
.mini-cal{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:6px 0 18px}
.mc{border:1px solid var(--line2);border-radius:10px;padding:12px;background:rgba(10,8,6,.45);font-size:13px;color:var(--cream2)}
.mc b{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:6px}
.guide-actions{display:flex;gap:10px;flex-wrap:wrap}
.pg-foot{margin-top:26px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border-top:1px solid var(--line2);padding-top:12px}

footer{padding:40px 0 60px;color:var(--muted);font-size:13px}
footer .wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;border-top:1px solid var(--line2);padding-top:24px}
footer img{height:26px;width:auto;opacity:.85}
footer p{max-width:720px}

.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);opacity:0;transition:.25s;background:var(--gold);color:#140f07;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;padding:12px 18px;border-radius:10px;z-index:90;pointer-events:none}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}

@media(max-width:980px){
  .hero .wrap{grid-template-columns:1fr}.eye{max-width:420px;margin:0 auto;width:100%}
  .head{display:block}.head p.sub{margin-top:14px}
  .cal{grid-template-columns:1fr 1fr}.cols2{grid-template-columns:1fr}
  .rules4,.phases{grid-template-columns:1fr 1fr}.nav{display:none}
  .letter{grid-template-columns:1fr}.portrait{max-width:260px}
  .mini-cal{grid-template-columns:1fr 1fr}
}
@media(max-width:640px){
  body{font-size:15px}
  .hero{padding:44px 0 48px}
  .steps3,.cal,.rem{grid-template-columns:1fr}
  .page{padding:28px 20px}.res{padding:20px}
  .day-intro{grid-template-columns:1fr;gap:6px}
  .status{display:none}
  .cells{gap:6px}
  section{padding:60px 0}
}
'''

PRINT_CSS = r'''
@page{size:A4;margin:0}
html,body{background:#0a0806}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pages{gap:0}
.page{width:210mm;height:297mm;border-radius:0;border:0;padding:16mm 16mm 14mm;page-break-after:always;break-after:page;display:flex;flex-direction:column}
.page:last-child{page-break-after:auto;break-after:auto}
.page .pg-foot{margin-top:auto;display:flex;justify-content:space-between;font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border-top:1px solid var(--line2);padding-top:8px}
.page p{font-size:13.5px}
.check span,.exi p,.rm span{font-size:13px}
.check li{padding:9px 12px}
.letter{grid-template-columns:62mm 1fr;gap:9mm}
.mini-cal{grid-template-columns:repeat(5,1fr)}
.rem{grid-template-columns:1fr 1fr}
body::after{display:none}
.rules4{grid-template-columns:repeat(4,1fr);gap:8px}.r4{padding:10px 12px}.r4 b{font-size:20px;margin-bottom:4px}.r4 span{font-size:12px}
.rm{padding:12px 14px}.vipbox{font-size:13px;padding:12px 14px}
'''

# ---------- contenido de la guía (se usa en la landing y en el PDF) ----------
def page(n, kicker, inner):
    return f'''<article class="page" id="g{n}">
  <div class="pg-top"><span>Tu Día 0 · Reto Cueva de Trading</span><b>{n:02d} / 05 · {kicker}</b></div>
  {inner}
  <div class="pg-foot"><span>Trade It Simple · @mariellangsaez</span><span>Contenido educativo · no es asesoría financiera</span></div>
</article>'''

G1 = page(1, 'Bienvenida', f'''
  <div class="letter">
    <div class="portrait"><img src="img/mariel-oro.jpg" alt="Mariel Lang Sáez" width="700" height="700"><span>Mariel · desde la Cueva</span></div>
    <div>
      <p class="label" style="margin-bottom:12px">Acceso concedido</p>
      <h3 class="ptitle">Bienvenida a la Cueva, tortuga.</h3>
      <p>Ya estás dentro. A partir del <b>domingo 25 de octubre</b> pasamos cinco días construyendo juntos, y el <b>jueves 29</b> sales con dos estrategias con su código, tu robot corriendo en un servidor y tu primer mini portafolio.</p>
      <p>Hoy no tienes que entender todo. Tienes que llegar <b>preparado</b>, y para eso es esta guía: en unas dos horas, repartidas como quieras antes del domingo, dejas tus accesos listos, instalas lo básico y calientas con tres ejercicios cortos. Así el Día 1 lo usamos para construir, no para pelear con instalaciones.</p>
      <p>Una sola idea para llevarte desde ya: <b>lo rentable es la estrategia, no tú.</b> No hace falta ser un genio. Hace falta un método que diga «no» antes que tu cuenta, y eso es lo que vamos a montar.</p>
      <p>Si en algún momento te atascas, es normal: le pasa a todo el mundo. Para eso está el grupo.</p>
      <p class="sign">Nos vemos el domingo en la Cueva.<br>— Mariel y el equipo TIS</p>
    </div>
  </div>
  <div class="rem" style="margin-top:22px">
    <div class="rm"><b>Esta guía tiene 5 páginas</b><span>01 Bienvenida · 02 Tus accesos y descargas · 03 Tres ejercicios de calentamiento · 04 Lo que tienes que recordar · 05 Tu semana y el checklist final.</span></div>
    <div class="rm"><b>Tiempo total: ~2 horas</b><span>Accesos e instalación: 40 min. Ejercicios: 75 min. No hace falta saber programar ni tener capital.</span></div>
  </div>''')

G2 = page(2, 'Accesos y descargas', '''
  <h3 class="ptitle">Antes del domingo: deja esto listo.</h3>
  <p>Marca cada casilla cuando la tengas. Lo que dice <span class="tag n">todavía no</span> es igual de importante: no gastes dinero antes de tiempo.</p>
  <ul class="check">
    <li><input type="checkbox" data-k="a1"><span><b>Entra a la plataforma del Reto</b> <span class="tag y">obligatorio</span><small>Con el mismo correo con el que compraste. El acceso te llegó en el correo de bienvenida. Ahí se suben los 5 entregables.</small></span></li>
    <li><input type="checkbox" data-k="a2"><span><b>Únete a la comunidad de WhatsApp</b> <span class="tag y">obligatorio</span><small>El enlace está en tu correo de bienvenida. Por ahí se avisan los horarios y los enlaces de cada directo. Si eres VIP, únete también a tu grupo VIP.</small></span></li>
    <li><input type="checkbox" data-k="a3"><span><b>Guarda nuestro correo como contacto</b> <span class="tag y">obligatorio</span><small>Y revisa la carpeta de spam o promociones. Si no te llegó nada, escríbenos por WhatsApp.</small></span></li>
    <li><input type="checkbox" data-k="a4"><span><b>Instala Visual Studio Code</b> <span class="tag o">recomendado</span><small>Es gratis: <code>code.visualstudio.com/download</code>. Es donde vive tu cueva. El domingo lo montamos juntos; si lo instalas antes, ganas tiempo.</small></span></li>
    <li><input type="checkbox" data-k="a5"><span><b>Crea tus cuentas gratis de GitHub y de Claude</b> <span class="tag o">recomendado</span><small>GitHub te da Copilot gratis dentro de VS Code; Claude (<code>claude.ai</code>) es tu copiloto. Qué plan necesitas exactamente te lo decimos el Día 1: para prepararte basta la cuenta gratis.</small></span></li>
    <li><input type="checkbox" data-k="a6"><span><b>Crea tu cuenta gratis de TradingView</b> <span class="tag o">recomendado</span><small>De ahí sacas los datos de precios (CSV) para el ejercicio 3 y para el Día 2.</small></span></li>
    <li><input type="checkbox" data-k="a7"><span><b>Descarga tu Cueva TIS</b> <span class="tag o">recomendado</span><small>El regalo del Día 2 de la Mega Cueva. Está en el Kit de la Cueva, pestaña Día 2. Lo usas en el ejercicio 2.</small></span></li>
    <li><input type="checkbox" data-k="a8"><span><b>El servidor (VPS) para tu robot</b> <span class="tag n">todavía no</span><small>No está incluido y no lo compres aún: el martes 27 te decimos cuál contratar y el miércoles 28 lo configuramos juntos.</small></span></li>
    <li><input type="checkbox" data-k="a9"><span><b>Bloquea 2 horas al día del 25 al 29</b> <span class="tag y">obligatorio</span><small>En tu calendario, ya. Si no puedes en directo, todo queda grabado hasta el 13 de diciembre.</small></span></li>
  </ul>''')

G3 = page(3, 'Calentamiento', '''
  <h3 class="ptitle">Tres ejercicios para llegar con ventaja.</h3>
  <p>No son tareas del Reto ni cuentan para la garantía. Son para que el domingo llegues con material propio y no en blanco.</p>
  <div class="ex">
    <div class="exi">
      <div class="h"><h4>1 · Tu diagnóstico</h4><span class="t">30 min · regalo Día 1</span></div>
      <p>Copia el prompt del Día 1 (Kit de la Cueva, pestaña Día 1), pégalo en Claude, ChatGPT o Gemini y responde sus preguntas con honestidad. Si no tienes experiencia, dilo: también funciona. De lo que te devuelva, quédate con <b>tus 3 mejores hipótesis</b> y escríbelas así:</p>
      <div class="fill">Compro ______ cuando ______. Salgo cuando ______.</div>
      <p class="out"><b>Llevas al Día 1 →</b> tu nivel sistemático y 3 hipótesis escritas.</p>
    </div>
    <div class="exi">
      <div class="h"><h4>2 · Tu primera ficha</h4><span class="t">30 min · regalo Día 2</span></div>
      <p>Abre tu Cueva TIS en VS Code (o usa la ruta «¿Prefieres tu chat?») y pásale al Director tu mejor hipótesis. Pide las fases 01 a 03. La fase 02 saldrá <b>PENDIENTE</b> si no tienes datos: es lo correcto, el método no inventa cifras.</p>
      <div class="fill">Regla completa = activo + condición que se pueda medir + salida escrita antes de entrar</div>
      <p class="out"><b>Llevas al Día 1 →</b> una ficha con tu regla en pasos numerados.</p>
    </div>
    <div class="exi">
      <div class="h"><h4>3 · Habla en datos</h4><span class="t">15 min · prepara el Día 2</span></div>
      <p>En TradingView (computadora), abre el gráfico del activo de tu hipótesis en <b>diario</b> o <b>1 hora</b>, menú del gráfico → <i>Exportar datos del gráfico</i>, y guarda el CSV en la carpeta <code>datos/</code> de tu cueva. Mira las fechas: cuantos más años, mejor.</p>
      <p class="out"><b>Llevas al Día 2 →</b> tu primer archivo de datos, listo para explorar.</p>
    </div>
  </div>
  <p class="note" style="margin-top:14px"><b>Bonus:</b> pasa la misma idea por el Megacueva Tester y mira su veredicto X/4. Si no aprueba, ¡bien! Acabas de ver el método funcionando.</p>''')

G4 = page(4, 'Recuerda', '''
  <h3 class="ptitle">Lo que tienes que recordar.</h3>
  <div class="rem">
    <div class="rm"><b>Un día, una misión, un entregable</b><span>Cada día tiene su contenido, su misión y un entregable. Lo subes al <strong>buzón de esa misión en la plataforma</strong>, no al WhatsApp.</span></div>
    <div class="rm"><b>3 directos, el resto en vídeo</b><span>Directos el domingo 25, el miércoles 28 y el jueves 29. Lunes y martes, vídeos y ejercicios a tu ritmo, con office hours.</span></div>
    <div class="rm"><b>Los horarios llegan por la comunidad</b><span>La hora y el enlace de cada directo se avisan en el grupo de WhatsApp. Activa sus notificaciones.</span></div>
    <div class="rm"><b>Todo queda grabado</b><span>Si no puedes en directo, lo ves después. Tienes acceso a la plataforma y a las grabaciones hasta el 13 de diciembre.</span></div>
    <div class="rm"><b>Pide ayuda pronto</b><span>Si te bloqueas, escribe en el grupo o en los foros en cuanto pase. Pedir ayuda también es condición de la garantía.</span></div>
    <div class="rm"><b>No necesitas capital</b><span>Trabajamos con datos históricos. Nadie opera con dinero real durante el Reto.</span></div>
  </div>
  <div class="vipbox" style="margin-top:16px"><b>Tu garantía del 100 %.</b> Si completas las 5 misiones tal como se entregan y no terminas con una estrategia backtesteada y un robot corriendo en tu VPS, te devolvemos el pago. Para eso: sube los 5 entregables dentro de las fechas del Reto, sigue los pasos con las herramientas indicadas (incluido contratar tu VPS), pide ayuda si te bloqueas y solicítala por escrito hasta el 3 de noviembre, adjuntando tus entregables.</div>
  <p style="margin-top:18px" class="label">Los 4 números que no se negocian</p>
  <div class="rules4" style="margin-top:10px">
    <div class="r4"><b>≥ 1,3</b><span>Factor de beneficio</span></div>
    <div class="r4"><b>≥ 30</b><span>Operaciones</span></div>
    <div class="r4"><b>&lt; 20 %</b><span>Caída máxima</span></div>
    <div class="r4"><b>&gt; 1</b><span>Factor de beneficio sin la mejor operación</span></div>
  </div>
  <p class="note">Siempre fuera de muestra y con costes. No se bajan nunca para que algo pase.</p>''')

G5 = page(5, 'Tu semana', '''
  <h3 class="ptitle">Tu semana en la Cueva.</h3>
  <div class="mini-cal">
    <div class="mc"><b>Dom 25 · directo</b>Método TIS y tus herramientas → entorno y repositorio listos</div>
    <div class="mc"><b>Lun 26 · vídeo</b>Pensar en datos → tu primera hipótesis</div>
    <div class="mc"><b>Mar 27 · vídeo</b>Claude, código y backtest → tu primera curva de equity</div>
    <div class="mc"><b>Mié 28 · directo</b>Tu primer sistema automatizado → robot instalado</div>
    <div class="mc"><b>Jue 29 · directo</b>Visión de portafolio → 2 estrategias en un mini portafolio</div>
  </div>
  <p class="label" style="margin-bottom:10px">Llegas listo al domingo si…</p>
  <ul class="check">
    <li><input type="checkbox" data-k="f1"><span><b>Entraste a la plataforma y estás en la comunidad de WhatsApp.</b></span></li>
    <li><input type="checkbox" data-k="f2"><span><b>Tienes VS Code instalado y tus cuentas de GitHub y Claude creadas.</b></span></li>
    <li><input type="checkbox" data-k="f3"><span><b>Tienes tus 3 hipótesis escritas</b> con «Compro ___ cuando ___. Salgo cuando ___.»</span></li>
    <li><input type="checkbox" data-k="f4"><span><b>Sabes dónde está tu cueva</b> (la carpeta con EMPEZAR y AGENTS.md) y tienes un CSV en <code>datos/</code>.</span></li>
    <li><input type="checkbox" data-k="f5"><span><b>Tienes las 2 horas bloqueadas</b> del domingo 25 al jueves 29.</span></li>
  </ul>
  <div class="vipbox"><b>Si eres VIP,</b> además de todo lo anterior tienes tu grupo VIP con Mariel, 2 estrategias extra con sus códigos (4 en total), una clase en directo al cierre y el banco de 100 ideas de trading con sus fuentes. Todo te llega por tu grupo VIP y por la plataforma.</div>
  <p style="margin-top:18px;font-family:var(--display);font-size:20px;color:var(--cream)">El domingo empiezas en cero. <span class="gold">El jueves tienes un robot.</span></p>''')

GUIDE = '\n'.join([G1, G2, G3, G4, G5])

FONTS = ''
FONTFACE = "@font-face{font-family:'Unbounded';font-style:normal;font-weight:500;font-display:swap;src:url(fonts/unbounded-latin-500-normal.woff2) format('woff2')}\n@font-face{font-family:'Unbounded';font-style:normal;font-weight:700;font-display:swap;src:url(fonts/unbounded-latin-700-normal.woff2) format('woff2')}\n@font-face{font-family:'Unbounded';font-style:normal;font-weight:800;font-display:swap;src:url(fonts/unbounded-latin-800-normal.woff2) format('woff2')}\n@font-face{font-family:'Unbounded';font-style:normal;font-weight:900;font-display:swap;src:url(fonts/unbounded-latin-900-normal.woff2) format('woff2')}\n@font-face{font-family:'Manrope';font-style:normal;font-weight:400;font-display:swap;src:url(fonts/manrope-latin-400-normal.woff2) format('woff2')}\n@font-face{font-family:'Manrope';font-style:normal;font-weight:500;font-display:swap;src:url(fonts/manrope-latin-500-normal.woff2) format('woff2')}\n@font-face{font-family:'Manrope';font-style:normal;font-weight:600;font-display:swap;src:url(fonts/manrope-latin-600-normal.woff2) format('woff2')}\n@font-face{font-family:'Manrope';font-style:normal;font-weight:700;font-display:swap;src:url(fonts/manrope-latin-700-normal.woff2) format('woff2')}\n@font-face{font-family:'Manrope';font-style:normal;font-weight:800;font-display:swap;src:url(fonts/manrope-latin-800-normal.woff2) format('woff2')}\n@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:400;font-display:swap;src:url(fonts/jetbrains-mono-latin-400-normal.woff2) format('woff2')}\n@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:500;font-display:swap;src:url(fonts/jetbrains-mono-latin-500-normal.woff2) format('woff2')}\n@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:700;font-display:swap;src:url(fonts/jetbrains-mono-latin-700-normal.woff2) format('woff2')}"

CSS = FONTFACE + CSS_BASE

def code(id_, title, txt, more=True):
    return f'''<div class="code" data-src="{id_}">
  <div class="code-bar"><span class="dots"><i></i><i></i><i></i></span><span>{title}</span><button class="copy" data-copy="{id_}">Copiar</button></div>
  <pre>{esc(txt)}</pre>
</div>
' + ('<button class="more" data-more>Ver completo ↓</button>' if more else '') + '''

INDEX = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Kit de la Cueva · Reto Cueva de Trading</title>
<meta name="description" content="Tus recursos de la Mega Cueva y tu guía Día 0 para llegar listo al Reto Cueva de Trading.">
<meta property="og:title" content="Kit de la Cueva · Acceso concedido">
<meta property="og:description" content="Tus prompts, tu Cueva TIS, el tester y tu guía Día 0. Para alumnos del Reto Cueva de Trading.">
<meta property="og:image" content="img/acceso.jpg">
<link rel="icon" href="img/logo-tiss.png">
{FONTS}
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="#top"><img src="img/logo-tiss.png" alt="TIS" width="120" height="30"><span>Kit de la Cueva</span></a>
    <nav class="nav"><a href="#recursos">Recursos</a><a href="#semana">Tu semana</a><a href="#dia0">Tu Día 0</a></nav>
    <div class="status"><i></i> Solo alumnos</div>
  </div>
</header>

<main id="top">
<section class="hero">
  <div class="grid-bg"></div>
  <div class="wrap">
    <div>
      <p class="label">Reto Cueva de Trading · Recursos para alumnos</p>
      <h1>Acceso concedido,<br><em>tortuga.</em></h1>
      <p class="lead">Aquí tienes todo lo que te llevaste de la Mega Cueva, listo para copiar y descargar, y tu guía <b>Día 0</b> para llegar al domingo con el trabajo empezado.</p>
      <div class="count" role="timer" aria-live="off">
        <p class="label">El Reto empieza en</p>
        <div class="cells">
          <div class="cell"><b id="cd-d">--</b><span>días</span></div>
          <div class="cell"><b id="cd-h">--</b><span>horas</span></div>
          <div class="cell"><b id="cd-m">--</b><span>min</span></div>
          <div class="cell"><b id="cd-s">--</b><span>seg</span></div>
        </div>
        <p class="when" id="cd-when">Domingo 25 de octubre · los horarios de cada directo se avisan en la comunidad.</p>
      </div>
      <div class="ctas">
        <a class="btn" href="#recursos">Ver mis recursos ↓</a>
        <a class="btn ghost" href="#dia0">Mi guía Día 0</a>
      </div>
    </div>
    <div class="eye"><img src="img/acceso.jpg" alt="Mariel con el ojo robótico en dorado: acceso concedido" width="900" height="900"><div class="eye-tag">● Alumno <b>verificado</b></div></div>
  </div>
</section>

<section id="empieza" style="padding-top:56px;padding-bottom:56px">
  <div class="wrap">
    <div class="steps3">
      <div class="s3"><span class="n">01 · HOY</span><h3>Revisa tu correo de bienvenida</h3><p>Ahí están tu acceso a la plataforma y el enlace a tu grupo de WhatsApp. Si no lo ves, mira en spam o promociones.</p></div>
      <div class="s3"><span class="n">02 · ESTA SEMANA</span><h3>Usa tus regalos de la Mega Cueva</h3><p>El prompt de diagnóstico, tu Cueva TIS y el tester. Los tienes justo debajo, cada uno con su «cómo usarlo».</p></div>
      <div class="s3"><span class="n">03 · ANTES DEL DOMINGO</span><h3>Haz tu Día 0</h3><p>Una guía de 5 páginas: accesos, descargas y 3 ejercicios cortos. Unas 2 horas en total.</p></div>
    </div>
  </div>
</section>

<section id="recursos">
  <div class="wrap">
    <div class="head">
      <div><p class="label">Lo que te llevaste de la Mega Cueva</p><h2>Tus recursos, <span class="gold">día por día.</span></h2></div>
      <p class="sub">Todo es tuyo. Cada recurso trae para qué sirve, cómo se usa y un botón para copiarlo o descargarlo.</p>
    </div>

    <div class="tabs" role="tablist">
      <button class="tab" role="tab" aria-selected="true" aria-controls="p1" id="t1">Día 1 <b>Tu diagnóstico</b></button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p2" id="t2">Día 2 <b>Tu mesa</b></button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p3" id="t3">Día 3 <b>El método</b></button>
    </div>

    <!-- DÍA 1 -->
    <div class="panel" id="p1" role="tabpanel" aria-labelledby="t1">
      <div class="day-intro"><div class="big">01</div><div><p class="label">Día 1 · Por qué sistemas</p><h3>Tu experiencia de trading, convertida en sistema.</h3><p>El primer paso para salir del «nivel plastilina»: dejar de chatear al azar con la IA y darle un manual que siga siempre igual.</p></div></div>
      <div class="res">
        <div class="res-top">
          <div><span class="kind">Prompt · skill /diagnostico</span><h3>El prompt del diagnóstico</h3></div>
          <div class="acts"><button class="btn sm" data-copy="txt-prompt">Copiar prompt</button><button class="btn sm ghost" data-copy="txt-skill">Copiar como SKILL.md</button></div>
        </div>
        <div class="cols2">
          <div class="box"><p class="label">Para qué te sirve</p>
            <p style="color:var(--cream2);font-size:15px;margin-bottom:12px">Te entrevista como lo haría un profesional y convierte lo que ya sabes (o lo que no sabes todavía) en un camino sistemático. Te devuelve:</p>
            <div class="chips"><span class="chip">Diagnóstico profesional</span><span class="chip">Tus hipótesis comprobables</span><span class="chip">Tus 3 primeras skills</span><span class="chip">Tu primer agente investigador</span><span class="chip">Plan de 7 días</span></div>
          </div>
          <div class="box"><p class="label">Cómo usarlo</p>
            <ol>
              <li>Abre Claude, ChatGPT o Gemini. Mejor si creas un <b>Proyecto</b> (por ejemplo, «Mi trading»).</li>
              <li>Súbele lo que tengas: tu historial de operaciones, PDFs, libros o notas. Si no tienes nada, no pasa nada.</li>
              <li>Pulsa <b>Copiar prompt</b>, pégalo y envíalo.</li>
              <li>Responde sus preguntas (máximo 10, de una en una) con honestidad y en corto.</li>
              <li>Guarda el resultado: tus hipótesis son tu punto de partida para el Reto.</li>
            </ol>
          </div>
        </div>
        {code('txt-prompt', 'diagnostico · prompt', PROMPT)}
        <p class="note"><b>¿Usas Claude Code?</b> Pulsa «Copiar como SKILL.md», guárdalo en <code>.claude/skills/diagnostico/SKILL.md</code> dentro de tu carpeta y escribe <code>/diagnostico</code>. Así la IA lo sigue siempre igual.</p>
      </div>
    </div>

    <!-- DÍA 2 -->
    <div class="panel" id="p2" role="tabpanel" aria-labelledby="t2" hidden>
      <div class="day-intro"><div class="big">02</div><div><p class="label">Día 2 · Monta tu mesa</p><h3>Tu cueva con un Director, 4 agentes y 3 skills.</h3><p>Una carpeta que recuerda: le das tu idea y la pasa por las fases del método TIS, fase a fase, sin inventar cifras.</p></div></div>

      <div class="res">
        <div class="res-top">
          <div><span class="kind">Descarga · zip</span><h3>Tu Cueva TIS</h3></div>
          <div class="acts"><a class="btn sm" href="{ZIP}" download>⬇ Descargar mi cueva</a><a class="btn sm ghost" href="{CUEVA}" target="_blank" rel="noopener">Guía completa ↗</a></div>
        </div>
        <div class="cols2">
          <div class="box"><p class="label">Para qué te sirve</p><ul>
            <li>Un <b>Director</b> que conoce el método TIS y te dice en qué fase está tu idea.</li>
            <li>Agentes que se reparten las fases: hipótesis, reglas y validador.</li>
            <li>3 skills: escritor de hipótesis, AED y validador 4/4.</li>
            <li>Cada idea termina en una <b>ficha</b> guardada en <code>fichas/</code>.</li></ul></div>
          <div class="box"><p class="label">Cómo usarla · 4 pasos</p><ol>
            <li>Descomprime el zip y haz doble clic en <b>EMPEZAR</b>. Abre VS Code con tu cueva (si no lo tienes, te lleva a descargarlo gratis).</li>
            <li>Activa tu IA: Copilot gratis con tu cuenta de GitHub, en modo <b>Agent</b>.</li>
            <li>Primer mensaje: <code>Lee AGENTS.md y actúa como el Director</code>. Luego pega tu idea.</li>
            <li>Abre <code>fichas/</code> y revisa tu ficha.</li></ol></div>
        </div>
        {code('txt-idea', 'tu orden para el Director', IDEA, False)}
      </div>

      <div class="res">
        <div class="res-top">
          <div><span class="kind">Sin instalar nada</span><h3>¿Prefieres tu chat? Director + skills</h3></div>
          <div class="acts"><button class="btn sm" data-copy="txt-director">1 · Copiar Director</button><button class="btn sm" data-copy="txt-skills">2 · Copiar skills</button></div>
        </div>
        <div class="box"><p class="label">Cómo usarlo</p><ol>
          <li>Abre un chat nuevo en Claude, ChatGPT o DeepSeek, pega el <b>Director</b> y envíalo. Responderá «Recibido».</li>
          <li>En el mismo chat, pega las <b>skills</b> y envíalas. Responderá «Listo, Director preparado».</li>
          <li>Pega tu orden con tu idea (arriba). Como el chat no guarda archivos, la ficha te llega en el chat: guárdala tú.</li></ol></div>
        {code('txt-director', 'AGENTS.md · el Director', DIRECTOR)}
      </div>

      <div class="res">
        <div class="res-top">
          <div><span class="kind">Herramienta web</span><h3>Megacueva Tester</h3></div>
          <div class="acts"><a class="btn sm" href="{TESTER}" target="_blank" rel="noopener">Abrir el tester ↗</a></div>
        </div>
        <div class="cols2">
          <div class="box"><p class="label">Para qué te sirve</p><p style="color:var(--cream2);font-size:15px">Pasa tu idea de una frase a pseudocódigo y a un backtest con costes, en tu navegador. Y te dice la verdad: su veredicto X/4 te dice «no» antes que tu cuenta.</p></div>
          <div class="box"><p class="label">Cómo usarlo · 3 pasos</p><ol>
            <li>Escribe tu idea como se la contarías a otra persona.</li>
            <li>Elige los datos.</li>
            <li>Corre la prueba y lee el veredicto con las 4 preguntas.</li></ol></div>
        </div>
      </div>
    </div>

    <!-- DÍA 3 -->
    <div class="panel" id="p3" role="tabpanel" aria-labelledby="t3" hidden>
      <div class="day-intro"><div class="big">03</div><div><p class="label">Día 3 · Los siguientes pasos</p><h3>El método decide. La IA es la obrera.</h3><p>Por qué funciona todo lo anterior: hay números que no se negocian y la cueva recuerda, no se olvida como un chat.</p></div></div>
      <div class="res">
        <div class="res-top">
          <div><span class="kind">Tu método · METODO.md</span><h3>La línea de producción de estrategias</h3></div>
          <div class="acts"><button class="btn sm" data-copy="txt-metodo">Copiar METODO.md</button></div>
        </div>
        <div class="phases">
          <div class="ph"><i>01 · CRITERIO</i>Hipótesis</div><div class="ph"><i>02 · CRITERIO + DATOS</i>AED</div>
          <div class="ph"><i>03 · MOTOR</i>Reglas</div><div class="ph"><i>04 · MOTOR</i>Backtest</div>
          <div class="ph"><i>05 · MOTOR</i>Optimización</div><div class="ph"><i>06 · MOTOR</i>Robustez</div>
          <div class="ph"><i>07 · CRITERIO</i>Tamaño y riesgo</div><div class="ph"><i>08 · DOCUMENTACIÓN</i>Puesta en marcha</div>
        </div>
        <p class="label" style="margin:24px 0 10px">Los 4 números · fuera de muestra y con costes</p>
        <div class="rules4">
          <div class="r4"><b>≥ 1,3</b><span>Factor de beneficio</span></div>
          <div class="r4"><b>≥ 30</b><span>Operaciones</span></div>
          <div class="r4"><b>&lt; 20 %</b><span>Caída máxima</span></div>
          <div class="r4"><b>&gt; 1</b><span>Factor de beneficio sin la mejor operación</span></div>
        </div>
        <div class="cols2" style="margin-top:20px">
          <div class="box"><p class="label">Para qué te sirve</p><p style="color:var(--cream2);font-size:15px">Es el filtro con el que vamos a trabajar en el Reto. Si lo tienes claro antes del domingo, entiendes cada misión desde el primer minuto.</p></div>
          <div class="box"><p class="label">Cómo usarlo</p><ol><li>Cópialo y pégalo en <code>metodo/METODO.md</code> de tu cueva, o en un Proyecto de tu IA.</li><li>Antes de dar por buena cualquier idea, pregúntate: ¿pasa los 4 números?</li></ol></div>
        </div>
        {code('txt-metodo', 'metodo/METODO.md', METODO)}
      </div>
    </div>
  </div>
</section>

<section id="semana">
  <div class="wrap">
    <div class="head">
      <div><p class="label">Del 25 al 29 de octubre</p><h2>Tu semana <span class="gold">en la Cueva.</span></h2></div>
      <p class="sub">Unas 2 horas al día. Un entregable cada día, que subes al buzón de la misión en la plataforma.</p>
    </div>
    <div class="cal">
      <div class="cd live"><div class="n">1</div><span class="d">Dom 25 · directo</span><h3>Método TIS y tus herramientas</h3><p class="f">Instalamos el entorno juntos.</p><p class="e">Tu entorno y tu repositorio listos</p></div>
      <div class="cd"><div class="n">2</div><span class="d">Lun 26 · vídeo + ejercicios</span><h3>Pensar en datos</h3><p class="f">Del dato a una idea que se pueda probar.</p><p class="e">Tu primera hipótesis</p></div>
      <div class="cd"><div class="n">3</div><span class="d">Mar 27 · vídeo + office hours</span><h3>Claude, código y backtest</h3><p class="f">Tu hipótesis pasa a código y a su primera prueba.</p><p class="e">Tu primera curva de equity</p></div>
      <div class="cd live"><div class="n">4</div><span class="d">Mié 28 · directo</span><h3>Tu primer sistema automatizado</h3><p class="f">Tu robot, en tu servidor.</p><p class="e">Tu estrategia automatizada e instalada</p></div>
      <div class="cd live"><div class="n">5</div><span class="d">Jue 29 · directo</span><h3>La visión de portafolio</h3><p class="f">Dos estrategias trabajando juntas.</p><p class="e">2 estrategias en un mini portafolio</p></div>
    </div>
  </div>
</section>

<section id="dia0" class="guide">
  <div class="wrap">
    <div class="head">
      <div><p class="label">Guía de preparación · 5 páginas</p><h2>Tu <span class="gold">Día 0.</span></h2></div>
      <div><p class="sub" style="margin-bottom:16px">En la Mega Cueva te dijimos que el diagnóstico era la pieza 1 de tu Día 0. Aquí está el resto: lo que haces antes del domingo para llegar listo.</p>
      <div class="guide-actions"><a class="btn sm" href="{PDF}" download>⬇ Descargar en PDF</a></div></div>
    </div>
    <div class="pages">
{GUIDE}
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <img src="img/logo-tiss.png" alt="Trade It Simple" width="104" height="26">
    <p>Página de recursos para alumnos del Reto Cueva de Trading. Contenido educativo: no constituye asesoría financiera. El trading conlleva riesgo de pérdida de capital y los resultados pasados no garantizan resultados futuros. Ni la Cueva ni las IA operan por ti ni dan señales.</p>
  </div>
</footer>
<div class="toast" id="toast">¡Copiado!</div>

{data('txt-prompt', PROMPT)}
{data('txt-skill', SKILL_DIAG)}
{data('txt-idea', IDEA)}
{data('txt-director', DIRECTOR)}
{data('txt-skills', SKILLS)}
{data('txt-metodo', METODO)}
<script>
(function(){{
  // countdown · el Reto arranca el domingo 25/10 (00:00 Madrid, igual que la landing del Reto)
  var T=new Date('2026-10-25T00:00:00+02:00').getTime();
  var ids=['d','h','m','s'].map(function(k){{return document.getElementById('cd-'+k)}});
  function pad(n){{return n<10?'0'+n:''+n}}
  function tick(){{
    var r=Math.max(0,T-Date.now()),s=Math.floor(r/1000);
    var v=[Math.floor(s/86400),Math.floor(s%86400/3600),Math.floor(s%3600/60),s%60];
    ids.forEach(function(el,i){{el.textContent=pad(v[i])}});
    if(r===0){{document.getElementById('cd-when').textContent='¡El Reto ya empezó! Entra a la plataforma y a la comunidad.';return}}
    setTimeout(tick,1000-(Date.now()%1000));
  }}
  tick();

  // tabs
  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  function sel(t,focus){{tabs.forEach(function(x){{var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on}});if(focus)t.focus();try{{history.replaceState(null,'','#'+t.id.replace('t','dia'))}}catch(e){{}}}}
  tabs.forEach(function(t,i){{
    t.addEventListener('click',function(){{sel(t)}});
    t.addEventListener('keydown',function(e){{if(e.key==='ArrowRight')sel(tabs[(i+1)%tabs.length],1);if(e.key==='ArrowLeft')sel(tabs[(i+tabs.length-1)%tabs.length],1)}});
  }});
  var m=location.hash.match(/^#dia([123])$/);if(m){{sel(tabs[m[1]-1]);document.getElementById('recursos').scrollIntoView()}}

  // copiar
  var toast=document.getElementById('toast'),tt;
  function show(msg){{toast.textContent=msg;toast.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){{toast.classList.remove('on')}},1800)}}
  function fallback(txt){{var ta=document.createElement('textarea');ta.value=txt;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var ok=false;try{{ok=document.execCommand('copy')}}catch(e){{}}document.body.removeChild(ta);return ok}}
  document.addEventListener('click',function(e){{
    var b=e.target.closest('[data-copy]');
    if(b){{
      var txt=JSON.parse(document.getElementById(b.getAttribute('data-copy')).textContent);
      var done=function(){{show('¡Copiado! Ahora pégalo en tu IA');if(b.classList.contains('copy')){{var o=b.textContent;b.textContent='✓ Copiado';b.classList.add('done');setTimeout(function(){{b.textContent=o;b.classList.remove('done')}},1600)}}}};
      if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(txt).then(done,function(){{fallback(txt)?done():show('No se pudo copiar: selecciónalo a mano')}})}}
      else{{fallback(txt)?done():show('No se pudo copiar: selecciónalo a mano')}}
      return;
    }}
    var mo=e.target.closest('[data-more]');
    if(mo){{var c=mo.previousElementSibling;var open=c.classList.toggle('open');mo.textContent=open?'Ver menos ↑':'Ver completo ↓'}}
  }});

  // checklist de la guía: se recuerda en este navegador
  [].forEach.call(document.querySelectorAll('.check input[data-k]'),function(c){{
    try{{c.checked=localStorage.getItem('dia0:'+c.dataset.k)==='1'}}catch(e){{}}
    c.addEventListener('change',function(){{try{{localStorage.setItem('dia0:'+c.dataset.k,c.checked?'1':'0')}}catch(e){{}}}});
  }});
}})();
</script>
</body>
</html>'''

GUIA = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Tu Día 0 · Reto Cueva de Trading</title>
{FONTS}<style>{CSS}{PRINT_CSS}</style></head>
<body><div class="pages">{GUIDE}</div></body></html>'''

open('index.html', 'w', encoding='utf-8').write(INDEX)
open('guia-dia-0.html', 'w', encoding='utf-8').write(GUIA)
print('ok', len(INDEX), len(GUIA))
