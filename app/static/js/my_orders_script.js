function updateOrder(orderId, action) {
    fetch(`/update-order/${orderId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: action }),
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById(`status-${orderId}`).innerText = action;
      }
    });
  }
  