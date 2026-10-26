"""Husky editorial layout experiment; original source content stays intact."""
from html import escape as e
import hashlib

def render_husky(p,sections,head,header,footer,icon):
 def para(text,cls=''):
  return f'<p class="{cls}">{e(text)}</p>'
 def original(section,title=None):
  items=sections[section]
  if title is None:return ''.join(para(t) for tag,t in items if tag=='p')
  start=next(i for i,(tag,t) in enumerate(items) if tag=='h3' and t==title)
  result=[]
  for tag,t in items[start+1:]:
   if tag=='h3':break
   if tag=='p':result.append(para(t))
  return ''.join(result)
 def media(file,alt,number,caption,cls='',priority=False):
  return f'<figure class="ed-media {cls}"><button class="ed-image" type="button" data-enlarge aria-label="Enlarge {e(alt)}"><img src="/assets/{file}" alt="{e(alt)}" {"fetchpriority=high" if priority else "loading=lazy"} decoding="async"><span class="ed-enlarge" aria-hidden="true">{icon()}<span>EXPAND IMAGE</span></span></button><figcaption class="micro"><span>FIG. {number}</span><span>{e(caption)}</span></figcaption></figure>'
 def detail(title,body,cls=''):
  return f'<details class="ed-details {cls}"><summary><span>{e(title)}</span><span class="ed-plus" aria-hidden="true">+</span></summary><div class="ed-detail-body">{body}</div></details>'
 def section_title(n,kicker,title):
  eyebrow=f'<span class="micro">{kicker}</span>' if kicker else ''
  cls='ed-section-heading' + (' ed-heading-direct' if not kicker else '')
  return f'<div class="{cls}"><span class="ed-number">{n}</span><div>{eyebrow}<h2>{title}</h2></div></div>'
 page=head('Husky Technologies / Drinktec Experience',p['description'],'husky-editorial')
 from pathlib import Path
 root=Path(__file__).parent
 css=hashlib.sha256((root/'dist/husky-editorial.css').read_bytes()).hexdigest()[:10]
 js=hashlib.sha256((root/'dist/husky-editorial.js').read_bytes()).hexdigest()[:10]
 page=page.replace('</head>',f'<link rel="stylesheet" href="/husky-editorial.css?v={css}"><script defer src="/husky-editorial.js?v={js}"></script></head>')
 page+=header('work')+'''<main id="main"><div class="ed-preview ed-shell micro"><span>HUSKY / EDITORIAL STUDY</span><a href="https://yosoyben.com/work/husky/" target="_blank" rel="noopener">VIEW CURRENT PAGE ↗</a></div>
 <section class="ed-opening" id="experience"><div class="ed-shell"><div class="ed-kicker micro"><a href="/work/">'''+icon('left')+''' ALL WORK</a><span>01 — 06</span></div>
 <div class="ed-title-grid"><h1><span class="ed-project-company">Husky Technologies</span><em class="ed-project-name">Drinktec Experience</em></h1><div class="ed-intro">'''+para(p['description'])+'''<a class="ed-down micro" href="#challenge">THE THINKING BEHIND THE EXPERIENCE ↓</a></div></div></div>'''
 page+=media('projects-husky.jpg','Husky Drinktec booth with a phoenix spanning the curved LED canopy','01','THE FINISHED EXPERIENCE / DRINKTEC','ed-hero',True)
 page+='</section><nav class="ed-index" aria-label="Case study sections"><div class="ed-shell">'
 links=[('experience','Experience'),('challenge','Challenge'),('interaction','Interaction'),('visual-language','Visual language'),('show-floor','In context'),('outcomes','Outcomes')]
 for n,(id,label) in enumerate(links,1):page+=f'<a href="#{id}"><span class="micro">0{n}</span>{label}</a>'
 page+='</div></nav>'
 page+='<section class="ed-section ed-shell" id="challenge">'+section_title('02','THE DESIGN CHALLENGE','Complex content.<br>One clear journey.')
 page+='<div class="ed-challenge-grid"><aside class="ed-role"><span class="micro">MY ROLE</span><h3>UX / UI Design</h3><span class="micro">RESPONSIBILITIES</span><p>'+e(p['responsibilities'])+'</p><span class="micro">CLIENT</span><p>Husky Technologies</p><span class="micro">FORMAT</span><p>Digital experience</p></aside><div class="ed-challenge-copy">'
 page+='<span class="micro ed-label">THE CHALLENGE</span>'+original('Project Snapshot','The Challenge')
 page+='<div class="ed-constraints"><span class="micro">DESIGN CONSTRAINTS</span><ul><li>Tight production timeline</li><li>Dense technical information</li><li>Live hardware, kiosks &amp; larger displays</li><li>A noisy show-floor environment</li></ul></div>'
 page+=detail('The connected solution',original('Project Snapshot','The Solution'))
 goals=''.join(f'<li><span class="micro">{n:02d}</span>{e(t)}</li>' for n,(tag,t) in enumerate(sections['Goals'],1) if tag=='p')
 page+=detail('Six goals for the experience','<ol class="ed-goals">'+goals+'</ol>')
 page+=detail('Project context',original('Project'))+'</div></div></section>'
 page+='<section class="ed-section ed-shell" id="interaction">'+section_title('03','','Designing the Interaction')
 page+='<div class="ed-decision"><div class="ed-decision-copy"><h3>Story above.<br>Control below.</h3><p>The upper display carried cinematic visuals and data. The lower touch surface handled navigation, selection, and controls.</p>'+detail('Why this interaction model',original('Process / Experience Structure','Dual-Screen Interaction Model'))+'</div>'
 page+=media('projects-husky-sketch-globe-flow.jpg','Geographic navigation sketches from globe to zone to country','02','GLOBE → ZONE → COUNTRY / DUAL-SCREEN FLOW','ed-globe')+'</div>'
 page+='<div class="ed-supporting"><div>'+media('projects-husky-experience-sketches.jpg','Early dual-screen sketches for geographic navigation, comparison, video and factory planning','03','SELECTED EARLY EXPERIENCE SKETCHES')+'</div><div class="ed-supporting-copy"><h3>Early Experience Sketches</h3><p>Kiosk flow, chapter structure, tap interactions, and motion cues were explored together.</p>'+detail('Explore the early thinking',original('Process / Experience Structure','Early Experience Sketches'))+'</div></div>'
 page+=detail('View the screen-flow and prototype documentation',original('Process / Experience Structure','Screen Flow + Prototype Structure')+media('projects-husky-process-overview.jpg','Existing process documentation showing sketches, prototype flows and UI components','04','SCREEN FLOW + PROTOTYPE STRUCTURE'),'ed-gallery')+'</section>'
 page+='<section class="ed-system" id="visual-language"><div class="ed-shell ed-section">'+section_title('04','','From Components to Visual Language')
 page+='<div class="ed-system-intro"><p>Chapter menus, data cards, gauges, media controls, and round CTAs established a consistent interface language across the booth.</p><div><span class="micro">ART DIRECTION</span><p>Dark surfaces. Precise framing.<br>High-contrast yellow and cyan.</p></div></div>'
 page+=media('projects-husky-ui-components.jpg','Reusable Husky UI components including menus, data cards, gauges and media controls','05','THE REUSABLE UI COMPONENT SYSTEM','ed-components')
 page+='<div class="ed-system-notes">'+detail('How the component system supported the experience',original('Process / Experience Structure','UI Component System'))+detail('Art direction rationale',''.join(para(t) for tag,t in sections['Art Direction / Visual System'][:1] if tag=='p'))+'</div>'
 page+='<div class="ed-visual-heading"><span class="micro">THE LANGUAGE IN USE</span><h3>One visual language.<br>Different chapters.</h3></div>'
 page+=media('projects-husky-chapter-screens.jpg','Completed rPET chapter screens and their lower touchscreen controls','06','COMPLETED CHAPTER SCREENS / DISPLAY + TOUCH CONTROLS','ed-screens')
 page+=detail('Explore chapter storytelling',original('Art Direction / Visual System','Chapter storytelling'))+'</div></section>'
 page+='<section class="ed-section ed-shell" id="show-floor">'+section_title('05','','From interface<br>to interaction.')
 page+='<div class="ed-context-intro"><p>Place. Rotate. Select.</p></div>'
 page+=media('projects-husky-tangible-interaction.jpg','Tangible product interaction sketches paired with a live booth demonstration','07','THE INTERACTION IN CONTEXT','ed-tangible')
 page+='<div class="ed-context-grid"><div class="ed-context-copy">'+original('Art Direction / Visual System','Physical-to-digital continuity')+para("A selected frame from the completed experience, bringing the project's strategy, interaction, and visual direction together.")+'</div>'
 page+=media('projects-husky-experience-in-booth.jpg','Completed tangible interaction running live at the Husky booth','08','THE COMPLETED EXPERIENCE ON THE FLOOR')+'</div></section>'
 page+='<section class="ed-outcomes ed-shell ed-section" id="outcomes">'+section_title('06','','Outcomes &amp; Design Takeaways')
 why=sections['Why It Worked'];page+='<div class="ed-closing">'+para(next(t for tag,t in why if tag=='p'),'ed-closing-statement')+'</div>'
 page+='<div class="ed-outcome-columns"><article><span class="micro">01 / THE VISITOR EXPERIENCE</span><h3>What visitors could do</h3>'+original('Why It Worked','What visitors could do')+'</article><article><span class="micro">02 / THE SYSTEM</span><h3>What the system unlocked</h3>'+original('Why It Worked','What the system unlocked')+'</article></div>'
 page+='<div class="ed-takeaway"><span class="micro">DESIGN TAKEAWAY</span><p>A clear visitor path. A shared interaction model. A reusable UI system.</p></div></section>'
 page+='<a class="ed-next ed-shell" href="/work/lockheed-martin/"><span class="micro">NEXT PROJECT / 02</span><div><h2>Lockheed Martin</h2><span class="ed-next-arrow" aria-hidden="true">↗</span></div></a></main>'+footer()
 return page

