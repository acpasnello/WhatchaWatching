document.addEventListener("DOMContentLoaded", function () {
    var display = document.getElementById("activity-display");
    fetch("/watching/community/activity")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            for (const element of data) {
                activityBlock(element, display);
                console.log(element)
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});

function activityBlock(activity, displayDiv) {
    var newDiv = document.createElement("div");
    if (activity.action == "reviewed") {
        newDiv.innerHTML = `
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>. - ${activity.when.toLocaleString()}<br>
            <b>${activity.rating}</b>: "${activity.review}"
        `;
    } else if (activity.action == "rated") {
        newDiv.innerHTML = `
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.name}</a>: <b>${activity.rating}</b> - ${activity.when}
        `;
    } else if (activity.action == "added") {
        newDiv.innerHTML = `
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.listitem}</a> to their list, <a href="${activity.link}" class="browseList">${activity.list}</a>. - ${activity.when}
        `;
    } else if (activity.action == "watched") {
        newDiv.innerHTML = `
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} <a href="${activity.medialink}" class="browseList">${activity.listitem}</a> - ${activity.when}.
        `;
    } else if (activity.action == "created") {
        newDiv.innerHTML = `
            <a href="/watching/community/profile/${activity.userID}" class="friendsresult">${activity.user}</a> ${activity.action} a new list, <a href="${activity.link}" class="homelistlink">${activity.list}</a> - ${activity.when}.
        `;
    }

    newDiv.style.borderStyle = "none none solid none";
    newDiv.style.borderWidth = "1px";
    newDiv.style.borderColor = "#A9A9A9";
    displayDiv.appendChild(newDiv);
}
