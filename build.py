from pathlib import Path
from html import escape
import json,re,hashlib
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
asset_css=hashlib.sha256((OUT/'style.css').read_bytes()).hexdigest()[:10]
asset_js=hashlib.sha256((OUT/'script.js').read_bytes()).hexdigest()[:10]
projects=json.loads((ROOT/'projects.json').read_text())
source=json.loads((ROOT/'content.json').read_text())
settings=json.loads((ROOT/'settings.json').read_text())
labels=['Project overview','Goals of the project','Process / experience structure','Art direction / visual system','Why it worked']
keys=['overview','goals','process','visual-system','why-it-worked']
def e(s):return escape(str(s),quote=True)
def capitalized(text):return re.sub(r'\b[a-z]',lambda m:m[0].upper(),text)
labels=[capitalized(label) for label in labels]
def icon(direction='right'):
 return f'<svg class="caret {direction}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>'
def header(active=''):
 links=''.join(f'<a href="/{url}/" '+('aria-current="page"' if active==url else '')+f'>{label}</a>' for i,(url,label) in enumerate([('work','Work'),('about','About'),('connect','Connect')]))
 return f'<a class="skip" href="#main">Skip to content</a><header class="site-header" id="top"><a class="brand" href="/" aria-label="Ben Diaz home"><img src="/assets/brand-diaz-logo.png" alt="Diaz" width="62" height="43"></a><span class="header-meta micro">DESIGNER &amp; THEN EVERYTHING ELSE</span><nav aria-label="Main navigation">{links}</nav></header>'
def footer():
 return '<footer class="site-footer micro"><span>© 2026 BEN DIAZ</span><span>MIDWEST BORN &amp; BRED</span><a href="#top">BACK TO TOP '+icon('up')+'</a></footer><dialog class="lightbox" aria-label="Enlarged project image"><button class="text-button" type="button">CLOSE ×</button><img alt=""></dialog></body></html>'
def head(title,desc,cls=''):
 return f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#eeeeec"><title>{e(title)} — Ben Diaz</title><meta name="description" content="{e(desc)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="preload" href="/assets/fonts/8d5b983ea6503b7d-s.p.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/style.css?v={asset_css}"><script defer src="/script.js?v={asset_js}"></script></head><body class="{cls}">'
def save(path,html):
 dest=OUT/path;dest.parent.mkdir(exist_ok=True,parents=True);dest.write_text(html)
def link(text,url,cls=''):
 return f'<a class="button {cls}" href="{e(url)}"><span>{text}</span>{icon()}</a>'
def cover(p,lazy=True):
 if p.get('image'):
  return f'<img src="/assets/{p["image"]}" alt="{e(p["alt"])}" width="1800" height="1013" '+('loading="lazy"' if lazy else 'fetchpriority="high"')+'>'
 typ={'lockheed-martin':('SYSTEM / 02','PRODUCT<br>VISUALIZER','orbit'),'mattermost':('PLATFORM / 03','TEAM<br>CONNECTION','network'),'leidos-cld':('DIGITAL / 04','INFORMATION<br>IN FOCUS','structure')}
 tag,title,kind=typ[p['slug']]
 return f'<div class="type-cover {kind}" role="img" aria-label="{e(p["client"])} typographic project cover"><span class="micro">{tag}</span><div class="cover-art" aria-hidden="true"><i></i><i></i><i></i><i></i></div><strong>{title}</strong><span class="micro">{e(p["client"])} / {e(p["short"])}</span></div>'
