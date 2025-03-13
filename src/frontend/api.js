const API_BASE = "http://127.0.0.1:1234"; // адрес вашего сервера (без /api)

async function getAllPosts() {
  try {
    const response = await fetch(`${API_BASE}/api/posts`);
    if (!response.ok) throw new Error("Ошибка при загрузке постов");
    const posts = await response.json();
    renderPosts(posts);
  } catch (error) {
    console.error(error);
    alert("Не удалось загрузить посты");
  }
}

function renderPosts(posts) {
  const postsContainer = document.getElementById("postsContainer");
  if (!postsContainer) return;
  postsContainer.innerHTML = "";
  
  posts.forEach(post => {
    const postCard = document.createElement("div");
    postCard.className = "post-card";

    let tags = "";
    try {
      tags = post[6] ? JSON.parse(post[6]).join(", ") : ""; 
    } catch (e) {
      console.error("Ошибка при обработке тегов:", e);
    }

    // Если API возвращает массивы, обращаемся по индексам
    // Если возвращает объекты, используйте post.username, post.title и т.д.
    // Предположим, что API возвращает массивы, как в вашем предыдущем ответе:
    postCard.innerHTML = `
      <h3>by ${post[2]}</h3>
      <h3>${post[3]}</h3>
      <p>${post[4]}</p>
      <small>Категория: ${post[5]} | Теги: ${tags}</small>
    `;
    postsContainer.appendChild(postCard);
  });
}

async function createPost(postData) {
  try {
    const response = await fetch(`${API_BASE}/api/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(postData)
    });
    if (!response.ok) throw new Error("Ошибка при создании поста");
    return await response.json();
  } catch (error) {
    console.error(error);
    alert("Не удалось создать пост");
  }
}

// Другие функции (loginUser, registerUser, getUser) остаются без изменений
