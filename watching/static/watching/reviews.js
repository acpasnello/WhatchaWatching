document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById("reviews")) {
        id = document.getElementById("id").value
        reviewDiv = document.getElementById("reviews")
        url = `/watching/reviews/${id}`
        fetch(url)
        .then(response=>response.json())
        .then(data => {
            for (const element of data) {
                console.log(element)
                displayReview(element, reviewDiv)
            }
        })
        .catch((error) => {
            console.error('Error: ', error)
        })
    }
})

function displayReview(element, div) {
    newDiv = document.createElement("div")
    newDiv.className = "row"
    newDiv.innerHTML = 
    `
    <div class="details-review-userdisplay col-1">
        <a href="/watching/profile/${element.userID}">${element.user}</a>
    </div>
    <div class="details-review-content col">
        ${element.rating}<br>
        ${element.review}
    </div>
    `
    div.appendChild(newDiv)
}