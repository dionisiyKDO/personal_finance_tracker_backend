import{j as m,k as o,l as I,aj as A,H as S,r as R,n as U,p as v,u as p,v as h,w as g,U as k,q as D,ak as y,z as j,al as q,am as w,g as x,an as F,c as H,ao as L}from"./DlLfKX1o.js";function z(a,s,n=!1){o&&I();var e=a,r=null,u=null,i=k,T=n?A:0,l=!1;const E=(c,t=!0)=>{l=!0,b(t,c)},b=(c,t)=>{if(i===(i=c))return;let d=!1;if(o){const N=e.data===S;!!i===N&&(e=R(),U(e),v(!1),d=!0)}i?(r?p(r):t&&(r=h(()=>t(e))),u&&g(u,()=>{u=null})):(u?p(u):t&&(u=h(()=>t(e))),r&&g(r,()=>{r=null})),d&&v(!0)};m(()=>{l=!1,s(E),l||b(null,null)},T),o&&(e=D)}let f=!1,_=Symbol();function C(a,s,n){const e=n[s]??(n[s]={store:null,source:j(void 0),unsubscribe:y});if(e.store!==a&&!(_ in n))if(e.unsubscribe(),e.store=a??null,a==null)e.source.v=void 0,e.unsubscribe=y;else{var r=!0;e.unsubscribe=q(a,u=>{r?e.source.v=u:H(e.source,u)}),r=!1}return a&&_ in n?w(a):x(e.source)}function M(){const a={};function s(){F(()=>{for(var n in a)a[n].unsubscribe();L(a,_,{enumerable:!1,value:!0})})}return[a,s]}function P(a){var s=f;try{return f=!1,[a(),f]}finally{f=s}}export{M as a,P as c,z as i,C as s};