def render_project(p,projects,sections,data,focus,head,header,footer,icon):
 """Shared editorial case studies, using only the project's existing material."""
 import re
 from pathlib import Path
 if p['slug']=='husky':
  page=render_husky(p,sections,head,header,footer,icon)
  page=re.sub(r'<div class="ed-preview ed-shell micro">.*?</div>','',page,count=1)
  return page
 def paras(items):return ''.join('<p>'+e(t)+'</p>' for t in items)
 def media(filename,caption,cls='',priority=False):
  return f'<figure class="ed-media {cls}"><button class="ed-image" type="button" data-enlarge aria-label="Enlarge {e(caption)}"><img src="/assets/{e(filename)}" alt="{e(caption)}" {"fetchpriority=high" if priority else "loading=lazy"} decoding="async"><span class="ed-enlarge" aria-hidden="true">{icon()}<span>EXPAND IMAGE</span></span></button><figcaption class="micro"><span>VISUAL DOCUMENT</span><span>{e(caption)}</span></figcaption></figure>'
 def links(items):
  return '<div class="ed-source-links">'+''.join(f'<a class="micro" href="{e(url)}" target="_blank" rel="noopener">{e(label)} ↗</a>' for label,url in items if 'figma.com' not in url)+'</div>' if items else ''
 def detail(title,body):return f'<details class="ed-details"><summary><span>{e(title)}</span><span class="ed-plus" aria-hidden="true">+</span></summary><div class="ed-detail-body">{body}</div></details>'
 def group(g,include_image=True):
  body=paras(g['paragraphs'])
  if include_image and g.get('image'):body+=media(g['image'],g.get('caption',g['title']))
  gal=g.get('gallery')
  if gal:
   body+='<div class="ed-samples"><span class="micro">'+e(gal['title'])+'</span>'
   body+=''.join(media(x['image'],x['caption']) for x in gal.get('samples',[])) or '<p>'+e(gal.get('empty',''))+'</p>'
   body+='</div>'
  return body+links(g.get('links',[]))
 def heading(n,kicker,title):
  return f'<div class="ed-section-heading"><span class="ed-number">{n:02d}</span><div><span class="micro">{e(kicker)}</span><h2>{e(title)}</h2></div></div>'
 def after(title):
  found=False;out=[]
  for tag,text in sections.get('Focus',[]):
   if tag=='h3':found=text==title
   elif found:out.append(text)
  return ' '.join(out)
 if data:
  challenge=data['challenge'];solution=data['solution'];goals=data['goals'];process=data['process'];visual=data['visual'];why=data['why']
 else:
  challenge=after('The Challenge');solution=after('The Approach');goals=focus['goals']
  process=[{'title':'Experience Structure','paragraphs':[focus['process']]}]
  visual=[{'title':'Design Direction','paragraphs':[focus['visual']]}]
  why=[{'title':'Product-Focused Exploration' if p['slug']=='zales' else 'Pacing And Visual Continuity','paragraphs':[focus['why']]}]
 visual_lead=next((g['image'] for g in visual if g.get('image')),None)
 context=next((g for g in reversed(visual) if g.get('image') and g['image']!=visual_lead),None)
 context=context or next((g for g in reversed(process) if g.get('image') and g['image']!=p['image']),None)
 nav=[('experience','Experience'),('challenge','Challenge'),('interaction','Interaction'),('visual-language','Visual language')]
 if context:nav.append(('show-floor','In context'))
 nav.append(('outcomes','Takeaways'))
 css=hashlib.sha256((Path(__file__).parent/'dist/husky-editorial.css').read_bytes()).hexdigest()[:10]
 js=hashlib.sha256((Path(__file__).parent/'dist/husky-editorial.js').read_bytes()).hexdigest()[:10]
 page=head(p['client']+' / '+p['short'],p['description'],'husky-editorial editorial-project')
 page=page.replace('</head>',f'<link rel="stylesheet" href="/husky-editorial.css?v={css}"><script defer src="/husky-editorial.js?v={js}"></script></head>')+header('work')
 headline='<span class="ed-project-company">'+e(p['client'])+'</span><em class="ed-project-name">'+e(p['short'])+'</em>'
 page+='<main id="main"><section class="ed-opening" id="experience"><div class="ed-shell"><div class="ed-kicker micro"><a href="/work/">'+icon('left')+' ALL WORK</a><span>'+f'{projects.index(p)+1:02d} — 06'+'</span></div>'
 page+='<div class="ed-title-grid"><h1>'+headline+'</h1><div class="ed-intro"><span class="micro">'+e(p['short'])+'</span>'+paras([p['description']])+'<a class="ed-down micro" href="#challenge">THE THINKING BEHIND THE EXPERIENCE ↓</a></div></div></div>'+media(p['image'],p['alt'],'ed-hero',True)+'</section>'
 page+='<nav class="ed-index" aria-label="Case study sections"><div class="ed-shell" style="--ed-count:'+str(len(nav))+'">'+''.join(f'<a href="#{id}"><span class="micro">{n:02d}</span>{e(label)}</a>' for n,(id,label) in enumerate(nav,1))+'</div></nav>'
 page+='<section class="ed-section ed-shell" id="challenge">'+heading(2,'THE DESIGN CHALLENGE','The brief. The responsibility.')
 page+='<div class="ed-challenge-grid"><aside class="ed-role"><span class="micro">MY ROLE</span><h3>'+e(p['role'])+'</h3><span class="micro">RESPONSIBILITIES</span>'+paras([p['responsibilities']])+'<span class="micro">CLIENT</span>'+paras([p['client']])+'</aside><div class="ed-challenge-copy"><span class="micro ed-label">THE CHALLENGE</span>'+paras([challenge])
 page+=detail('The approach',paras([solution]))+detail('Design goals','<ol class="ed-goals">'+''.join(f'<li><span class="micro">{n:02d}</span>{e(t)}</li>' for n,t in enumerate(goals,1))+'</ol>')
 if data:page+=detail('My contribution',paras([data['role']]))+links(data.get('overview_links',[]))
 else:page+=detail('Project context',paras([t for tag,t in sections.get('Project',[]) if tag=='p']))
 page+='</div></div></section>'
 page+='<section class="ed-section ed-shell" id="interaction">'+heading(3,'EXPERIENCE STRUCTURE',{'lockheed-martin':'Two surfaces. One experience.','mattermost':'From scenario to action.','leidos-cld':'A story shaped by scrolling.','zales':'Discovery through interaction.','leidos-animation':'A story shaped by pacing.'}[p['slug']])
 selected=next((g for g in process if g.get('image')),None)
 if selected:
  page+='<div class="ed-decision"><div class="ed-decision-copy"><span class="micro ed-label">'+e(selected['title'])+'</span>'+paras(selected['paragraphs'])+links(selected.get('links',[]))+'</div>'+media(selected['image'],selected['caption'])+'</div>'
 for g in process:
  if g is selected:continue
  page+=detail(g['title'],group(g))
 page+='</section>'
 page+='<section class="ed-system" id="visual-language"><div class="ed-shell ed-section">'+heading(4,'ART DIRECTION / VISUAL SYSTEM','The visual language.')
 primary=next((g for g in visual if g.get('image')),None)
 if primary:
  page+='<div class="ed-system-intro"><div>'+paras(primary['paragraphs'])+'</div><span class="micro">'+e(primary['title'])+'</span></div>'+media(primary['image'],primary['caption'],'ed-screens')
 else:
  page+='<div class="ed-system-intro">'+paras(visual[0]['paragraphs'])+'</div>'
 for g in visual:
  if g is primary or (not primary and g is visual[0]):continue
  page+=detail(g['title'],group(g,g is not context))
 page+='</div></section>'
 if context:
  page+='<section class="ed-section ed-shell" id="show-floor">'+heading(5,'THE COMPLETED EXPERIENCE','Design in context.')+media(context['image'],context.get('caption',context['title']),'ed-tangible')+'</section>'
 page+='<section class="ed-outcomes ed-shell ed-section" id="outcomes">'+heading(6 if context else 5,'DESIGN RATIONALE / TAKEAWAYS','Why the approach works.')+'<div class="ed-outcome-columns">'
 for n,g in enumerate(why,1):page+='<article><span class="micro">'+f'{n:02d} / DESIGN TAKEAWAY'+'</span><h3>'+e(g['title'])+'</h3>'+paras(g['paragraphs'])+links(g.get('links',[]))+'</article>'
 page+='</div></section>'
 nxt=projects[(projects.index(p)+1)%len(projects)]
 page+='<a class="ed-next ed-shell" href="/work/'+nxt['slug']+'/"><span class="micro">NEXT PROJECT</span><div><h2>'+e(nxt['client'])+'</h2><span class="ed-next-arrow" aria-hidden="true">↗</span></div><span class="micro">'+e(nxt['short'])+'</span></a></main>'+footer()
 return page
