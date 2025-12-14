// document.addEventListener("DOMContentLoaded", () => {
//   const protectedPages = ["/dashboard", "/profile", "/create"];
//   if (protectedPages.includes(location.pathname) && !localStorage.getItem("token")) {
//     location.href = "/";
//     return;
//   }

//   document.getElementById("logoutBtn")?.addEventListener("click", logout);
//   document.getElementById("createBtn")?.addEventListener("click", () => location.href="/create");
//   document.getElementById("profileBtn")?.addEventListener("click", () => location.href="/profile");

//   if (document.getElementById("feed")) {
//     loadFeed();
//     document.getElementById("feed").addEventListener("click", handleFeedClick);
//   }
// });

// document.querySelector(".sidebar li:nth-child(2)")
//   ?.addEventListener("click", () => {
//     document.getElementById("searchInput").style.display = "block";
//   });

// document.getElementById("searchInput")
//   ?.addEventListener("input", async e => {
//     const q = e.target.value;
//     const res = await authFetch(`/api/search?q=${q}`);
//     const users = await res.json();

//     searchResults.innerHTML = users
//       .map(u => `<div class="search-user">@${u.username}</div>`)
//       .join("");
//   });


// function authFetch(url, options = {}) {
//   return fetch(url, {
//     ...options,
//     headers: {
//       "Content-Type": "application/json",
//       "Authorization": "Bearer " + localStorage.getItem("token")
//     }
//   });
// }

// /* ================= FEED ================= */

// async function loadFeed() {
//   const res = await authFetch("/api/feed");
//   const posts = await res.json();
//   const feed = document.getElementById("feed");
//   feed.innerHTML = "";

//   if (posts.length === 0) {
//     feed.innerHTML = "<p style='text-align:center'>No posts yet</p>";
//     return;
//   }

//   posts.forEach(p => {
//     feed.insertAdjacentHTML("beforeend", `
//       <div class="post">
//         <div class="post-header">
//           <div class="post-user">
//             <img src="https://i.pravatar.cc/150?u=${p.user_id}">
//             <b>${p.username}</b>
//           </div>
//           <button class="follow-btn" 
//             data-user="${p.user_id}" 
//             data-following="${p.is_following}">
//             ${p.is_following ? "Following" : "Follow"}
//           </button>
//         </div>

//         <img src="${p.image_url}" class="post-img">

//         <div class="post-actions">
//           <button class="like-btn" data-post="${p.post_id}">❤️</button>
//           <span>${p.like_count} likes</span>
//           <p><b>${p.username}</b> ${p.caption}</p>
//         </div>
//       </div>
//     `);
//   });
// }

// /* ================= INTERACTIONS ================= */

// function handleFeedClick(e) {
//   if (e.target.classList.contains("like-btn")) {
//     likePost(e.target.dataset.post);
//   }

//   if (e.target.classList.contains("follow-btn")) {
//     const uid = e.target.dataset.user;
//     const following = e.target.dataset.following === "1";
//     following ? unfollow(uid) : follow(uid);
//   }
// }

// async function likePost(pid) {
//   await authFetch(`/api/like/${pid}`, { method: "POST" });
//   loadFeed();
// }

// async function follow(uid) {
//   await authFetch(`/api/follow/${uid}`, { method: "POST" });
//   loadFeed();
// }

// async function unfollow(uid) {
//   await authFetch(`/api/unfollow/${uid}`, { method: "POST" });
//   loadFeed();
// }

// /* ================= PROFILE ================= */

// async function loadProfile() {
//   const data = await (await authFetch("/api/profile")).json();

//   profilePhoto.src = `https://i.pravatar.cc/150?u=${data.user.id}`;
//   profileName.innerText = data.user.username;

//   postCount.innerText = data.stats.posts;
//   followerCount.innerText = data.stats.followers;
//   followingCount.innerText = data.stats.following;

//   const container = document.getElementById("profilePosts");
//   container.innerHTML = "";
//   data.posts.forEach(p => {
//     container.innerHTML += `<img src="${p.image_url}">`;
//   });
// }

// /* ================= ACTIONS ================= */

// function logout() {
//   localStorage.removeItem("token");
//   location.href = "/";
// }

// function goHome() {
//   location.href = "/dashboard";
// }


