import{k as c,K as y,B as k,ag as p,af as h,ax as x,e as g,an as B,N as q,ao as A,i as C,L as w,ay as D,az as I,q as u,l as R,n as W}from"./DlLfKX1o.js";function J(e){c&&y(e)!==null&&k(e)}let T=!1;function F(){T||(T=!0,document.addEventListener("reset",e=>{Promise.resolve().then(()=>{var t;if(!e.defaultPrevented)for(const r of e.target.elements)(t=r.__on_r)==null||t.call(r)})},{capture:!0}))}function N(e){var t=x,r=g;p(null),h(null);try{return e()}finally{p(t),h(r)}}function Q(e,t,r,i=r){e.addEventListener(t,()=>N(r));const n=e.__on_r;n?e.__on_r=()=>{n(),i(!0)}:e.__on_r=()=>i(!0),F()}const U=new Set,j=new Set;function z(e,t,r,i={}){function n(a){if(i.capture||G.call(t,a),!a.cancelBubble)return N(()=>r==null?void 0:r.call(this,a))}return e.startsWith("pointer")||e.startsWith("touch")||e==="wheel"?q(()=>{t.addEventListener(e,n,i)}):t.addEventListener(e,n,i),n}function X(e,t,r,i,n){var a={capture:i,passive:n},o=z(e,t,r,a);(t===document.body||t===window||t===document)&&B(()=>{t.removeEventListener(e,o,a)})}function Y(e){for(var t=0;t<e.length;t++)U.add(e[t]);for(var r of j)r(e)}function G(e){var L;var t=this,r=t.ownerDocument,i=e.type,n=((L=e.composedPath)==null?void 0:L.call(e))||[],a=n[0]||e.target,o=0,_=e.__root;if(_){var f=n.indexOf(_);if(f!==-1&&(t===document||t===window)){e.__root=t;return}var E=n.indexOf(t);if(E===-1)return;f<=E&&(o=f)}if(a=n[o]||e.target,a!==t){A(e,"currentTarget",{configurable:!0,get(){return a||r}});var P=x,M=g;p(null),h(null);try{for(var l,b=[];a!==null;){var m=a.assignedSlot||a.parentNode||a.host||null;try{var d=a["__"+i];if(d!==void 0&&!a.disabled)if(C(d)){var[S,...O]=d;S.apply(a,[e,...O])}else d.call(a,e)}catch(v){l?b.push(v):l=v}if(e.cancelBubble||m===t||m===null)break;a=m}if(l){for(let v of b)queueMicrotask(()=>{throw v});throw l}}finally{e.__root=t,delete e.currentTarget,p(P),h(M)}}}function H(e){var t=document.createElement("template");return t.innerHTML=e,t.content}function s(e,t){var r=g;r.nodes_start===null&&(r.nodes_start=e,r.nodes_end=t)}function Z(e,t){var r=(t&D)!==0,i=(t&I)!==0,n,a=!e.startsWith("<!>");return()=>{if(c)return s(u,null),u;n===void 0&&(n=H(a?e:"<!>"+e),r||(n=y(n)));var o=i?document.importNode(n,!0):n.cloneNode(!0);if(r){var _=y(o),f=o.lastChild;s(_,f)}else s(o,o);return o}}function $(e=""){if(!c){var t=w(e+"");return s(t,t),t}var r=u;return r.nodeType!==3&&(r.before(r=w()),W(r)),s(r,r),r}function ee(){if(c)return s(u,null),u;var e=document.createDocumentFragment(),t=document.createComment(""),r=w();return e.append(t,r),s(t,r),e}function te(e,t){if(c){g.nodes_end=u,R();return}e!==null&&e.before(t)}const K="5";typeof window<"u"&&(window.__svelte||(window.__svelte={v:new Set})).v.add(K);export{F as a,te as b,ee as c,Y as d,X as e,U as f,s as g,G as h,J as i,$ as j,Q as l,j as r,Z as t};