landing=head('Design, in its element','Ben Diaz. UX/UI and experience design across interfaces, immersive spaces, and motion.','landing-page')+header()+'''<main class="landing" id="main"><div class="landing-top micro"><span>PORTFOLIO / BEN DIAZ</span></div><div class="landing-stage"><h1 class="landing-name">BEN<br>DIAZ<span class="registration">[BD]</span></h1><div class="visual-stage"><canvas id="core-canvas" role="img" aria-label="An interactive rotating monochrome sculptural knot"></canvas><div class="visual-bracket tl"></div><div class="visual-bracket tr"></div><div class="visual-bracket bl"></div><div class="visual-bracket br"></div><div class="visual-tag micro">FORM STUDY / 001<br>EXPLORING CONNECTION</div><button class="motion-toggle micro" type="button" aria-pressed="false">PAUSE MOTION</button></div><div class="landing-side micro"><span>UX / UI</span><span>INTERACTION</span><span>IMMERSIVE</span><span>MOTION</span></div></div><div class="landing-bottom"><div><p>Interfaces. Experiences.<br>A different way in.</p></div><div class="landing-enter">'''+link('ENTER WORK','/work/','dark')+'''</div></div></main>'''+footer()
save(Path('index.html'),landing)
# Two-column work index; project artwork appears behind the focused link.
work=head('Selected work','Six selected projects in UX/UI, product, immersive experience, and motion design.','work-page')+header('work')+'''<main id="main" class="page-shell"><div class="page-kicker micro"><a class="home-link" href="/">'''+icon('left')+''' HOME LANDING</a></div><div class="page-heading"><h1>Selected<br>Work<span class="title-mark">[06]</span></h1></div><section class="work-grid" aria-label="Selected projects">'''
for i,p in enumerate(projects):
 work+=f'<a class="work-card" href="/work/{p["slug"]}/"><div class="work-card-cover" aria-hidden="true">{cover(p,False)}<span class="work-print-caption micro"><span>{e(p["client"])}</span><span>FILE / 0{i+1}</span></span></div><span class="work-card-number micro">0{i+1}</span><div class="work-card-copy"><h2>{e(p["client"])}</h2><span class="micro">{e(p["short"])}</span></div><span class="work-card-type micro">{e(p["kind"])}</span>{icon()}</a>'
work+='</section><div class="archive-foot micro"><a href="/about/">MEET THE DESIGNER '+icon()+'</a></div></main>'+footer()
save(Path('work/index.html'),work)
# Reuse the supplied case-study copy without inventing research, metrics, or outcomes.
def original_sections(slug):
 sections={};section='';heading=None
 for tag,text in source[slug]:
  if text.lower()=='final experience' or text.startswith('Next project /'):break
  if tag=='h2':section=text;sections[section]=[]
  elif section and tag in ['p','h3'] and not text.isdigit() and not text.startswith('Section /'):sections[section].append((tag,text))
 return sections
def find_after(items,heading):
 for i,(tag,t) in enumerate(items):
  if tag=='h3' and t==heading:return next((x for k,x in items[i+1:] if k=='p'),'')
 return ''
focused={
 'lockheed-martin':{
 'goals':['Make complex capabilities understandable.','Support guided product exploration.','Balance visual impact with technical credibility.'],
 'process':'The experience was structured around guided exploration and distinct product moments, giving live demonstrations a clear narrative.',
 'visual':'Visual clarity shaped the interface: a direct hierarchy and focused product moments keep advanced systems at the center of the story.',
 'why':'A guided structure gives audiences a way into complex capabilities. Clear visual priorities help the experience support live conversations.'},
 'mattermost':{
 'goals':['Keep powerful tools approachable.','Make information hierarchy clear.','Support everyday team collaboration.'],
 'process':'Information hierarchy and interaction clarity were the priorities, with everyday team workflows shaping how the experience was organized.',
 'visual':'The visual system was designed to feel trustworthy for technical teams, balancing product capability with an approachable interface.',
 'why':'Consistent hierarchy helps people understand what matters. Clear interactions make complex collaboration workflows easier to follow.'},
 'leidos-cld':{
 'goals':['Make a complex offering navigable.','Keep technical depth accessible.','Provide clear paths into deeper content.'],
 'process':'A modular page system organized the offering into a structured digital story, with clear entry points into more detailed content.',
 'visual':'Strong hierarchy, purposeful imagery, and a modular system connect the pages while allowing individual capabilities room to stand out.',
 'why':'A clear structure makes dense information easier to approach. Modular pages allow the broader story and detailed capability content to work together.'},
 'zales':{
 'goals':['Bring product discovery into an immersive space.','Keep the jewelry central to the experience.','Make spatial exploration approachable.'],
 'process':'The flows and interface were designed around spatial browsing, connecting immersive interaction with the product story.',
 'visual':'The design puts jewelry first. Interface hierarchy supports exploration while leaving the product room to carry the visual and emotional focus.',
 'why':'Product-focused navigation gives spatial interaction a clear purpose: helping shoppers explore the jewelry and discover its details.'},
 'leidos-animation':{
 'goals':['Give complex ideas a clear narrative.','Use pacing to support comprehension.','Connect motion with the Leidos brand story.'],
 'process':'Paced sequences and a shared visual system shaped the storytelling across screens and presentations.',
 'visual':'Art direction and visual design work alongside the sequence pacing to bring energy and clarity to the subject matter.',
 'why':'Pacing gives the viewer time to follow the story. A consistent visual system helps connect individual moments into one clear narrative.'}}
