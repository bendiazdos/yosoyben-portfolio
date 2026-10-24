// One resting position; complete card objects travel through the viewport between selections.
(()=>{
 const stage=document.querySelector('.project-stage');if(!stage)return;
 const projects=JSON.parse(document.querySelector('#project-records').textContent);
 const mediaPreference=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width:760px)');
 const previewMotion=document.body.classList.contains('motion-preview');
 const reduced={get matches(){return mediaPreference.matches&&!previewMotion}};
 const card=stage.querySelector('.featured-project'),copy=stage.querySelector('.project-copy');
 const images=[...stage.querySelectorAll('.project-image')],buttons=[...stage.querySelectorAll('[data-select]')];
 const previous=stage.querySelector('[aria-label="Previous project"]'),next=stage.querySelector('[aria-label="Next project"]');
 const gesture=new ProjectGesture(),cache=new Map();
 const ease='cubic-bezier(.22,1,.36,1)',duration=660;
 const wrap=index=>Math.max(0,Math.min(projects.length-1,index));
 const storage={get(){try{return sessionStorage.getItem('portfolio-project')}catch{return null}},set(slug){try{sessionStorage.setItem('portfolio-project',slug)}catch{}}};
 let active=Math.max(0,projects.findIndex(p=>p.slug===storage.get())),front=0;
 let pending=null,inFlight=null,running=false,opening=false,epoch=0,controller,pointer=null,swiped=false;
 let motion=[],idle=[],hoverFrame=0,departing=null;
 function loadImage(index){
  const src='/assets/'+projects[wrap(index)].image;
  if(!cache.has(src)){const image=new Image();image.src=src;cache.set(src,image.decode().catch(()=>{}));}
  return cache.get(src);
 }
 function preload(){loadImage(active-1);loadImage(active+1)}
 function animate(element,frames,options={}){
  if(reduced.matches)return Promise.resolve();
  const animation=element.animate(frames,{duration:360,easing:ease,fill:'none',...options});
  motion.push(animation);return animation.finished.catch(()=>{});
 }
 function text(p){
  const title=stage.querySelector('[data-title]');
  const lines={'lockheed-martin':['Lockheed','Martin'],'leidos-cld':['Leidos','CLD']}[p.slug];
  title.replaceChildren(...(lines?lines.flatMap((line,i)=>i?[document.createElement('br'),document.createTextNode(line)]:[document.createTextNode(line)]):[document.createTextNode(p.client)]));
  stage.querySelector('[data-category]').textContent=p.short;
  stage.querySelector('[data-description]').textContent=p.description;
  for(const key of ['role','responsibilities','client','format'])stage.querySelector('[data-'+key+']').textContent=p[key];
  stage.querySelector('[data-card-title]').textContent=p.client;
  stage.querySelector('[data-card-category]').textContent=p.kind;
 }
 function navigation(){
  const p=projects[active],number=String(active+1).padStart(2,'0');
  stage.querySelector('[data-current]').textContent=number;
  stage.querySelector('[data-card-number]').textContent=number+' / 06';
  stage.querySelector('.number-track').style.setProperty('--selected',active);
  buttons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===active)));
  previous.disabled=active===0;next.disabled=active===projects.length-1;
  stage.querySelectorAll('[data-project-link]').forEach(link=>link.href='/work/'+p.slug+'/'+(previewMotion?'?motion=preview':''));
  card.setAttribute('aria-label','View '+p.client+' case study');storage.set(p.slug);
 }
 function resetVisuals(){
  motion.forEach(animation=>animation.cancel());motion=[];departing?.remove();departing=null;
  const p=projects[active];images[front].src='/assets/'+p.image;
  images.forEach((image,i)=>{
   image.classList.toggle('is-front',i===front);image.style.zIndex=i===front?'2':'1';
   image.alt=i===front?p.alt:'';if(i===front)image.removeAttribute('aria-hidden');else image.setAttribute('aria-hidden','true');
  });
  text(p);navigation();preload();
 }
 function settle(){running=false;inFlight=null;stage.removeAttribute('data-transitioning');idle.splice(0).forEach(resolve=>resolve());}
 async function transition(target,direction){
  running=true;inFlight=target;const token=epoch;
  await loadImage(target);if(token!==epoch)return;
  const incoming=1-front,p=projects[target];
  images[incoming].src='/assets/'+p.image;await images[incoming].decode().catch(()=>{});
  if(token!==epoch)return;
  // Capture the hovered object before switching to the resting slide geometry.
  const outgoingTransform=getComputedStyle(card).transform;
  const outgoingScale=getComputedStyle(card).scale;
  const outgoingStroke=getComputedStyle(stage.querySelector('.card-stroke')).transform;
  const outgoingCTA=getComputedStyle(stage.querySelector('.card-cta')).opacity;
  stage.dataset.transitioning='true';
  const r=card.getBoundingClientRect();
  // A temporary inert snapshot carries the complete outgoing object, including its shadow and copy.
  if(!reduced.matches){
   departing=card.cloneNode(true);departing.removeAttribute('href');departing.removeAttribute('data-project-link');
   departing.classList.add('departing-card');departing.setAttribute('aria-hidden','true');departing.inert=true;
   Object.assign(departing.style,{position:'fixed',left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',margin:'0',transform:'none',scale:outgoingScale,pointerEvents:'none'});
   departing.querySelector('.card-stroke').style.transform=outgoingStroke;
   Object.assign(departing.querySelector('.card-cta').style,{opacity:outgoingCTA,visibility:'visible'});
   document.body.append(departing);
  }
  active=target;front=incoming;navigation();preload();
  images.forEach((image,i)=>{
   image.classList.toggle('is-front',i===front);image.style.zIndex=i===front?'2':'1';
   image.alt=i===front?p.alt:'';if(i===front)image.removeAttribute('aria-hidden');else image.setAttribute('aria-hidden','true');
  });
  stage.querySelector('[data-card-title]').textContent=p.client;
  stage.querySelector('[data-card-category]').textContent=p.kind;
  const exit=direction>0?-(r.bottom+90):innerHeight-r.top+90;
  const entry=direction>0?innerHeight-r.top+90:-(r.bottom+90);
  const rest='translate3d(0,0,0) rotateX(.25deg) rotateY(-.3deg)';
  const objectMotion=Promise.all([
   departing?animate(departing,[{transform:outgoingTransform},{transform:`translate3d(0,${exit}px,0) ${outgoingTransform==='none'?'':outgoingTransform} rotateZ(${-direction*.7}deg)`}],{duration:590,easing:'cubic-bezier(.45,0,.65,1)',fill:'both'}):Promise.resolve(),
   animate(card,[{transform:`translate3d(0,${entry}px,0) rotateX(${direction*1.4}deg) rotateY(-.8deg)`},{transform:rest}],{duration,delay:35,fill:'both'}),
   animate(images[front],[{transform:'scale(1.022)'},{transform:'scale(1.012)'}],{duration:530,delay:100})
  ]);
  const textMotion=(async()=>{
   await animate(copy,[{opacity:1},{opacity:0}],{duration:130,easing:'cubic-bezier(.4,0,1,1)'});
   if(token!==epoch)return;text(p);
   await animate(copy,[{opacity:0},{opacity:1}],{duration:390,delay:25});
  })();
  const details=Promise.all([
   animate(stage.querySelector('[data-card-number]'),[{opacity:.2,transform:`translateY(${direction*7}px)`},{opacity:1,transform:'translateY(0)'}],{duration:300,delay:150}),
   animate(stage.querySelector('.card-stroke'),[{transform:'scaleX(.55)'},{transform:'scaleX(1)'}],{duration:420,delay:190})
  ]);
  await Promise.all([objectMotion,textMotion,details]);if(token!==epoch)return;
  resetVisuals();settle();drain();
 }
 function drain(){
  if(running||opening||pending===null)return;
  const request=pending;pending=null;if(request.index!==active)transition(request.index,request.direction);
 }
 function select(index,direction){
  if(opening)return;
  const target=wrap(index);pending={index:target,direction:direction??(target>=active?1:-1)};drain();
 }
 function step(direction){select((pending?.index??inFlight??active)+direction,direction)}
 function mount(){
  controller?.abort();controller=new AbortController();const signal=controller.signal;
  const header=document.querySelector('.site-header');
  const showcaseTop=()=>Math.max(0,Math.min(stage.getBoundingClientRect().top+window.scrollY-header.offsetHeight,document.documentElement.scrollHeight-innerHeight));
  const updateArrival=()=>{
   const landing=showcaseTop();
   stage.classList.toggle('is-arrived',window.scrollY>=landing-2);
   document.body.style.setProperty('--intro-progress',String(Math.min(1,Math.max(0,window.scrollY/Math.max(1,landing)))));
  };
  addEventListener('scroll',updateArrival,{passive:true,signal});
  addEventListener('resize',updateArrival,{passive:true,signal});
  updateArrival();
  document.querySelector('.intro-work').addEventListener('click',event=>{event.preventDefault();gesture.reset();window.scrollTo({top:showcaseTop(),behavior:reduced.matches?'instant':'smooth'})},{signal});
  stage.querySelector('.showcase-top').addEventListener('click',()=>{
   epoch++;pending=null;active=0;resetVisuals();settle();gesture.reset();
   window.scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'});
   document.querySelector('#intro-title').focus({preventScroll:true});
  },{signal});
  buttons.forEach((button,i)=>button.addEventListener('click',()=>select(i),{signal}));
  previous.addEventListener('click',()=>step(-1),{signal});next.addEventListener('click',()=>step(1),{signal});
  stage.addEventListener('keydown',event=>{
   if(!event.target.closest('.project-navigator,.project-arrows'))return;
   if(!['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
   event.preventDefault();const direction=['ArrowUp','ArrowLeft'].includes(event.key)?-1:1;
   const i=event.key==='Home'?0:event.key==='End'?projects.length-1:(pending?.index??inFlight??active)+direction;
   select(i,['Home','End'].includes(event.key)?undefined:direction);buttons[wrap(i)].focus({preventScroll:true});
  },{signal});
  addEventListener('wheel',event=>{
   if(mobile.matches||event.ctrlKey||opening||document.body.classList.contains('is-opening'))return;
   if(window.scrollY<showcaseTop()-2){
    gesture.push(event.deltaY,event.deltaMode,performance.now(),innerHeight);return;
   }
   if(event.target.closest('input,select,textarea,[contenteditable=true]'))return;
   // At the first project, upward wheel input belongs to the document again.
   if(event.deltaY<0&&active===0&&!running&&pending===null){gesture.reset();return;}
   event.preventDefault();
   if(Math.abs(event.deltaX)>Math.abs(event.deltaY))return;
   const direction=gesture.push(event.deltaY,event.deltaMode,performance.now(),innerHeight);
   if(direction)step(direction);
  },{passive:false,signal});
  card.addEventListener('dragstart',event=>event.preventDefault(),{signal});
  card.addEventListener('pointerdown',event=>{if(event.button!==0)return;pointer={x:event.clientX,y:event.clientY,id:event.pointerId};card.setPointerCapture(event.pointerId);swiped=false},{signal});
  card.addEventListener('pointerup',event=>{
   if(!pointer||pointer.id!==event.pointerId)return;
   const dx=event.clientX-pointer.x,dy=event.clientY-pointer.y;pointer=null;
   if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.25){swiped=true;step(dx<0?1:-1);}
  },{signal});
  card.addEventListener('pointercancel',()=>{pointer=null},{signal});
  card.addEventListener('click',event=>{if(swiped){event.preventDefault();event.stopImmediatePropagation();swiped=false;}},{signal});
  card.addEventListener('pointermove',event=>{
   if(event.pointerType==='touch'||reduced.matches||hoverFrame||opening||running)return;
   const x=event.clientX,y=event.clientY;
   hoverFrame=requestAnimationFrame(()=>{hoverFrame=0;const r=card.getBoundingClientRect();card.style.setProperty('--parallax-x',`${((x-r.left)/r.width-.5)*4}px`);card.style.setProperty('--parallax-y',`${((y-r.top)/r.height-.5)*4}px`);});
  },{signal});
  card.addEventListener('pointerleave',()=>{card.style.removeProperty('--parallax-x');card.style.removeProperty('--parallax-y')},{signal});
  document.addEventListener('portfolio:prepare-open',event=>{
   opening=true;pending=null;card.style.removeProperty('--parallax-x');card.style.removeProperty('--parallax-y');
   event.detail.ready=running?new Promise(resolve=>idle.push(resolve)):Promise.resolve();
  },{signal});
  document.addEventListener('portfolio:cancel-open',()=>{opening=false;gesture.reset()},{signal});
 }
 resetVisuals();mount();
 addEventListener('pagehide',()=>{controller?.abort();epoch++;pending=null;settle();motion.forEach(a=>a.cancel());motion=[];departing?.remove();departing=null;cancelAnimationFrame(hoverFrame);hoverFrame=0});
 addEventListener('pageshow',event=>{if(event.persisted){opening=false;active=Math.max(0,projects.findIndex(p=>p.slug===storage.get()));resetVisuals();mount();gesture.reset();}});
})();
