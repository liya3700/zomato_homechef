function updateOrder(orderId, status) {
  console.log("OrderId" + status)
  const formData = new FormData();
  formData.append("status", status)
  fetch(`/update-order/${orderId}`, {
    method: 'POST',
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        location.reload();
        document.getElementById(`status-${orderId}`).innerText = status;
      }
    });
}
