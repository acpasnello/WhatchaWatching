document.addEventListener('DOMContentLoaded', function () {
    var waiting = document.querySelectorAll("img.missingposter");

    waiting.forEach(function(img) {
        id = img.dataset.id;
        path = getposterpath(id)
        img.src = path
    })
})

function getposterpath(activityID) {
    data = {'id': activityID}
    fetch("/getposterpath", {
        method: "POST",
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(function(data) {
        console.log(data)
        return data["url"]
    })
}