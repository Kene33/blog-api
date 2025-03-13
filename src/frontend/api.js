// main.js

const API_BASE = "http://127.0.0.1:1234/api"; // Измените адрес, если необходимо

// Получить все посты
async function getAllPosts() {
  try {
    const response = await fetch(`${API_BASE}/posts`);
    if (!response.ok) throw new Error("Ошибка при загрузке постов");
    const posts = await response.json();
    renderPosts(posts);
  } catch (error) {
    console.error(error);
    alert("Не удалось загрузить посты");
  }
}

// Отрисовка постов
function renderPosts(posts) {
  const postsContainer = document.getElementById("postsContainer");
  if (!postsContainer) return;
  postsContainer.innerHTML = "";
  posts.forEach(post => {
    const postCard = document.createElement("div");
    postCard.className = "post-card";
    postCard.innerHTML = `
      <h3>${post.title}</h3>
      <p>${post.content}</p>
      <small>Категория: ${post.category} | Теги: ${post.tags ? post.tags.join(", ") : ""}</small>
      ${post.image_url ? `<img src="${API_BASE}${post.image_url}" alt="Post Image">` : ""}
    `;
    postsContainer.appendChild(postCard);
  });
}

// Создать пост
async function createPost(postData) {
  try {
    const response = await fetch(`${API_BASE}/posts`, {
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

// Авторизация
async function loginUser(userData) {
  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });
    return await response.json();
  } catch (error) {
    console.error(error);
    return { status: "error", detail: "Ошибка запроса" };
  }
}

// Регистрация
async function registerUser(userData) {
  try {
    const response = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });
    return await response.json();
  } catch (error) {
    console.error(error);
    return { status: "error", detail: "Ошибка запроса" };
  }
}

// Получение данных пользователя
async function getUser(userId) {
  try {
    const response = await fetch(`${API_BASE}/user/${userId}`);
    if (!response.ok) throw new Error("Ошибка при загрузке пользователя");
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}
