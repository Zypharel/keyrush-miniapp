// Пример текущего пользователя — меняешь id, name и роль для теста
const currentUser = {
  id: 12345,
  username: "zypharel",
  role: "buyer" // "buyer", "seller", "moderator", "admin", "owner"
};

// Минимальная комиссия платформы (в %)
const platformCommissionPercent = 10;

// Список пользователей (продавцов), для примера
const users = [
  { id: 111, username: "seller_ivan", role: "seller", rating: 4.8 },
  { id: 222, username: "seller_masha", role: "seller", rating: 4.3 },
  { id: 12345, username: "zypharel", role: "buyer", rating: 0 }
];

// Пример товаров — массив объектов
let marketplaceItems = [
  {
    id: 1,
    sellerId: 111,
    name: "GTA V Premium",
    description: "Премиум ключ Rockstar Games, активируется в Steam.",
    price: 1500,
    currency: "TON",
    keys: ["KEY1-1234-5678", "KEY1-2345-6789"],
    soldKeys: [], // проданные ключи
    complaints: 0
  },
  {
    id: 2,
    sellerId: 222,
    name: "The Witcher 3 Complete",
    description: "Полное издание с DLC, ключ Steam.",
    price: 1200,
    currency: "TON",
    keys: ["WITCHER3-1-2345", "WITCHER3-2-3456", "WITCHER3-3-4567"],
    soldKeys: [],
    complaints: 1
  }
];

// Заглушка: функция имитации покупки (автоматическая выдача ключа)
function buyItem(itemId) {
  const item = marketplaceItems.find(i => i.id === itemId);
  if (!item) return null;

  if (item.keys.length === 0) {
    alert("К сожалению, ключи для этого товара закончились.");
    return null;
  }
  const key = item.keys.shift();  // берём первый свободный ключ
  item.soldKeys.push(key);
  return key;
}
