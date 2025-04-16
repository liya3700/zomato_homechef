document.addEventListener("DOMContentLoaded", function () {
    loadItems();
});

function loadItems() {
    fetch("/get_all_items")
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let grid = document.getElementById("itemsGrid");
            grid.innerHTML = "";

            data.data.forEach(request => {
                let card = document.createElement("div");
                card.classList.add("request-card");

                card.innerHTML = `
                    <img src="${profilePicUrl + request.image}" alt="${request.name}" class="card-image">
                    <h3>${request.name}</h3>
                    <p>${request.desc}</p>
                    <p>€${request.price}</p>
                    <button class="delete-button">Delete</button>
                `;
                card.onclick = function () {
                    window.location.href = "/request_detail/" + request.id;
                };
                grid.appendChild(card);
                const deleteBtn = card.querySelector('.delete-button');
                deleteBtn.addEventListener('click', (event) => {
                    event.stopPropagation();
                    const confirmDelete = confirm(`Are you sure you want to delete "${request.name}"?`);
                    if (confirmDelete) {
                        fetch(`/delete_item/${request.id}`)
                            .then(response => {
                                if (response.ok) {
                                    card.remove();
                                    location.reload();
                                } else {
                                    console.error('Failed to delete', error);
                                }
                            })
                            .catch(error => console.error('Error deleting:', error));
                    }
                });
            });


            let addItemCard = document.createElement("div");
            addItemCard.classList.add("request-card", "add-item-card");
            addItemCard.innerHTML = `
                <button class="add-item-button">Add Item</button>
            `;
            addItemCard.onclick = function () {
                window.location.href = "/addItem";
            };
            grid.appendChild(addItemCard);

        })
        .catch(error => console.error("Error loading foods:", error));
}
