import{t as m,d as x,f as At}from"../chunks/Byjy3L_i.js";import{i as Ct}from"../chunks/C-xWZpZg.js";import{ag as qt,b as zt,h as M,a as Ft,ak as Ht,U as dt,m as Q,o as vt,n as ft,j as G,D as St,e as Bt,al as ut,am as _t,an as pt,a0 as Gt,i as W,p as X,ao as Jt,$ as Ot,a1 as Pt,af as i,ad as e,ae as t,ac as J,g as s,ab as xt,d as Y}from"../chunks/DiOX1np-.js";import{s as n}from"../chunks/9GPvL92g.js";import{s as Rt,a as Vt,i as D}from"../chunks/Cyrhthi-.js";import{e as gt,i as mt}from"../chunks/CMkO9gSr.js";import{u as Zt}from"../chunks/C8XgMGF-.js";const tt=0,O=1,at=2;function Kt(c,d,f,b,j){M&&Ft();var g=c,u=qt(),I=Gt,_=dt,r,a,l,h=(u?vt:ft)(void 0),y=(u?vt:ft)(void 0),T=!1;function v(o,p){T=!0,p&&(ut(w),_t(w),pt(I));try{o===tt&&f&&(r?W(r):r=G(()=>f(g))),o===O&&b&&(a?W(a):a=G(()=>b(g,h))),o===at&&j&&(l?W(l):l=G(()=>j(g,y))),o!==tt&&r&&X(r,()=>r=null),o!==O&&a&&X(a,()=>a=null),o!==at&&l&&X(l,()=>l=null)}finally{p&&(pt(null),_t(null),ut(null),Jt())}}var w=zt(()=>{if(_!==(_=d())){if(Ht(_)){var o=_;T=!1,o.then(p=>{o===_&&(Q(h,p),v(O,!0))},p=>{if(o===_&&(Q(y,p),v(at,!0),!j))throw y.v}),M?f&&(r=G(()=>f(g))):St(()=>{T||v(tt,!0)})}else Q(h,_),v(O,!1);return()=>_=dt}});M&&(g=Bt)}function bt(c,d,f){if(f){if(c.classList.contains(d))return;c.classList.add(d)}else{if(!c.classList.contains(d))return;c.classList.remove(d)}}async function Mt(c){try{if(!c)return null;const f=window.location.port!=="8000"?"http://localhost:8000":"",b=await fetch(`${f}/api/dashboard-data/`,{method:"GET",headers:{Authorization:`Token ${c.token}`,"Content-Type":"application/json"}});if(!b.ok){const u=(await b.json()).error||"Failed to fetch dashboard data";return console.log(u),null}return await b.json()}catch(d){return console.error("Error during login:",d),null}}var Qt=m('<div class="flex justify-between items-center"><span class="capitalize"> </span> <div class="text-right"><div class="font-semibold"> </div> <div class="text-sm text-gray-500"> </div></div></div>'),Wt=m('<div class="flex justify-between items-center"><span class="w-2/3 text-nowrap overflow-x-hidden text-ellipsis"> </span> <div class="text-right"><div class="font-semibold"> </div> <div class="text-sm text-gray-500"> </div></div></div>'),Xt=m('<div class="bg-[--surface] p-4 rounded-lg shadow"><h3 class="text-lg font-semibold mb-4">Top Vendors</h3> <div class="space-y-3"></div></div>'),Yt=m('<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6"><div class="bg-[--surface] p-4 rounded-lg shadow"><h3 class="text-lg font-semibold mb-4">Expense Categories</h3> <div class="space-y-3"></div></div> <!></div>'),Dt=m('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6"><div class="bg-[--surface] p-4 rounded-lg shadow"><h3 class="text-lg font-semibold text-gray-200">Income</h3> <p class="text-2xl font-bold text-green-600"> </p> <p class="text-sm text-gray-500"> </p></div> <div class="bg-[--surface] p-4 rounded-lg shadow"><h3 class="text-lg font-semibold text-gray-200">Expenses</h3> <p class="text-2xl font-bold text-red-600"> </p> <p class="text-sm text-gray-500"> </p></div> <div class="bg-[--surface] p-4 rounded-lg shadow"><h3 class="text-lg font-semibold text-gray-200">Net Balance</h3> <p class="text-2xl font-bold"> </p> <p class="text-sm text-gray-500"> </p></div></div> <!> <div class="mt-8 p-4 bg-[--surface] rounded"><h3 class="text-sm font-mono">Debug Data:</h3> <pre class="text-xs overflow-auto"> </pre></div>',1),ta=m('<div class="bg-[--surface] border border-yellow-200 text-yellow-600 p-4 rounded-lg"><p>No dashboard data available</p></div>'),aa=m('<div class="bg-[--surface] border border-red-200 text-red-700 p-4 rounded-lg"><p> </p></div>'),ea=m('<div class="flex items-center justify-center h-64"><p class="text-gray-500">Loading dashboard data...</p></div>'),sa=m('<div class="p-4 container mx-auto"><h1 class="text-3xl font-bold mb-6">Financial Dashboard</h1> <!></div>');function va(c,d){Ot(d,!1);const[f,b]=Vt(),g=Mt(Rt(Zt,"$user",f)),u=(r,a="UAH")=>r==null?"-":new Intl.NumberFormat("uk-UA",{style:"currency",currency:a}).format(r);g.then(r=>{console.log("Dashboard data received:",r)}).catch(r=>{console.error("Dashboard data error:",r)}),Ct();var I=sa(),_=i(e(I),2);Kt(_,()=>g,r=>{var a=ea();x(r,a)},(r,a)=>{var l=At(),h=xt(l);{var y=v=>{var w=Dt(),o=xt(w),p=e(o),P=i(e(p),2),ht=e(P,!0);t(P);var et=i(P,2),yt=e(et);t(et),t(p);var R=i(p,2),V=i(e(R),2),wt=e(V,!0);t(V);var st=i(V,2),$t=e(st);t(st),t(R);var rt=i(R,2),L=i(e(rt),2),kt=e(L,!0);t(L);var it=i(L,2),Nt=e(it);t(it),t(rt),t(o);var ot=i(o,2);{var Et=U=>{var A=Yt(),C=e(A),B=i(e(C),2);gt(B,5,()=>s(a).data.expense_categories,mt,(q,$)=>{var N=Qt(),z=e(N),F=e(z,!0);t(z);var E=i(z,2),k=e(E),Z=e(k,!0);t(k);var H=i(k,2),S=e(H);t(H),t(E),t(N),J(K=>{n(F,s($).category||"Uncategorized"),n(Z,K),n(S,`${s($).count??""} transactions`)},[()=>u(s($).total)],Y),x(q,N)}),t(B),t(C);var It=i(C,2);{var Tt=q=>{var $=Xt(),N=i(e($),2);gt(N,5,()=>s(a).data.top_vendors,mt,(z,F)=>{var E=Wt(),k=e(E),Z=e(k,!0);t(k);var H=i(k,2),S=e(H),K=e(S,!0);t(S);var ct=i(S,2),Lt=e(ct);t(ct),t(H),t(E),J(Ut=>{n(Z,s(F).vendor||"Unknown"),n(K,Ut),n(Lt,`${s(F).transaction_count??""} transactions`)},[()=>u(s(F).total_spent)],Y),x(z,E)}),t(N),t($),x(q,$)};D(It,q=>{s(a).data.top_vendors&&q(Tt)})}t(A),x(U,A)};D(ot,U=>{s(a).data.expense_categories&&U(Et)})}var nt=i(ot,2),lt=i(e(nt),2),jt=e(lt,!0);t(lt),t(nt),J((U,A,C,B)=>{n(ht,U),n(yt,`${s(a).data.basic_stats.income.count||0} transactions`),n(wt,A),n($t,`${s(a).data.basic_stats.expenses.count||0} transactions`),bt(L,"text-green-600",s(a).data.basic_stats.net>0),bt(L,"text-red-600",s(a).data.basic_stats.net<0),n(kt,C),n(Nt,`${s(a).data.basic_stats.total_transactions||0} total transactions`),n(jt,B)},[()=>u(s(a).data.basic_stats.income.total),()=>u(s(a).data.basic_stats.expenses.total),()=>u(s(a).data.basic_stats.net),()=>JSON.stringify(s(a),null,2)],Y),x(v,w)},T=v=>{var w=ta();x(v,w)};D(h,v=>{s(a)&&s(a).data&&s(a).data.basic_stats?v(y):v(T,!1)})}x(r,l)},(r,a)=>{var l=aa(),h=e(l),y=e(h);t(h),t(l),J(()=>n(y,`Error loading dashboard: ${s(a)??""}`)),x(r,l)}),t(I),x(c,I),Pt(),b()}export{va as component};
