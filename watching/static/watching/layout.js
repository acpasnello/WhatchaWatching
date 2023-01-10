document.addEventListener('DOMContentLoaded', function() {
  var lazyloadImages = document.querySelectorAll("img.lazy");    
  var lazyloadThrottleTimeout;
  
  function lazyload () {
    if(lazyloadThrottleTimeout) {
      clearTimeout(lazyloadThrottleTimeout);
    }    
    
    lazyloadThrottleTimeout = setTimeout(function() {
        var scrollTop = window.pageYOffset;
        lazyloadImages.forEach(function(img) {
            if(img.offsetTop < (window.innerHeight + scrollTop)) {
              img.src = img.dataset.src;
              img.classList.remove('lazy');
            }
        });
        if(lazyloadImages.length == 0) { 
          document.removeEventListener("scroll", lazyload);
          window.removeEventListener("resize", lazyload);
          window.removeEventListener("orientationChange", lazyload);
        }
    }, 20);
  }
  
  document.addEventListener("scroll", lazyload);
  // window.addEventListener("resize", lazyload);
  // window.addEventListener("orientationChange", lazyload);

  // let sInput = document.querySelector('#search')
  // sInput.addEventListener("keydown", function(){
  //   if (!event.ctrlKey && !event.altKey && !event.metaKey && !event.shiftKey) {
  //     console.log(event.key)
  //     let query = sInput.value
  //     console.log(query)
  //     let data = {query: query}
  //     const oldsearch = document.getElementById("searchtop5")
  //     if (oldsearch != null) {
  //       oldsearch.remove();
  //     }
  //     if (query != '') {
  //       getSearch(data)
  //       .then((data) => {
  //         console.log(data)
  //         // Display first 5 results under search input
  //         let top5 = []
  //         let top5div = document.createElement("div")
  //         top5div.id = "searchtop5"
  //         let title = null;
  //         for (i = 0; i < 5; ) {
  //           if (data[i]["media_type"] == "person") {
  //             continue
  //           } else if (data[i]["media_type"] == "movie") {
  //             title = data[i]["title"];
  //             i++;
  //           } else if (data[i]["media_type"] == "tv") {
  //             title = data[i]["original_name"];
  //             i++;
  //           }
  //           console.log(title)
  //           top5[i] = document.createElement("div")
  //           top5[i].innerHTML = `<h4>${title}</h4>`
  //           console.log(top5[i])
  //           top5[i].style.color = "white";
  //           top5div.appendChild(top5[i])
  //         }
  //
  //         // top5div.innerHTML = ``
  //         document.querySelector('#searchform').appendChild(top5div)
  //       })
  //       .catch((error) => {
  //         console.error('Problem with fetch: ', error)
  //       });
  //     }
  //   } else {
  //     event.stopPropagation()
  //   }
  // })

})

async function getSearch(query){
  let csrf = getCookie('csrftoken')
  const response = await fetch("/search", {
    method: 'POST',
    credentials: 'same-origin',
    headers: {"X-CSRFToken": csrf,
        'Content-Type': 'application/json:charset=utf-8'
      },
    body: JSON.stringify(query)
  });
  if (!response.ok) {
    throw new Error('Network response was not ok')
  }
  return response.json();
}

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
