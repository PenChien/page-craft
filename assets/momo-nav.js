/* Momo 章節導覽列：捲到哪章亮哪章。捕捉階段監聽捲動，頁面放在網頁程式的內層捲動元素裡也收得到。
   判定線用導覽列實際高度，多排換行時才不會亮錯章。 */
(function(){
  var nav=document.querySelector('nav.mnav'); if(!nav) return;
  var links=[].slice.call(nav.querySelectorAll('a[href^="#"]'));
  var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});
  function pad(){document.documentElement.style.scrollPaddingTop=(nav.offsetHeight+8)+'px';}
  function upd(){
    var y=nav.getBoundingClientRect().bottom+24, cur=0;   // 比 scroll-padding 多留 16px，錨點跳轉落在線上時不會差一點沒過
    secs.forEach(function(s,i){ if(s && s.getBoundingClientRect().top<=y) cur=i; });
    links.forEach(function(a,i){ a.classList.toggle('on', i===cur); });
  }
  document.addEventListener('scroll',upd,true);
  window.addEventListener('resize',function(){pad();upd();});
  pad(); upd();
})();
