/* Admin Review Tool — visible only to AESOP-YAPT */
(function(){
  if(localStorage.getItem('aesop-learner-id')!=='AESOP-YAPT') return;

  const PROXY='/aesop-api/proxy.php';

  const style=document.createElement('style');
  style.textContent=`
#ar-btn{position:fixed;bottom:22px;right:22px;background:#12122a;color:#c9a84c;border:1.5px solid #c9a84c;border-radius:7px;padding:9px 16px;font:700 13px/1 'Nunito Sans',sans-serif;cursor:pointer;z-index:9999;display:none;box-shadow:0 3px 14px rgba(0,0,0,.55);transition:background .15s,opacity .15s;}
#ar-btn.visible{display:block;}
#ar-btn:hover{background:#1e1e44;}
#ar-panel{position:fixed;top:0;right:-450px;width:430px;height:100vh;background:#0d0d1e;border-left:1px solid #c9a84c44;z-index:10000;display:flex;flex-direction:column;transition:right .25s ease;font-family:'Nunito Sans',sans-serif;box-shadow:-4px 0 24px rgba(0,0,0,.5);}
#ar-panel.open{right:0;}
#ar-ph{padding:15px 18px;border-bottom:1px solid #c9a84c33;display:flex;justify-content:space-between;align-items:center;}
#ar-title{color:#c9a84c;font:700 13px/1 inherit;letter-spacing:.04em;}
#ar-close{background:none;border:none;color:#666;font-size:22px;cursor:pointer;padding:0;line-height:1;}
#ar-close:hover{color:#aaa;}
#ar-orig{margin:14px 18px 0;padding:10px 13px;background:#1a1a30;border-left:3px solid #c9a84c;color:#bbb;font-size:12.5px;line-height:1.55;border-radius:0 5px 5px 0;max-height:110px;overflow-y:auto;font-style:italic;}
#ar-result{flex:1;overflow-y:auto;padding:14px 18px;color:#ddd;font-size:13.5px;line-height:1.7;white-space:pre-wrap;}
#ar-result em{color:#888;font-style:italic;}
#ar-footer{padding:12px 18px;border-top:1px solid #c9a84c22;display:flex;gap:8px;}
.ar-btn2{flex:1;padding:8px 10px;border:1px solid #c9a84c55;background:#1a1a30;color:#c9a84c;border-radius:6px;font:600 12px/1 'Nunito Sans',sans-serif;cursor:pointer;transition:background .15s;}
.ar-btn2:hover{background:#252545;}
.ar-btn2:disabled{opacity:.35;cursor:default;}
  `;
  document.head.appendChild(style);

  const btn=document.createElement('button');
  btn.id='ar-btn';
  btn.textContent='✦ Review Selection';
  document.body.appendChild(btn);

  const panel=document.createElement('div');
  panel.id='ar-panel';
  panel.innerHTML=`
<div id="ar-ph"><span id="ar-title">✦ Admin Review</span><button id="ar-close" title="Close">×</button></div>
<div id="ar-orig"></div>
<div id="ar-result"><em>Select text in the lesson and click Review Selection.</em></div>
<div id="ar-footer">
  <button class="ar-btn2" id="ar-rewrite" disabled>↻ Rewrite</button>
  <button class="ar-btn2" id="ar-copy" disabled>⎘ Copy</button>
</div>`;
  document.body.appendChild(panel);

  let sel='';

  document.addEventListener('mouseup',function(){
    const s=window.getSelection();
    const t=s?s.toString().trim():'';
    if(t.length>10){sel=t;btn.classList.add('visible');}
    else{btn.classList.remove('visible');}
  });

  document.getElementById('ar-close').addEventListener('click',function(){
    panel.classList.remove('open');
  });

  async function callProxy(system,userMsg){
    const res=await fetch(PROXY,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        model:'claude-sonnet-4-6',
        max_tokens:700,
        system:system,
        messages:[{role:'user',content:userMsg}]
      })
    });
    if(!res.ok) throw new Error('HTTP '+res.status);
    const d=await res.json();
    return(d.content&&d.content[0]&&d.content[0].text)||'No response.';
  }

  btn.addEventListener('click',async function(){
    if(!sel) return;
    const orig=document.getElementById('ar-orig');
    const result=document.getElementById('ar-result');
    const rewrite=document.getElementById('ar-rewrite');
    const copy=document.getElementById('ar-copy');
    orig.textContent=sel;
    result.innerHTML='<em>Evaluating…</em>';
    rewrite.disabled=true;
    copy.disabled=true;
    panel.classList.add('open');
    btn.classList.remove('visible');
    try{
      const text=await callProxy(
        'You are an educational content reviewer for Aesop Academy, an AI literacy platform for middle and high school students. Review the provided text for factual accuracy, clarity, and age-appropriateness. Lead with a one-word verdict: Accurate, Unclear, or Inaccurate. Then give concise bullet points on specific issues or confirmations. Be direct.',
        `Review this lesson text:\n\n"${sel}"`
      );
      result.textContent=text;
      rewrite.disabled=false;
      copy.disabled=false;
    }catch(e){
      result.innerHTML='<em>⚠ API unavailable. Check connection.</em>';
    }
  });

  document.getElementById('ar-rewrite').addEventListener('click',async function(){
    const result=document.getElementById('ar-result');
    const rewrite=this;
    const copy=document.getElementById('ar-copy');
    rewrite.disabled=true;
    copy.disabled=true;
    result.innerHTML='<em>Rewriting…</em>';
    try{
      const text=await callProxy(
        'You are a content writer for Aesop Academy, an AI literacy platform for middle and high school students. Rewrite the provided text to be accurate, clear, and age-appropriate. Match the original tone and approximate length. Return only the rewritten text — no labels, no commentary.',
        `Rewrite this lesson text:\n\n"${sel}"`
      );
      result.textContent=text;
      rewrite.disabled=false;
      copy.disabled=false;
    }catch(e){
      result.innerHTML='<em>⚠ API unavailable.</em>';
      rewrite.disabled=false;
    }
  });

  document.getElementById('ar-copy').addEventListener('click',function(){
    const text=document.getElementById('ar-result').textContent;
    navigator.clipboard.writeText(text).then(function(){
      const c=document.getElementById('ar-copy');
      c.textContent='✓ Copied';
      setTimeout(function(){c.textContent='⎘ Copy';},1800);
    });
  });
})();
