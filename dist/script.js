const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
// Preserve links shared before the dedicated pages were introduced.
if(location.pathname==='/'&&['#work','#about','#contact','#connect'].includes(location.hash)){
 const path={'#work':'/work/','#about':'/about/','#contact':'/connect/','#connect':'/connect/'}[location.hash];location.replace(path);
}
// Case studies are five chapters rather than a single long page.
const chapterTabs=[...document.querySelectorAll('[data-chapter]')];
if(chapterTabs.length){
 const panels=[...document.querySelectorAll('.chapter-panel')];
 const chapterSystem=document.querySelector('.chapter-system');
 const chapterRail=document.querySelector('.chapter-rail');
 const chapterContent=document.querySelector('.chapter-content');
 let fadeFrame=0;
 function updateChapterFade(){
  fadeFrame=0;
  const rail=chapterRail.getBoundingClientRect();
  const start=rail.bottom-chapterContent.getBoundingClientRect().top;
  chapterSystem.classList.toggle('chapters-pinned',rail.top<=1);
  chapterContent.style.setProperty('--chapter-fade-start',`${start}px`);
  chapterContent.style.setProperty('--chapter-fade-end',`${start+120}px`);
 }
 function scheduleChapterFade(){if(!fadeFrame)fadeFrame=requestAnimationFrame(updateChapterFade)}
 addEventListener('scroll',scheduleChapterFade,{passive:true});
 addEventListener('resize',scheduleChapterFade);
 new ResizeObserver(scheduleChapterFade).observe(chapterSystem);
 let active=0;
 const keys=['overview','goals','process','visual-system','why-it-worked'];
 document.querySelector('[role=tablist]').setAttribute('aria-orientation','horizontal');
 function selectChapter(index,{focus=false,scroll=false,hash=true}={}){
  const rail=document.querySelector('.chapter-rail');
  const wasPinned=rail.getBoundingClientRect().top<=0;
  active=Math.max(0,Math.min(4,index));
  chapterTabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===active));tab.tabIndex=i===active?0:-1});
  panels.forEach((panel,i)=>panel.hidden=i!==active);
  if(hash)history.replaceState(null,'','#'+keys[active]);
  if(wasPinned){const system=document.querySelector('.chapter-system');window.scrollTo({top:window.scrollY+system.getBoundingClientRect().top+parseFloat(getComputedStyle(system).paddingTop),behavior:'instant'})}
  if(focus)chapterTabs[active].focus();
  updateChapterFade();
  if(scroll)document.querySelector('.chapter-system').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth',block:'start'});
 }
 chapterTabs.forEach((tab,i)=>{
  tab.addEventListener('click',()=>selectChapter(i));
  tab.addEventListener('keydown',event=>{let index=i;if(['ArrowDown','ArrowRight'].includes(event.key))index=(i+1)%5;else if(['ArrowUp','ArrowLeft'].includes(event.key))index=(i+4)%5;else if(event.key==='Home')index=0;else if(event.key==='End')index=4;else return;event.preventDefault();selectChapter(index,{focus:true})});
 });
 const initial=keys.indexOf(location.hash.slice(1));if(initial>=0)selectChapter(initial,{hash:false});
 addEventListener('hashchange',()=>{const i=keys.indexOf(location.hash.slice(1));if(i>=0)selectChapter(i,{hash:false})});
}
// Project image viewer: native dialog supplies Escape, focus trapping, and focus restoration.
const lightbox=document.querySelector('.lightbox');
if(lightbox){
 const image=lightbox.querySelector('img');
 document.querySelectorAll('[data-enlarge]').forEach(button=>button.addEventListener('click',()=>{const source=button.querySelector('img');image.src=source.src;image.alt=source.alt;lightbox.showModal()}));
 lightbox.querySelector('button').addEventListener('click',()=>lightbox.close());
 lightbox.addEventListener('click',event=>{if(event.target===lightbox)lightbox.close()});
}
// Restrained cover parallax. No motion when the visitor requests reduced motion.
const parallax=document.querySelector('[data-parallax]');let parallaxVisible=false,parallaxPending=false;
function updateParallax(){parallaxPending=false;if(!parallaxVisible||reducedMotion.matches)return;const image=parallax.querySelector(':scope > img');if(!image)return;const r=parallax.getBoundingClientRect();const amount=Math.max(-1,Math.min(1,(innerHeight/2-r.top-r.height/2)/innerHeight));image.style.transform=`translateY(${amount*25}px)`}
if(parallax){new IntersectionObserver(entries=>{parallaxVisible=entries[0].isIntersecting;if(parallaxVisible)updateParallax()}).observe(parallax);addEventListener('scroll',()=>{if(!parallaxPending&&parallaxVisible){parallaxPending=true;requestAnimationFrame(updateParallax)}},{passive:true})}
const contact=document.querySelector('#contact-form');
if(contact)contact.addEventListener('submit',event=>{event.preventDefault();if(!contact.reportValidity())return;const data=new FormData(contact);const subject=`Portfolio inquiry from ${data.get('name')}`;const body=`Name: ${data.get('name')}\nEmail: ${data.get('email')}\n\n${data.get('message')}`;location.href=`mailto:${contact.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;document.querySelector('#contact-status').textContent='Your email draft is ready in your email app. Send it there to get in touch.'});
// Procedural form study: a shaded torus knot drawn locally without external assets.
const canvas=document.querySelector('#core-canvas');
if(canvas){
 const context=canvas.getContext('2d');const stage=canvas.parentElement,toggle=stage.querySelector('.motion-toggle');
 let width=1,height=1,angle=.6,px=0,py=0,tx=0,ty=0,paused=reducedMotion.matches,last=0,frame=0,visible=true;
 const N=112,M=18,vertices=[],faces=[];
 const normalize=v=>{const l=Math.hypot(...v)||1;return v.map(x=>x/l)};
 const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 function center(t){const r=1.12+.43*Math.cos(3*t);return[r*Math.cos(2*t),r*Math.sin(2*t),.65*Math.sin(3*t)]}
 for(let i=0;i<N;i++){
  const t=i/N*Math.PI*2,c=center(t),a=center(t+.002),b=center(t-.002),tangent=normalize(a.map((v,k)=>v-b[k]));
  const normal=normalize(cross(tangent,[0,0,1])),binormal=normalize(cross(tangent,normal));
  for(let j=0;j<M;j++){const s=j/M*Math.PI*2,n=normal.map((v,k)=>v*Math.cos(s)+binormal[k]*Math.sin(s));vertices.push({p:c.map((v,k)=>v+.29*n[k]),n})}
 }
 for(let i=0;i<N;i++)for(let j=0;j<M;j++)faces.push([i*M+j,((i+1)%N)*M+j,((i+1)%N)*M+(j+1)%M,i*M+(j+1)%M]);
 function rotate(v,az,ax){const c=Math.cos(az),s=Math.sin(az),cx=Math.cos(ax),sx=Math.sin(ax),x=v[0]*c+v[2]*s,z=-v[0]*s+v[2]*c;return[x,v[1]*cx-z*sx,v[1]*sx+z*cx]}
 function render(){
  context.clearRect(0,0,width,height);const scale=Math.min(width*.27,height*.31);const az=angle+px*.35,ax=-.45+py*.3;
  const pts=vertices.map(v=>{const p=rotate(v.p,az,ax),n=rotate(v.n,az,ax),perspective=5.7/(5.7-p[2]);return{x:width*.54+p[0]*scale*perspective,y:height*.48+p[1]*scale*perspective,z:p[2],n}});
  const gradient=context.createRadialGradient(width*.54,height*.86,0,width*.54,height*.86,scale*1.15);gradient.addColorStop(0,'rgba(45,55,48,.12)');gradient.addColorStop(1,'rgba(45,55,48,0)');context.save();context.translate(0,height*.7);context.scale(1,.19);context.translate(0,-height*.7);context.fillStyle=gradient;context.fillRect(0,0,width,height*2);context.restore();
  const sorted=faces.map(f=>({f,z:f.reduce((s,i)=>s+pts[i].z,0)/4})).sort((a,b)=>a.z-b.z);
  for(const {f} of sorted){const vs=f.map(i=>pts[i]);const n=normalize(vs.reduce((a,v)=>a.map((x,k)=>x+v.n[k]),[0,0,0]));const diffuse=Math.max(0,n[0]*-.45+n[1]*-.6+n[2]*.55);const shine=Math.pow(Math.max(0,n[2]),8)*24;const tone=Math.min(252,Math.max(105,156+diffuse*82+shine));context.beginPath();context.moveTo(vs[0].x,vs[0].y);for(let i=1;i<4;i++)context.lineTo(vs[i].x,vs[i].y);context.closePath();context.fillStyle=`rgb(${tone-2},${tone},${tone-1})`;context.fill();context.strokeStyle='rgba(47,58,49,.13)';context.lineWidth=.45;context.stroke()}
 }
 function resize(){const r=stage.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,1.7);width=r.width;height=r.height;canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);context.setTransform(dpr,0,0,dpr,0,0);render()}
 function animate(now){frame=requestAnimationFrame(animate);if(!visible||document.hidden||now-last<32)return;const dt=Math.min((now-last)/1000,.06);last=now;px+=(tx-px)*.06;py+=(ty-py)*.06;if(!paused)angle+=dt*.14;if(!paused||Math.abs(px-tx)+Math.abs(py-ty)>.002)render()}
 function updateToggle(){toggle.textContent=paused?'PLAY MOTION':'PAUSE MOTION';toggle.setAttribute('aria-pressed',String(paused))}
 toggle.addEventListener('click',()=>{paused=!paused;updateToggle();render()});
 stage.addEventListener('pointermove',event=>{if(reducedMotion.matches)return;const r=stage.getBoundingClientRect();tx=(event.clientX-r.left)/r.width-.5;ty=(event.clientY-r.top)/r.height-.5});stage.addEventListener('pointerleave',()=>{tx=0;ty=0});
 reducedMotion.addEventListener('change',()=>{paused=reducedMotion.matches;px=py=tx=ty=0;updateToggle();render()});
 new ResizeObserver(resize).observe(stage);new IntersectionObserver(entries=>visible=entries[0].isIntersecting).observe(canvas);updateToggle();resize();frame=requestAnimationFrame(animate);
 addEventListener('pagehide',()=>cancelAnimationFrame(frame),{once:true});
}

// Return to the preceding page, skipping this page's section/hash entries.
(() => {
 const pageKey = url => url.origin + url.pathname + url.search;
 document.addEventListener('click', event => {
  const link = event.target.closest('[data-page-back]');
  if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  const current = new URL(location.href);
  const entries = window.navigation?.entries();
  const index = window.navigation?.currentEntry?.index;
  if (entries && Number.isInteger(index)) {
   for (let i = index - 1; i >= 0; i--) {
    if (!entries[i].url) break;
    const previous = new URL(entries[i].url);
    if (pageKey(previous) === pageKey(current)) continue;
    if (previous.origin === current.origin) {
     event.preventDefault(); history.go(i - index);
    }
    return;
   }
  } else if (document.referrer) {
   const previous = new URL(document.referrer);
   if (previous.origin === current.origin && pageKey(previous) !== pageKey(current)) {
    event.preventDefault(); location.replace(previous.href);
   }
  }
 });
})();
