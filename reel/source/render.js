const {chromium}=require('playwright');
const path=require('path'),fs=require('fs');
(async()=>{
  const [,,html,out,mode]=process.argv;
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve(html));
  await p.evaluate(()=>window.ready);
  fs.mkdirSync(out,{recursive:true});
  let times;
  if(mode==='preview') times=[0.5,1.5,1.9,2.6,4.9,7.6,8.2,9.8,12.8,13.2,15.0,15.6,17.8,18.3,19.0,21.5];
  else {const N=Math.round(+mode*30);times=[...Array(N).keys()].map(i=>i/30);}
  for(let i=0;i<times.length;i++){
    await p.evaluate(t=>window.render(t),times[i]);
    const f=mode==='preview'?`p_${times[i].toFixed(2)}.jpg`:`${String(i).padStart(5,'0')}.jpg`;
    await p.screenshot({path:path.join(out,f),type:'jpeg',quality:94});
  }
  await b.close();
})();
