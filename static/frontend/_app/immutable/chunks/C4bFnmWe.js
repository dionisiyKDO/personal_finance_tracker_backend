import{M as s}from"./DiOX1np-.js";const r=s(null);async function m(e,t){try{const o=await fetch("/api/auth/login/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:e,password:t})});if(!o.ok){const a=(await o.json()).error||"Failed to fetch user info";return console.log(a),!1}const n={token:(await o.json()).token,username:e};return localStorage.setItem("token",n.token),localStorage.setItem("username",n.username),r.set({token:n.token,username:n.username}),!0}catch(o){return console.error("Error during login:",o),!1}}function g(){const e=localStorage.getItem("token"),t=localStorage.getItem("username");e&&t&&r.set({token:e,username:t})}function k(){localStorage.removeItem("token"),localStorage.removeItem("username"),r.set(null)}export{k as a,g as i,m as l,r as u};
