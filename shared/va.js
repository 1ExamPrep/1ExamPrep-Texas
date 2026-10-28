/* Small page behaviour for the listing pages: footer year, one FAQ open at a time. */
(function(){
  "use strict";
  document.querySelectorAll("[data-year]").forEach(function(el){el.textContent=new Date().getFullYear();});
  document.querySelectorAll(".faq details").forEach(function(d){d.addEventListener("toggle",function(){if(d.open)d.parentNode.querySelectorAll("details").forEach(function(o){if(o!==d)o.open=false;});});});
})();
/* Two-step license finder on the home page: pick a type, then a license, and go straight to its page. */
(function(){
  var f=document.querySelector("[data-finder]");if(!f)return;
  var g=f.querySelector("[data-fg]"),l=f.querySelector("[data-fl]"),all=[].slice.call(l.options);
  function fill(){var v=g.value;l.innerHTML="";all.forEach(function(o){if(o.getAttribute("data-g")===v)l.appendChild(o);});}
  g.addEventListener("change",fill);fill();
  f.addEventListener("submit",function(e){e.preventDefault();if(l.value)location.href=l.value;});
})();
/* Mark the current license in the side index. */
(function(){var p=location.pathname.replace(/index\.html$/,"");document.querySelectorAll(".tx-rail a").forEach(function(a){var h=a.pathname.replace(/index\.html$/,"");if(h!=="/"&&p.indexOf(h)===0)a.setAttribute("aria-current","page");});})();
