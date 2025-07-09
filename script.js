const marketplace = document.getElementById("marketplace");
const searchInput = document.getElementById("searchInput");

// Показываем список товаров (фильтр по названию)
function showItems(filter = "") {
  marketplace.innerHTML = ""; // очистка

  const filtered = marketplaceItems.filter(item =>
    item.name.toLowerCase().includes(filter.toLowerCase())
  );

  if (filtered.length === 0) {
    marketplace.innerHTML = "<p>Товары не найдены</p>";
    return;
  }

  filtered.forEach(item => {
    const seller = users.find(u => u.id === item.sellerId);
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h2>${item.name}</h2>
      <p class="description">${item.description}</p>
      <p class="price">${item.price} ${item.currency}</p>
      <p>Продавец: @${seller.username} (Рейтинг: ${seller.rating.toFixed(1)})</p>
      <button>Купить</button>
      <button class="complain-btn" style="background:#dc3545; margin-top:8px;">Проблемный товар</button>
    `;

    // Покупка
    card.querySelector("button").onclick = () => {
      if (currentUser.role === "buyer" || currentUser.role === "seller") {
        const key = buyItem(item.id);
        if (key) {
          alert(`Покупка успешна! Ваш ключ: ${key}`);
          // Тут можно добавить отправку уведомлений и обновление данных
          showItems(searchInput.value);
        }
      } else {
        alert("Только покупатели и продавцы могут совершать покупки.");
      }
    };

    // Жалоба
    card.querySelector(".complain-btn").onclick = () => {
      if (currentUser.role === "buyer" || currentUser.role === "moderator" || currentUser.role === "admin") {
        item.complaints++;
        alert("Жалоба отправлена. Модератор проверит.");
        // Тут можно отправлять жалобу в чат поддержки или в админку
      } else {
        alert("Недостаточно прав для жалобы.");
      }
    };

    marketplace.appendChild(card);
  });
}

searchInput.oninput = () => {
  showItems(searchInput.value);
};

window.onload = () => {
  showItems();
};
