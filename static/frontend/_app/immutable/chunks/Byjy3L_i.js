import{am as v,al as p,ap as P,l as h,R as A,D as B,T as D,z as R,A as T,aq as k,ar as q,h as m,e as u,a as C,B as w,s as I}from"./DiOX1np-.js";let L=!1;function W(){L||(L=!0,document.addEventListener("reset",e=>{Promise.resolve().then(()=>{var r;if(!e.defaultPrevented)for(const t of e.target.elements)(r=t.__on_r)==null||r.call(t)})},{capture:!0}))}function M(e){var r=P,t=h;v(null),p(null);try{return e()}finally{v(r),p(t)}}function J(e,r,t,i=t){e.addEventListener(r,()=>M(t));const n=e.__on_r;n?e.__on_r=()=>{n(),i(!0)}:e.__on_r=()=>i(!0),W()}const F=new Set,U=new Set;function z(e,r,t,i={}){function n(a){if(i.capture||G.call(r,a),!a.cancelBubble)return M(()=>t==null?void 0:t.call(this,a))}return e.startsWith("pointer")||e.startsWith("touch")||e==="wheel"?B(()=>{r.addEventListener(e,n,i)}):r.addEventListener(e,n,i),n}function K(e,r,t,i,n){var a={capture:i,passive:n},o=z(e,r,t,a);(r===document.body||r===window||r===document)&&A(()=>{r.removeEventListener(e,o,a)})}function Q(e){for(var r=0;r<e.length;r++)F.add(e[r]);for(var t of U)t(e)}function G(e){var b;var r=this,t=r.ownerDocument,i=e.type,n=((b=e.composedPath)==null?void 0:b.call(e))||[],a=n[0]||e.target,o=0,c=e.__root;if(c){var f=n.indexOf(c);if(f!==-1&&(r===document||r===window)){e.__root=r;return}var y=n.indexOf(r);if(y===-1)return;f<=y&&(o=f)}if(a=n[o]||e.target,a!==r){D(e,"currentTarget",{configurable:!0,get(){return a||t}});var N=P,S=h;v(null),p(null);try{for(var _,E=[];a!==null;){var g=a.assignedSlot||a.parentNode||a.host||null;try{var l=a["__"+i];if(l!==void 0&&!a.disabled)if(R(l)){var[x,...O]=l;x.apply(a,[e,...O])}else l.call(a,e)}catch(d){_?E.push(d):_=d}if(e.cancelBubble||g===r||g===null)break;a=g}if(_){for(let d of E)queueMicrotask(()=>{throw d});throw _}}finally{e.__root=r,delete e.currentTarget,v(N),p(S)}}}function H(e){var r=document.createElement("template");return r.innerHTML=e,r.content}function s(e,r){var t=h;t.nodes_start===null&&(t.nodes_start=e,t.nodes_end=r)}function X(e,r){var t=(r&k)!==0,i=(r&q)!==0,n,a=!e.startsWith("<!>");return()=>{if(m)return s(u,null),u;n===void 0&&(n=H(a?e:"<!>"+e),t||(n=T(n)));var o=i?document.importNode(n,!0):n.cloneNode(!0);if(t){var c=T(o),f=o.lastChild;s(c,f)}else s(o,o);return o}}function Y(e=""){if(!m){var r=w(e+"");return s(r,r),r}var t=u;return t.nodeType!==3&&(t.before(t=w()),I(t)),s(t,t),t}function Z(){if(m)return s(u,null),u;var e=document.createDocumentFragment(),r=document.createComment(""),t=w();return e.append(r,t),s(r,t),e}function $(e,r){if(m){h.nodes_end=u,C();return}e!==null&&e.before(r)}const V="5";typeof window<"u"&&(window.__svelte||(window.__svelte={v:new Set})).v.add(V);export{W as a,F as b,s as c,$ as d,K as e,Z as f,Q as g,G as h,Y as i,J as l,U as r,X as t};