document.addEventListener("DOMContentLoaded", () => {
  const protectedPages = ["/dashboard", "/profile", "/create"];
  if (protectedPages.includes(location.pathname) && !localStorage.getItem("token")) {
    location.href = "/";
    return;
  }

  document.getElementById("logoutBtn")?.addEventListener("click", logout);
  document.getElementById("createBtn")?.addEventListener("click", () => location.href = "/create");
  document.getElementById("profileBtn")?.addEventListener("click", () => location.href = "/profile");

  // SEARCH BUTTON
  document.querySelector(".sidebar li:nth-child(2)")
    ?.addEventListener("click", () => {
      document.getElementById("searchInput").style.display = "block";
    });

  if (document.getElementById("feed")) {
    loadFeed();
    document.getElementById("feed").addEventListener("click", handleFeedClick);
  }

  if (document.getElementById("searchInput")) {
    document.getElementById("searchInput").addEventListener("input", searchUsers);
  }
});

/* ================= AUTH FETCH ================= */
function authFetch(url, options = {}) {
  return fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  });
}

/* ================= LOAD FEED ================= */
async function loadFeed() {
  const res = await authFetch("/api/feed");
  const posts = await res.json();

  const feed = document.getElementById("feed");
  feed.innerHTML = "";

  if (posts.length === 0) {
    feed.innerHTML = "<p style='text-align:center'>No posts yet</p>";
    return;
  }

  posts.forEach(p => {
    feed.insertAdjacentHTML("beforeend", `
      <div class="post">
        <div class="post-header">
          <div class="post-user">
            <img src="https://i.pravatar.cc/150?u=${p.user_id}">
            <b>${p.username}</b>
          </div>

          <button 
            class="follow-btn"
            data-user="${p.user_id}"
            data-following="${p.is_following}">
            ${p.is_following ? "Following" : "Follow"}
          </button>
        </div>

        <img src="${p.image_url}" class="post-img">

        <div class="post-actions">
          <button class="like-btn" data-post="${p.post_id}">❤️</button>
          <span>${p.like_count} likes</span>

          <p><b>${p.username}</b> ${p.caption}</p>

          <!-- COMMENT INPUT -->
          <div class="comments">
            <input 
              placeholder="Add a comment..."
              onkeydown="if(event.key==='Enter') addComment(${p.post_id}, this)">
          </div>
        </div>
      </div>
    `);
  });
}

/* ================= FEED CLICK HANDLER ================= */
function handleFeedClick(e) {
  if (e.target.classList.contains("like-btn")) {
    likePost(e.target.dataset.post);
  }

  if (e.target.classList.contains("follow-btn")) {
    const uid = e.target.dataset.user;
    const following = e.target.dataset.following === "1";
    following ? unfollow(uid) : follow(uid);
  }
}

/* ================= ACTIONS ================= */
async function likePost(pid) {
  await authFetch(`/api/like/${pid}`, { method: "POST" });
  loadFeed();
}

async function follow(uid) {
  await authFetch(`/api/follow/${uid}`, { method: "POST" });
  loadFeed();
}

async function unfollow(uid) {
  await authFetch(`/api/unfollow/${uid}`, { method: "POST" });
  loadFeed();
}

/* ================= COMMENTS ================= */
async function addComment(postId, input) {
  if (!input.value.trim()) return;

  await authFetch(`/api/comment/${postId}`, {
    method: "POST",
    body: JSON.stringify({ text: input.value })
  });

  input.value = "";
  loadFeed();
}

/* ================= PROFILE ================= */
async function loadProfile() {
  const data = await (await authFetch("/api/profile")).json();

  profilePhoto.src = `https://i.pravatar.cc/150?u=${data.user.id}`;
  profileName.innerText = data.user.username;

  postCount.innerText = data.stats.posts;
  followerCount.innerText = data.stats.followers;
  followingCount.innerText = data.stats.following;

  const container = document.getElementById("profilePosts");
  container.innerHTML = "";

  data.posts.forEach(p => {
    container.innerHTML += `
      <div class="profile-post">
        <img src="${p.image_url}">
        <div class="post-meta">
          ❤️ ${p.like_count} &nbsp;&nbsp; 💬 ${p.comment_count}
        </div>
      </div>
    `;
  });
}

/* ================= SEARCH ================= */
async function searchUsers(e) {
  const q = e.target.value;
  const res = await authFetch(`/api/search?q=${q}`);
  const users = await res.json();

  const box = document.getElementById("searchResults");
  box.innerHTML = users.map(
    u => `<div class="search-user">@${u.username}</div>`
  ).join("");
}

/* ================= NAV ================= */
function logout() {
  localStorage.removeItem("token");
  location.href = "/";
}

function goHome() {
  location.href = "/dashboard";
}
