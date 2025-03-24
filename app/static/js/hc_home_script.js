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
                    <h3>${request.name} Needed</h3>
                    <p>${request.desc}</p>
                    <p>€${request.price}</p>
                `;
                card.onclick = function () {
                    window.location.href = "/request_detail/" + request.id;
                };
                grid.appendChild(card);
            });
        })
        .catch(error => console.error("Error loading blood requests:", error));
}
