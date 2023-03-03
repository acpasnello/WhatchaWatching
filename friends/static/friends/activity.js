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
<<<<<<< HEAD
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>.<br>
=======
            <a href="/watching/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>.<br>
>>>>>>> 586772be6bba14d659d948b3dafac54f3713dd03
            <b>${activity.rating}</b>: "${activity.review}"
        </div>`
    }
    else if (activity.action == "rated") {
        newDiv.innerHTML = 
        `<div>
<<<<<<< HEAD
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>: <b>${activity.rating}</b>
=======
            <a href="/watching/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>: <b>${activity.rating}</b>
>>>>>>> 586772be6bba14d659d948b3dafac54f3713dd03
        </div>`
    }
    else if (activity.action == "added") {
        newDiv.innerHTML = 
        `<div>
<<<<<<< HEAD
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.listitem}</a> to their list, <a href="${activity.listlink}">${activity.list}</a>.
=======
            <a href="/watching/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.listitem}</a> to their list, <a href="${activity.listlink}">${activity.list}</a>.
>>>>>>> 586772be6bba14d659d948b3dafac54f3713dd03
        </div>`
    }
    else if (activity.action == "watched") {
        newDiv.innerHTML = 
        `<div>
<<<<<<< HEAD
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="#" class="browseList">${activity.listitem}.
=======
            <a href="/watching/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="#" class="browseList">${activity.listitem}.
>>>>>>> 586772be6bba14d659d948b3dafac54f3713dd03
        </div>`
    }
    else if (activity.action == "created") {
        newDiv.innerHTML = 
        `<div>
<<<<<<< HEAD
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} a new list, <a href="#">${activity.list}</a>.
=======
            <a href="/watching/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} a new list, <a href="#">${activity.list}</a>.
>>>>>>> 586772be6bba14d659d948b3dafac54f3713dd03
        </div>`
    }
    
    newDiv.style.borderStyle = "none none solid none";
    newDiv.style.borderWidth = "1px";
    newDiv.style.borderColor = "#A9A9A9";
    displayDiv.appendChild(newDiv)
}