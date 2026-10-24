/* A gesture ends at silence, not when an animation timer expires. */
(function(root){
 class ProjectGesture {
  constructor(){this.reset()}
  reset(){this.last=-Infinity;this.direction=0;this.sum=0;this.consumed=false;this.valley=Infinity;this.peak=0;this.rising=0;this.triggered=-Infinity}
  push(delta,mode,time,pageHeight=900){
   const magnitude=Math.abs(delta)*(mode===1?16:mode===2?pageHeight:1);
   if(magnitude<.5)return 0;
   const direction=Math.sign(delta),gap=time-this.last;
   // Reversing a deliberate gesture can respond before the inertia gap expires.
   const reversed=direction!==this.direction&&magnitude>=10&&gap>65;
   if(gap>170||reversed){this.sum=0;this.consumed=false;this.direction=direction}
   this.last=time;
   if(this.consumed){
    this.valley=Math.min(this.valley,magnitude);
    this.rising=magnitude>this.previous*1.15?this.rising+1:0;
    // A fresh push after a decaying tail is a new gesture, even without silence.
    const freshPush=time-this.triggered>180&&this.peak>this.valley*2&&this.rising>=2&&magnitude>=10&&magnitude>this.valley*2.5;
    // Discrete wheel ticks can repeat without trackpad-style acceleration.
    const wheelTick=gap>=80&&(mode!==0||magnitude>=80);
    this.previous=magnitude;
    if(!freshPush&&!wheelTick)return 0;
    this.consumed=false;this.sum=0;
   }
   this.previous=magnitude;
   this.peak=Math.max(this.peak,magnitude);
   if(direction!==this.direction){this.sum=0;this.direction=direction}
   this.sum+=Math.min(magnitude,120);
   if(this.sum<24)return 0;
   this.consumed=true;this.sum=0;this.triggered=time;this.valley=magnitude;this.peak=magnitude;this.rising=0;return direction;
  }
 }
 if(typeof module==='object'&&module.exports)module.exports=ProjectGesture;
 else root.ProjectGesture=ProjectGesture;
})(typeof window==='object'?window:globalThis);
