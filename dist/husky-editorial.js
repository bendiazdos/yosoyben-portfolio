// Real anchor links remain usable without JavaScript; highlight the section in view.
const editorialIndex=document.querySelector('.ed-index');
if(editorialIndex){
 const links=[...editorialIndex.querySelectorAll('a')];
 const sections=links.map(a=>document.getElementById(a.hash.slice(1))).filter(Boolean);
 let pending=false;
 function updateIndex(){
  pending=false;
  const offset=editorialIndex.offsetHeight+60;
  let current=sections[0];
  for(const section of sections)if(section.getBoundingClientRect().top<=offset)current=section;
  links.forEach(link=>{if(link.hash==='#'+current.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')});
 }
 function schedule(){if(!pending){pending=true;requestAnimationFrame(updateIndex)}}
 addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);updateIndex();
}
// Keep existing chapter bookmarks useful after the editorial migration.
const legacyChapters={'#overview':'challenge','#goals':'challenge','#process':'interaction','#visual-system':'visual-language','#why-it-worked':'outcomes'};
function followLegacyChapter(){const target=legacyChapters[location.hash];if(target)document.getElementById(target)?.scrollIntoView({behavior:'instant'});}
addEventListener('hashchange',followLegacyChapter);followLegacyChapter();