image_map={'Early Experience Sketches':'projects-husky-experience-sketches.jpg','Dual-Screen Interaction Model':'projects-husky-sketch-globe-flow.jpg','Screen Flow + Prototype Structure':'projects-husky-process-overview.jpg','UI Component System':'projects-husky-ui-components.jpg','Chapter storytelling':'projects-husky-chapter-screens.jpg','Physical-to-digital continuity':'projects-husky-tangible-interaction.jpg','What visitors could do':'projects-husky-chapter-adoption.jpg','What the system unlocked':'projects-husky-experience-in-booth.jpg'}
def figure(filename,caption):
 return f'<figure class="project-figure"><button class="image-button" type="button" data-enlarge aria-label="Enlarge {e(caption)}"><img src="/assets/{filename}" alt="{e(caption)}" loading="lazy" width="1800" height="1100"></button><figcaption class="micro"><span>VISUAL DOCUMENT /</span><span>{e(caption)}</span></figcaption></figure>'
def blocks(items,accordion=False):
 out='';groups=[];current={'title':None,'paragraphs':[]}
 for tag,t in items:
  if tag=='h3':
   if current['paragraphs']:groups.append(current)
   current={'title':t,'paragraphs':[]}
  elif tag=='p':current['paragraphs'].append(t)
 if current['paragraphs']:groups.append(current)
 accordion_number=0
 for i,g in enumerate(groups):
  inner=''.join(f'<p>{e(t)}</p>' for t in g['paragraphs'])
  if g['title'] in image_map:inner+=figure(image_map[g['title']],g['title'])
  if accordion and g['title']:
   accordion_number+=1
   out+=f'<details class="process-step"><summary><span class="micro">{accordion_number:02d}</span>{e(capitalized(g["title"]))}<span class="plus" aria-hidden="true">+</span></summary><div class="process-content">{inner}</div></details>'
  else:out+=(f'<h3>{e(capitalized(g["title"]))}</h3>' if g['title'] else '')+inner
 return out
def render_outcome_cards(cards,intro=()):
 out=''.join(f'<p>{e(text)}</p>' for text in intro)+'<div class="outcome-grid">'
 for n,card in enumerate(cards,1):
  out+='<article class="outcome-card">'+figure(card['image'],card.get('caption',card['title']))
  out+=f'<span class="outcome-number micro">{n:02d}</span><h3>{e(capitalized(card["title"]))}</h3>'
  out+=''.join(f'<p>{e(text)}</p>' for text in card['paragraphs'])
  if card.get('links'):out+='<div class="case-source-links">'+''.join(f'<a class="micro" href="{e(url)}" target="_blank" rel="noopener">{e(label)} {icon()}</a>' for label,url in card['links'])+'</div>'
  out+='</article>'
 return out+'</div>'

