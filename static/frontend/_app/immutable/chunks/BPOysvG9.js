import{n as v,l as p,ap as P,C as h,a7 as k,j as C,a9 as q,O as A,P as T,Q as y,aq as B,ar as D,h as m,k as u,c as I,y as R}from"./C-rDJMBQ.js";let L=!1;function W(){L||(L=!0,document.addEventListener("reset",e=>{Promise.resolve().then(()=>{var r;if(!e.defaultPrevented)for(const t of e.target.elements)(r=t.__on_r)==null||r.call(t)})},{capture:!0}))}function M(e){var r=P,t=h;v(null),p(null);try{return e()}finally{v(r),p(t)}}function z(e,r,t,i=t){e.addEventListener(r,()=>M(t));const n=e.__on_r;n?e.__on_r=()=>{n(),i(!0)}:e.__on_r=()=>i(!0),W()}const F=new Set,U=new Set;function j(e,r,t,i={}){function n(a){if(i.capture||G.call(r,a),!a.cancelBubble)return M(()=>t==null?void 0:t.call(this,a))}return e.startsWith("pointer")||e.startsWith("touch")||e==="wheel"?C(()=>{r.addEventListener(e,n,i)}):r.addEventListener(e,n,i),n}function J(e,r,t,i,n){var a={capture:i,passive:n},o=j(e,r,t,a);(r===document.body||r===window||r===document)&&k(()=>{r.removeEventListener(e,o,a)})}function K(e){for(var r=0;r<e.length;r++)F.add(e[r]);for(var t of U)t(e)}function G(e){var b;var r=this,t=r.ownerDocument,i=e.type,n=((b=e.composedPath)==null?void 0:b.call(e))||[],a=n[0]||e.target,o=0,c=e.__root;if(c){var f=n.indexOf(c);if(f!==-1&&(r===document||r===window)){e.__root=r;return}var w=n.indexOf(r);if(w===-1)return;f<=w&&(o=f)}if(a=n[o]||e.target,a!==r){q(e,"currentTarget",{configurable:!0,get(){return a||t}});var N=P,O=h;v(null),p(null);try{for(var _,E=[];a!==null;){var g=a.assignedSlot||a.parentNode||a.host||null;try{var l=a["__"+i];if(l!==void 0&&!a.disabled)if(A(l)){var[S,...x]=l;S.apply(a,[e,...x])}else l.call(a,e)}catch(d){_?E.push(d):_=d}if(e.cancelBubble||g===r||g===null)break;a=g}if(_){for(let d of E)queueMicrotask(()=>{throw d});throw _}}finally{e.__root=r,delete e.currentTarget,v(N),p(O)}}}function H(e){var r=document.createElement("template");return r.innerHTML=e,r.content}function s(e,r){var t=h;t.nodes_start===null&&(t.nodes_start=e,t.nodes_end=r)}function X(e,r){var t=(r&B)!==0,i=(r&D)!==0,n,a=!e.startsWith("<!>");return()=>{if(m)return s(u,null),u;n===void 0&&(n=H(a?e:"<!>"+e),t||(n=T(n)));var o=i?document.importNode(n,!0):n.cloneNode(!0);if(t){var c=T(o),f=o.lastChild;s(c,f)}else s(o,o);return o}}function Y(e=""){if(!m){var r=y(e+"");return s(r,r),r}var t=u;return t.nodeType!==3&&(t.before(t=y()),R(t)),s(t,t),t}function Z(){if(m)return s(u,null),u;var e=document.createDocumentFragment(),r=document.createComment(""),t=y();return e.append(r,t),s(r,t),e}function $(e,r){if(m){h.nodes_end=u,I();return}e!==null&&e.before(r)}const Q="5";typeof window<"u"&&(window.__svelte||(window.__svelte={v:new Set})).v.add(Q);export{W as a,$ as b,Z as c,F as d,s as e,K as f,J as g,G as h,Y as i,z as l,U as r,X as t};
