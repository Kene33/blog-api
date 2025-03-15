const API_BASE = "http://127.0.0.1:4000"; // адрес вашего сервера (без /api)

async function getAllPosts() {
  try {
    const response = await fetch(`${API_BASE}/api/posts`, {
      method: "GET",
      credentials: "include"
    });
    if (!response.ok) throw new Error("Ошибка при загрузке постов");
    const posts = await response.json();
    renderPosts(posts);
  } catch (error) {
    console.error(error);
    alert("Не удалось загрузить посты");
  }
}

function timeAgo(dateString) {
  const now = new Date();
  const date = new Date(dateString);
  const diffInSeconds = Math.floor((now - date) / 1000);

  const seconds = diffInSeconds;
  const minutes = Math.floor(diffInSeconds / 60);
  const hours = Math.floor(diffInSeconds / 3600);
  const days = Math.floor(diffInSeconds / 86400);
  const months = Math.floor(diffInSeconds / 2592000); // 30 days
  const years = Math.floor(diffInSeconds / 31536000); // 365 days

  // Если пост был создан больше года назад, выводим полную дату
  if (years > 0) {
      return date.toLocaleString(); // Отобразится как "14.03.2025, 19:18:27" или в зависимости от локали
  }
  // Если пост был создан несколько месяцев назад, выводим сколько месяцев назад
  else if (months > 0) {
      return `${months} месяц${months === 1 ? '' : 'a'} назад`;
  }
  // Если пост был создан меньше месяца назад, выводим количество дней
  else if (days > 0) {
      return `${days} день${days === 1 ? '' : 'я'} назад`;
  }
  // Для секунд и минут
  else if (hours > 0) {
      return `${hours} час${hours === 1 ? '' : 'а'} назад`;
  } else if (minutes > 0) {
      return `${minutes} минут${minutes === 1 ? '' : 'ы'} назад`;
  } else {
      return `${seconds} секунд${seconds === 1 ? '' : 'ы'} назад`;
  }
}

// Асинхронная функция для рендеринга постов
async function renderPosts(posts) {
  const postContainer = document.getElementById("postContainer");
  postContainer.innerHTML = "";

  // Сортировка постов по дате (сначала новые)
  //posts.sort((a, b) => new Date(b[5] || 0) - new Date(a[5] || 0));
  if (!posts || posts.length === 0) {
    postContainer.innerHTML = "<p style='text-align: center; color: gray;'>Постов пока нет.</p>";
    return;
  }

  posts.forEach((post) => {
    // const [title, username, content, category, tags, createdAtRaw] = post;
    const createdAtRaw = post[6]
    // Преобразуем raw дату в строку времени
    const createdAtText = createdAtRaw ? timeAgo(createdAtRaw) : "Дата неизвестна";
    const tags = post[5];
    const postCard = document.createElement("div");
    postCard.classList.add("post");
    postCard.innerHTML = `
      <h3 style="font-size: 0.8em;">
        <span style="color: #888;">by </span>
        <span>${post[1]}</span>
      </h3>
      <h3>${post[2]}</h3>
      <p>${post[3]}</p>
      <small>Категория: ${post[4]} | Теги: ${Array.isArray(tags) ? tags.join(", ") : "Нет тегов"}</small>
      <br>
      <small style="color: gray;">${createdAtText}</small>
    `;
    postContainer.appendChild(postCard);
  });
}

async function createPost(postData) {
  try {
    const response = await fetch(`${API_BASE}/api/posts`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(postData)
    });
    
    if (response.status === 401) {
      // Если сервер вернул 401, выводим сообщение о том, что пользователь не авторизован
      alert("Вы не вошли в аккаунт");
      return;
    }
    console.log(JSON.stringify(postData))
    if (!response.ok) throw new Error("Ошибка при создании поста");
    return await response.json();
  } catch (error) {
    console.error(error);
    alert("Не удалось создать пост");
  }
}


async function loginUser(userData) {
  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });
    const result = await response.json();
    if (result.ok && result.access_token) {
      localStorage.setItem("access_token", result.access_token);
      // Перенаправляем пользователя, например, на профиль
      window.location.href = "profile.html";
    }
    return result;
  } catch (error) {
    console.error(error);
    return { status: "error", detail: "Ошибка запроса" };
  }
}

// Функция для регистрации пользователя
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

// Функция для получения данных пользователя по id
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