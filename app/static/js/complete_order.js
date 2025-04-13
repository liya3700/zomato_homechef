document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("orderForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();


        const chefId = form.querySelector("button").dataset.chefId;
        const foodId = form.querySelector("button").dataset.id;
        const address = document.getElementById("address").value;
        const quantity = document.getElementById("quantity").value;
        const mobile = document.getElementById("mobile").value;

        console.log("ChefId:" + chefId)
        console.log("FoodId:" + foodId)

        const formData = new FormData();
        formData.append("chef_id", chefId)
        formData.append("item_id", foodId)
        formData.append("address", address);
        formData.append("quantity", quantity);
        formData.append("mobile", mobile);

        fetch('/place-order', {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                const message = document.getElementById("successMsg");
                if (data.success) {
                    message.textContent = "Order placed!";
                    message.style.color = "green";
                    document.getElementById("orderForm").reset();
                } else {
                    message.textContent = "Error placing order.";
                    message.style.color = "red";
                }
            })
            .catch(error => console.error("Error:", error));
    });
});