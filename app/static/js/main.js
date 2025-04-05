// Обработка быстрых кнопок количества
document.addEventListener("DOMContentLoaded", function () {
  // Установка количества и автоматического расчета суммы
  const quantityButtons = document.querySelectorAll(".quantity-button");
  quantityButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const quantity = this.getAttribute("data-value");
      const price = quantity * 180; // 180 - цена за бутыль
      document.getElementById("quantity").value = quantity;
      document.getElementById("amount").value = price.toFixed(2);
    });
  });

  // Обработка кнопок типа оплаты
  const paymentButtons = document.querySelectorAll(".payment-type-button");
  paymentButtons.forEach((button) => {
    button.addEventListener("click", function () {
      paymentButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");
      document.getElementById("payment_type").value =
        this.getAttribute("data-value");
    });
  });
});

function deleteRecord(id) {
  if (confirm("Вы уверены, что хотите удалить запись?")) {
    fetch(`/delivery/delete/${id}`, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // Удаляем запись из DOM или обновляем таблицу
          document.getElementById(`record-${id}`).remove();
          // Или можно обновить всю таблицу
          // updateDeliveryTable();
        } else {
          alert("Ошибка: " + data.message);
        }
      })
      .catch((error) => console.error("Error:", error));
  }
}
