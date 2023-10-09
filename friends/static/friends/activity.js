document.addEventListener("DOMContentLoaded", function () {
    var display = document.getElementById("activity-display");
    fetch("/watching/community/activity")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            for (const element of data) {
                activityBlock(element, display);
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});

function activityBlock(activity, displayDiv) {
    var newDiv = document.createElement("div");
    if (activity.action == "reviewed") {
        newDiv.innerHTML = `<div>
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>. - ${activity.when.toLocaleString()}<br>
            <b>${activity.rating}</b>: "${activity.review}"
        </div>`;
    } else if (activity.action == "rated") {
        newDiv.innerHTML = `<div>
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>: <b>${activity.rating}</b> - ${activity.when}
        </div>`;
    } else if (activity.action == "added") {
        newDiv.innerHTML = `<div>
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.listitem}</a> to their list, <a href="${activity.listlink}">${activity.list}</a>. - ${activity.when}
        </div>`;
    } else if (activity.action == "watched") {
        newDiv.innerHTML = `<div>
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="#" class="browseList">${activity.listitem} - ${activity.when}.
        </div>`;
    } else if (activity.action == "created") {
        newDiv.innerHTML = `<div>
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} a new list, <a href="#" class="homelistlink">${activity.list}</a> - ${activity.when}.
        </div>`;
    }

    newDiv.style.borderStyle = "none none solid none";
    newDiv.style.borderWidth = "1px";
    newDiv.style.borderColor = "#A9A9A9";
    displayDiv.appendChild(newDiv);
}
