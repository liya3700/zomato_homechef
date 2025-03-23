document.addEventListener("DOMContentLoaded", function () {
    loadItems();
});

// Function to Load Blood Requests Dynamically
function loadItems() {
    fetch("/get_all_chefs")
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let grid = document.getElementById("chefsGrid");
            grid.innerHTML = "";  // Clear previous entries

            data.data.forEach(request => {
                let card = document.createElement("div");
                card.classList.add("chefs-card");

                card.innerHTML = `
                    <img src="${profilePicUrl + request.profile_pic}" alt="${request.username}" class="card-image">
                    <h3>${request.username}</h3>
                    <p>${request.location}</p>
                `;
                card.onclick = function () {
                    window.location.href = `/getItemsByChefId/${request.id}`;
                };
                grid.appendChild(card);
            });
        })
        .catch(error => console.error("Error loading blood requests:", error));
}
