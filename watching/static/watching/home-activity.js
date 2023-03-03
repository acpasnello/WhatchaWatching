document.addEventListener('DOMContentLoaded', function() {
    var display = document.getElementById("activity-display")
    fetch("/watching/community/activity")
    .then((response) => {
        // console.log(response)
        return response.json()
    })
    .then((data) => {
        for (const element of data) {
            // console.log(element)
            activityBlock(element, display)
        }
    })
    .catch((error) => {
        console.error('Error:', error)
    })
})

function activityBlock(activity, displayDiv) {
    var newDiv = document.createElement('div')
    if (activity.action == "reviewed") {
        newDiv.innerHTML = 
        `<div>
            <img class="missingposter" data-id="${activity.id}">
            <a href="/watching/profile/${activity.userID}" class="homelistlink">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="homelistlink">${activity.name}</a>.<br>
            <b>${activity.rating}</b>: "${activity.review}"
        </div>`
    }
    else if (activity.action == "rated") {
        newDiv.innerHTML = 
        `<div>
            <a href="/watching/profile/${activity.userID}" class="homelistlink">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="homelistlink">${activity.name}</a>: <b>${activity.rating}</b>
        </div>`
    }
    else if (activity.action == "added") {
        newDiv.innerHTML = 
        `<div>
            <a href="/watching/profile/${activity.userID}" class="homelistlink">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="homelistlink">${activity.listitem}</a> to their list, <a href="${activity.listlink}" class="homelistlink">${activity.list}</a>.
        </div>`
    }
    else if (activity.action == "watched") {
        newDiv.innerHTML = 
        `<div>
            <a href="/watching/profile/${activity.userID}" class="homelistlink">${activity.user}</a> ${activity.action} <a href="#" class="homelistlink">${activity.listitem}.
        </div>`
    }
    else if (activity.action == "created") {
        newDiv.innerHTML = 
        `<div>
            <a href="/watching/profile/${activity.userID}" class="homelistlink">${activity.user}</a> ${activity.action} a new list, <a href="#" class="homelistlink">${activity.list}</a>.
        </div>`
    }
    
    newDiv.style.borderStyle = "none none solid none";
    newDiv.style.borderWidth = "1px";
    newDiv.style.borderColor = "#A9A9A9";
    displayDiv.appendChild(newDiv)
}