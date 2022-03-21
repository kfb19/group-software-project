// Posts likes to the server and updates the html (Authors: Michael Hills, Tomas Premoli)
function postData(id) {
    let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var req = new XMLHttpRequest();
    var url = "/likes/";
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Once POST is successful update like counter and button
            button = document.getElementById("button-" + id);
            count = parseInt(document.getElementById("num-" + id).innerHTML);

            if (button.innerHTML == "Like") {
                document.getElementById("button-" + id).innerHTML = "Unlike";
                count++;
                document.getElementById("num-" + id).innerHTML = count;
            } else {
                document.getElementById("button-" + id).innerHTML = "Like";
                count--;
                document.getElementById("num-" + id).innerHTML = count;
            }
            count = document.getElementById("num-" + id).innerHTML;
        } else if (this.readyState == 4 && this.status != 200) {
            alert("!200");
        }
    };


    req.open("POST", url);
    req.setRequestHeader('X-CSRFToken', csrf)
    req.setRequestHeader("Content-Type", "text/plain");
    req.send(id);
}