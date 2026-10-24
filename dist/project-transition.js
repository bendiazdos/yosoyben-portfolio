(()=>{
 const mediaPreference=matchMedia('(prefers-reduced-motion: reduce)');
 // Keep an explicitly enabled local review mode across archive/home navigation.
 const localHost=['127.0.0.1','localhost'].includes(location.hostname);
 const motionMode=new URLSearchParams(location.search).get('motion');
 let localMotionPreview=localHost&&motionMode==='preview';
 if(localHost){try{
  if(motionMode==='preview')sessionStorage.setItem('portfolio-motion-preview','true');
  else if(motionMode==='system')sessionStorage.removeItem('portfolio-motion-preview');
  if(motionMode!=='system')localMotionPreview=sessionStorage.getItem('portfolio-motion-preview')==='true';
 }catch{}}

 const reduced={get matches(){return mediaPreference.matches&&!localMotionPreview}};
 if(localMotionPreview){document.documentElement.classList.add('motion-preview');document.body.classList.add('motion-preview');const style=document.createElement('style');style.textContent='@view-transition{navigation:auto}';document.head.append(style);}
 const isHome=()=>!!document.querySelector('.project-stage');
 const shared=()=>isHome()?document.querySelector('.project-visual'):document.querySelector('.ed-hero .ed-image');
 const native='onpageswap' in window&&'onpagereveal' in window;
 let navigating=false,timer,clone;
 const put=value=>{try{sessionStorage.setItem('portfolio-arrival',JSON.stringify(value))}catch{}};
 function arrive(){
  document.body.classList.remove('is-opening');navigating=false;clone?.remove();clone=null;
  if(isHome())return;
  try{const data=JSON.parse(sessionStorage.getItem('portfolio-arrival')||'null');
   if(data?.path===location.pathname&&Date.now()-data.time<5000){document.body.classList.add('is-arriving');sessionStorage.removeItem('portfolio-arrival');setTimeout(()=>document.body.classList.remove('is-arriving'),800);}
  }catch{}
 }
 addEventListener('pageswap',event=>{
  if(!event.viewTransition||reduced.matches)return;
  const target=event.activation?.entry?.url;
  if(!isHome()||!target||!new URL(target).pathname.startsWith('/work/'))return;
  const media=shared();if(media){media.style.viewTransitionName='project-bridge';event.viewTransition.finished.finally(()=>media.style.removeProperty('view-transition-name'));}
 });
 addEventListener('pagereveal',event=>{
  if(!event.viewTransition||reduced.matches||isHome())return;
  const from=window.navigation?.activation?.from?.url;
  if(from&&new URL(from).pathname!=='/')return;
  const media=shared();if(media){media.style.viewTransitionName='project-bridge';event.viewTransition.finished.finally(()=>media.style.removeProperty('view-transition-name'));}
 });
 document.addEventListener('click',async event=>{
  const link=event.target.closest('.project-stage [data-project-link]');if(!link)return;
  if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  if(reduced.matches)return;
  event.preventDefault();if(navigating)return;navigating=true;
  const preparation={ready:Promise.resolve()};document.dispatchEvent(new CustomEvent('portfolio:prepare-open',{detail:preparation}));
  document.body.classList.add('is-opening');await preparation.ready;if(!navigating)return;
  const destination=new URL(link.href);put({path:destination.pathname,time:Date.now()});
  if(native){timer=setTimeout(()=>location.assign(destination.href),170);return;}
  // Continuous fallback for browsers without cross-document View Transitions.
  const media=shared(),img=media?.querySelector('img.is-front');
  if(img){const r=media.getBoundingClientRect();clone=img.cloneNode();clone.className='route-media-bridge';clone.alt='';clone.setAttribute('aria-hidden','true');Object.assign(clone.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px'});document.body.append(clone);clone.animate([{transform:'translateX(0) rotateY(0deg)',opacity:1},{transform:`translateX(${-Math.min(r.left-24,innerWidth*.3)}px) rotateY(-10deg)`,opacity:.25}],{duration:470,easing:'cubic-bezier(.22,1,.36,1)',fill:'forwards'});}
  timer=setTimeout(()=>location.assign(destination.href),450);
 });
 addEventListener('keydown',event=>{if(event.key==='Escape'&&navigating){clearTimeout(timer);clone?.remove();clone=null;navigating=false;document.body.classList.remove('is-opening');document.dispatchEvent(new Event('portfolio:cancel-open'))}});
 addEventListener('pageshow',arrive);arrive();
})();