def outcome_cards(items):
 intro=[];cards=[];current=None
 for tag,text in items:
  if tag=='h3':
   current={'title':text,'paragraphs':[],'image':image_map[text]};cards.append(current)
  elif tag=='p':
   if current is None:intro.append(text)
   else:current['paragraphs'].append(text)
 return render_outcome_cards(cards,intro)

def detailed_chapters(slug):
 data=json.loads((ROOT/(slug+'-case-study.json')).read_text())
 def render(groups):
  out=''
  for n,g in enumerate(groups,1):
   inner=''.join(f'<p>{e(t)}</p>' for t in g['paragraphs'])
   if g.get('image'):inner+=figure(g['image'],g['caption'])
   if g.get('gallery'):
    gallery=g['gallery'];samples=gallery['samples'][:3]
    tiles=''.join(figure(sample['image'],sample['caption']) for sample in samples)
    if not tiles:tiles=f'<p class="sample-gallery-empty">{e(gallery["empty"])}</p>'
    inner+=f'<section class="sample-gallery" aria-label="{e(gallery["title"])}"><span class="micro">{e(gallery["title"])}</span><div class="sample-gallery-grid">{tiles}</div></section>'

   if g.get('links'):inner+='<div class="case-source-links">'+''.join(f'<a class="micro" href="{e(url)}" target="_blank" rel="noopener">{e(label)} {icon()}</a>' for label,url in g['links'])+'</div>'
   out+=f'<details class="process-step"><summary><span class="micro">{n:02d}</span>{e(g["title"])}<span class="plus" aria-hidden="true">+</span></summary><div class="process-content">{inner}</div></details>'
  return out
 overview='<div class="overview-split">'+''.join(f'<div><span class="micro">{label}</span><p>{e(data[key])}</p></div>' for key,label in [('challenge','THE CHALLENGE'),('solution','THE SOLUTION')])+'</div>'
 overview+=f'<div class="case-role"><span class="micro">MY ROLE / THE VIRTUAL WILD</span><p>{e(data["role"])}</p></div>'
 if data.get('overview_links'):overview+='<div class="case-source-links">'+''.join(f'<a class="micro" href="{e(url)}" target="_blank" rel="noopener">{e(label)} {icon()}</a>' for label,url in data['overview_links'])+'</div>'
 goals='<ol class="goal-list goal-grid">'+''.join(f'<li><span class="micro">{n:02d}</span>{e(t)}</li>' for n,t in enumerate(data['goals'],1))+'</ol>'
 return [overview,goals,render(data['process']),render(data['visual']),render_outcome_cards(data['why'])]

for i,p in enumerate(projects):
 from husky_editorial import render_project
 data_path=ROOT/(p['slug']+'-case-study.json')
 editorial_data=json.loads(data_path.read_text()) if data_path.exists() else None
 save(Path('work')/p['slug']/'index.html',render_project(p,projects,original_sections(p['slug']),editorial_data,focused.get(p['slug']),head,header,footer,icon))
 continue
