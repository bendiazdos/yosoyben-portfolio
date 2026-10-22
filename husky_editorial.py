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
  return f'<div class="ed-section-heading"><span class="ed-number">{n}</span><div><span class="micro">{kicker}</span><h2>{title}</h2></div></div>'
 page=head('Husky / One booth. A connected experience.',p['description'],'husky-editorial')
 from pathlib import Path
 root=Path(__file__).parent
 css=hashlib.sha256((root/'dist/husky-editorial.css').read_bytes()).hexdigest()[:10]
 js=hashlib.sha256((root/'dist/husky-editorial.js').read_bytes()).hexdigest()[:10]
 page=page.replace('</head>',f'<link rel="stylesheet" href="/husky-editorial.css?v={css}"><script defer src="/husky-editorial.js?v={js}"></script></head>')
 page+=header('work')+'''<main id="main"><div class="ed-preview ed-shell micro"><span>HUSKY / EDITORIAL STUDY</span><a href="https://yosoyben.com/work/husky/" target="_blank" rel="noopener">VIEW CURRENT PAGE ↗</a></div>
 <section class="ed-opening" id="experience"><div class="ed-shell"><div class="ed-kicker micro"><a href="/work/">'''+icon('left')+''' ALL WORK</a><span>HUSKY TECHNOLOGIES / DRINKTEC</span><span>01 — 06</span></div>
 <div class="ed-title-grid"><h1>One booth.<br>A connected<br><em>experience.</em></h1><div class="ed-intro"><span class="micro">DRINKTEC EXPERIENCE.</span>'''+para(p['description'])+'''<a class="ed-down micro" href="#challenge">THE THINKING BEHIND THE EXPERIENCE ↓</a></div></div></div>'''
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
 page+='<section class="ed-section ed-shell" id="interaction">'+section_title('03','DESIGNING THE INTERACTION','A shared logic.<br>Across two screens.')
 page+='<div class="ed-decision"><div class="ed-decision-copy"><span class="micro ed-label">THE KEY DECISION</span><h3>Story above.<br>Control below.</h3><p>The upper display carried cinematic visuals and data. The lower touch surface handled navigation, selection, and controls.</p>'+detail('Why this interaction model',original('Process / Experience Structure','Dual-Screen Interaction Model'))+'</div>'
 page+=media('projects-husky-sketch-globe-flow.jpg','Geographic navigation sketches from globe to zone to country','02','GLOBE → ZONE → COUNTRY / DUAL-SCREEN FLOW','ed-globe')+'</div>'
 page+='<div class="ed-supporting"><div>'+media('projects-husky-experience-sketches.jpg','Early dual-screen sketches for geographic navigation, comparison, video and factory planning','03','SELECTED EARLY EXPERIENCE SKETCHES')+'</div><div class="ed-supporting-copy"><span class="micro ed-label">EARLY EXPERIENCE SKETCHES</span><h3>Map the journey<br>before the polish.</h3><p>Kiosk flow, chapter structure, tap interactions, and motion cues were explored together.</p>'+detail('Explore the early thinking',original('Process / Experience Structure','Early Experience Sketches'))+'</div></div>'
 page+=detail('View the screen-flow and prototype documentation',original('Process / Experience Structure','Screen Flow + Prototype Structure')+media('projects-husky-process-overview.jpg','Existing process documentation showing sketches, prototype flows and UI components','04','SCREEN FLOW + PROTOTYPE STRUCTURE'),'ed-gallery')+'</section>'
 page+='<section class="ed-system" id="visual-language"><div class="ed-shell ed-section">'+section_title('04','FROM COMPONENTS TO VISUAL LANGUAGE','A system built<br>to hold the story.')
 page+='<div class="ed-system-intro"><p>Chapter menus, data cards, gauges, media controls, and round CTAs established a consistent interface language across the booth.</p><div><span class="micro">ART DIRECTION</span><p>Dark surfaces. Precise framing.<br>High-contrast yellow and cyan.</p></div></div>'
 page+=media('projects-husky-ui-components.jpg','Reusable Husky UI components including menus, data cards, gauges and media controls','05','THE REUSABLE UI COMPONENT SYSTEM','ed-components')
 page+='<div class="ed-system-notes">'+detail('How the component system supported the experience',original('Process / Experience Structure','UI Component System'))+detail('Art direction rationale',''.join(para(t) for tag,t in sections['Art Direction / Visual System'][:1] if tag=='p'))+'</div>'
 page+='<div class="ed-visual-heading"><span class="micro">THE LANGUAGE IN USE</span><h3>One visual language.<br>Different chapters.</h3></div>'
 page+=media('projects-husky-chapter-screens.jpg','Completed rPET chapter screens and their lower touchscreen controls','06','COMPLETED CHAPTER SCREENS / DISPLAY + TOUCH CONTROLS','ed-screens')
 page+=detail('Explore chapter storytelling',original('Art Direction / Visual System','Chapter storytelling'))+'</div></section>'
 page+='<section class="ed-section ed-shell" id="show-floor">'+section_title('05','BACK ON THE SHOW FLOOR','From interface<br>to interaction.')
 page+='<div class="ed-context-intro"><p>Place. Rotate. Select.</p><span class="micro">PHYSICAL-TO-DIGITAL CONTINUITY</span></div>'
 page+=media('projects-husky-tangible-interaction.jpg','Tangible product interaction sketches paired with a live booth demonstration','07','THE INTERACTION IN CONTEXT','ed-tangible')
 page+='<div class="ed-context-grid"><div class="ed-context-copy">'+original('Art Direction / Visual System','Physical-to-digital continuity')+para("A selected frame from the completed experience, bringing the project's strategy, interaction, and visual direction together.")+'</div>'
 page+=media('projects-husky-experience-in-booth.jpg','Completed tangible interaction running live at the Husky booth','08','THE COMPLETED EXPERIENCE ON THE FLOOR')+'</div></section>'
 page+='<section class="ed-outcomes ed-shell ed-section" id="outcomes">'+section_title('06','OUTCOMES & DESIGN TAKEAWAYS','A connected experience.<br>A consistent system.')
 why=sections['Why It Worked'];page+='<div class="ed-closing">'+para(next(t for tag,t in why if tag=='p'),'ed-closing-statement')+'</div>'
 page+='<div class="ed-outcome-columns"><article><span class="micro">01 / THE VISITOR EXPERIENCE</span><h3>What visitors could do</h3>'+original('Why It Worked','What visitors could do')+'</article><article><span class="micro">02 / THE SYSTEM</span><h3>What the system unlocked</h3>'+original('Why It Worked','What the system unlocked')+'</article></div>'
 page+='<div class="ed-takeaway"><span class="micro">DESIGN TAKEAWAY</span><p>A clear visitor path. A shared interaction model. A reusable UI system.</p></div></section>'
 page+='<a class="ed-next ed-shell" href="/work/lockheed-martin/"><span class="micro">NEXT PROJECT / 02</span><div><h2>Lockheed Martin</h2><span class="ed-next-arrow" aria-hidden="true">↗</span></div><span class="micro">PRODUCT VISUALIZER</span></a></main>'+footer()
 return page
