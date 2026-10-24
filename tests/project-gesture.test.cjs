const assert=require('node:assert/strict');
const Gesture=require('../dist/project-gesture.js');
function replay(samples){const g=new Gesture();return samples.map(([delta,mode,time])=>g.push(delta,mode,time)).filter(Boolean)}
const burst=(values,start=0,mode=0,step=16)=>values.map((delta,i)=>[delta,mode,start+i*step]);
const trackpad=[2,4,8,14,22,30,28,24,20,17,14,12,10,8,7,6,5,4,3,2,1,.7];
assert.deepEqual(replay(burst(trackpad)),[1],'one trackpad gesture, including its momentum, advances once');
assert.deepEqual(replay([...burst(trackpad),...burst(trackpad,560)]),[1,1],'a second intentional gesture responds without a fixed cooldown');
assert.deepEqual(replay([...burst(trackpad),...burst(trackpad.map(x=>-x),560)]),[1,-1],'reverse trackpad direction returns one project');
assert.deepEqual(replay([[100,0,0],[100,0,40],[100,0,85],[100,0,285]]),[1,1],'mouse-wheel burst and separate wheel action');
assert.deepEqual(replay([[3,1,0],[-3,1,100]]),[1,-1],'line-mode wheel direction reversal');
assert.deepEqual(replay([[1,2,0]]),[1],'page-mode wheel input');
assert.deepEqual(replay(burst(Array(120).fill(12))),[1],'a long uninterrupted momentum stream cannot skip projects');
assert.deepEqual(replay([[2,0,0],[-2,0,20],[1,0,40],[-1,0,60]]),[],'tiny direction jitter does not navigate');
assert.deepEqual(replay([[100,0,0],[100,0,190]]),[1,1],'new input during the visual transition remains intentional input');
assert.deepEqual(replay([...burst(trackpad),...burst(trackpad,352)]),[1,1],'a fresh swipe after a tail responds without waiting for silence');
assert.deepEqual(replay([[100,0,0],[100,0,100],[100,0,200]]),[1,1,1],'separate pixel-mode wheel ticks remain responsive');
assert.deepEqual(replay([[3,1,0],[3,1,100],[3,1,200]]),[1,1,1],'separate line-mode wheel ticks remain responsive');
assert.deepEqual(replay(burst([30,25,20,12,7,4,2,1,2,3,2,1,.7])),[1],'small momentum rebounds do not advance');
console.log('13 wheel and trackpad-momentum scenarios passed.');