profile='<div class="profile-frame" role="img" aria-label="Profile photograph placeholder"><div class="profile-corner micro">PROFILE / 001</div><svg viewBox="0 0 200 240" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><circle cx="100" cy="83" r="32"/><path d="M36 204v-24c0-34 26-56 64-56s64 22 64 56v24"/></svg><span class="micro">PORTRAIT TO FOLLOW</span></div>'
resume=link('DOWNLOAD RÉSUMÉ',settings['resume'],'outline') if settings['resume'] else '<button class="button outline" disabled aria-describedby="resume-note"><span>DOWNLOAD RÉSUMÉ</span>'+icon('down')+'</button><p class="micro muted" id="resume-note">RÉSUMÉ WILL BE AVAILABLE HERE SOON.</p>'
if settings['resume']:resume=resume.replace('<a ','<a download ')
about=head('About','About Ben Diaz — UX/UI, interaction, immersive experience, art direction, and motion.','about-page')+header('about')+'<main id="main" class="page-shell"><div class="page-kicker micro"><span>THE PERSON BEHIND THE WORK</span><span>PROFILE / BEN DIAZ</span></div><div class="about-layout"><aside>'+profile+'</aside><section class="about-intro"><h1>Always<br>curious.</h1><p>I’m Ben Diaz, a UX/UI designer working across interfaces, immersive experiences, websites, WebXR, and motion.</p><p>Clean structure and clear hierarchy on one side. Atmosphere and personality on the other. Both matter.</p><p>I’m interested in the connection between a clear idea and an experience that feels alive.</p><div class="resume-block">'+resume+'</div></section></div><section class="skills-section"><div><span class="micro">WHAT I BRING</span><h2>Different tools.<br>Connected thinking.</h2></div><div class="skills-list">'
for i,(a,b) in enumerate([('UX / UI design','Clear structure, hierarchy, and interface design.'),('Experience & interaction','Connected journeys across screens and physical spaces.'),('Art direction','A considered visual language from concept to execution.'),('Immersive / WebXR','Spatial experiences that put exploration first.'),('Motion & prototyping','Pacing, transitions, and ideas brought to life.')]):about+=f'<div><span class="micro">0{i+1}</span><h3>{a}</h3><p>{b}</p></div>'
about+='</div></section><div class="bottom-invite"><span class="micro">GOOD WORK STARTS WITH A CONVERSATION.</span>'+link('LET’S CONNECT','/connect/','dark')+'</div></main>'+footer();save(Path('about/index.html'),about)
email=settings['email']
connect=head('Connect','Start a conversation with Ben Diaz about design, projects, and collaborations.','connect-page')+header('connect')+'<main id="main" class="page-shell"><div class="page-kicker micro"><span>OPEN A CONVERSATION</span><span>CONNECT / 003</span></div><div class="connect-layout"><div><span class="micro">A NEW PROJECT. A SHARED IDEA. A HELLO.</span><h1>Let’s<br>connect<span class="terminal-cursor" aria-hidden="true">_</span></h1><p>Have something in mind?<br>I’d like to hear about it.</p><div class="connect-discipline micro">UX / UI<br>INTERACTION & EXPERIENCE<br>ART DIRECTION<br>IMMERSIVE / WEBXR<br>MOTION</div></div><section class="contact-panel"><div class="panel-heading micro"><span>CONTACT / BEN DIAZ</span><span>[01]</span></div>'
if email:
 connect+='<form id="contact-form" data-email="'+e(email)+'"><label>Your name<input name="name" autocomplete="name" required placeholder="Name"></label><label>Email address<input name="email" type="email" autocomplete="email" required placeholder="you@company.com"></label><label>What are you thinking?<textarea name="message" rows="5" required placeholder="Tell me a little about your project or idea."></textarea></label><button class="button dark" type="submit"><span>OPEN EMAIL DRAFT</span>'+icon()+'</button><p class="micro muted">OPENS YOUR EMAIL APP WITH YOUR MESSAGE READY TO SEND.</p><p role="status" id="contact-status"></p></form><a class="direct-email" href="mailto:'+e(email)+'">'+e(email)+'</a>'
else:
 connect+='<div class="contact-route"><span class="micro">NEW PROJECTS / COLLABORATIONS / OPPORTUNITIES</span><h2>Start here.</h2><p>Send a message through my contact form. I’d love to hear what you’re working on.</p>'+link('OPEN CONTACT FORM',settings['contact_url'],'dark')+'<p class="micro muted">OPENS THE CONTACT PAGE ON YOSOYBEN.COM.</p></div>'
connect+='</section></div></main>'+footer();save(Path('connect/index.html'),connect)
# Former anchor links continue to land on the corresponding dedicated pages.
save(Path('favicon.svg'),'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#171918"/><path d="M17 14h14c15 0 23 8 23 18S46 50 31 50H17zm9 9v18h6c8 0 12-3 12-9s-4-9-12-9z" fill="#eee"/></svg>')
print('Built landing, work, six five-chapter case studies, About, and Connect.')
