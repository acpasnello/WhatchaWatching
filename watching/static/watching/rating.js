var popup = document.getElementById("rating-popup")
var btn = document.getElementById("add-rating-button")
var cancel = document.getElementById("cancel-rating-button")
var submit = document.getElementById("submit-rating")
var medianame = document.getElementById("subject-name").value
var subjecttype = document.getElementById("subject-type").value

btn.onclick = function(event) {
    event.preventDefault()
    // popup.style.top = btn.offsetTop + btn.clientHeight
    popup.style.display = 'block'
}

cancel.onclick = function() {
    popup.style.display = 'none'
    return false;
}

async function submitRating(subject, rating, review=null) {
    var csrf = getCookie('csrftoken')
    let data = {
            "subject": subject,
            "subjectname": medianame,
            "rating": rating,
            "review": review,
            "subjecttype": subjecttype
        };
    console.log(JSON.stringify(data))
    var response = await fetch("/watching/community/addrating", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    }); // End of fetch
    var result = await response.json()
    console.log(result)
    return result
} // End of function

submit.onclick = function(event) {
    event.preventDefault()
    var subject = document.getElementById("id").value
    var rating = document.getElementById("rating").value
    var review = document.getElementById("review").value
    if (review != null) {
        // can just call the submitRating function here, and use .then to handle response, instead of assigning to variable
        submitRating(subject, rating, review)
        .then((data) => {
            if (data.success) {
                popup.style.display = 'none'
                btn.innerText = data.message
            }
            else {
                popup.innerHTML = '<h4>Rating submission failed.</h4>'
            }
        })
    }
    else {
        var response = submitRating(subject, rating)
    }
}
// 'use strict';

// const e = React.createElement;

// class RatingPopup extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = { liked: false };
//   }

//   render() {
//     if (this.state.liked) {
//       return 'You liked this.';
//     }

//     return e(
//       'button',
//       { onClick: () => this.setState({ liked: true }) },
//       'Rate'
//     );
//   }
// }

// const domContainer = document.querySelector('#add-rating-button');
// const root = ReactDOM.createRoot(domContainer);
// root.render(e(RatingPopup));

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}