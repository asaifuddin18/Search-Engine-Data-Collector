
const links = JSON.parse(document.getElementById('links').textContent);
var labels = null;
var info = null;
var stats_local = null;
try {
    labels = JSON.parse(document.getElementById('labels').textContent);
} catch(error) {
}

try {
    stats_local = JSON.parse(document.getElementById('stats_local').textContent);
} catch(error) {
}

document.getElementById('submit_annotation').addEventListener("click", function(event) {
    var res = document.getElementsByClassName("ezO2md");
    annotation_string = "";
    for (var i = 1; i < res.length + 1; i++) {
        var y = document.getElementById("y" + i.toString());
        var n = document.getElementById("n" + i.toString());
        if (y.classList.contains("btn-success")) {
            annotation_string += "1";
        } else if (n.classList.contains("btn-danger")) {
            annotation_string += "0";
        } else {
            alert("Please mark search result #" + i.toString() + " as Homepage or Not Homepage before continuing.");
            return
        }
    }
    document.location.href = "/" +'edit/' + annotation_string;
})

window.onload = function() {
    var res = document.getElementsByClassName("ezO2md");
    for (var i = 1; i < res.length + 1; i++) {
        document.getElementById("y" + i.toString()).addEventListener("click", function(event) {
            event.target.classList.add("btn-success");
            var num = event.target.id.slice(1);
            var n = document.getElementById("n" + num);
            if (n.classList.contains("btn-danger")) {
                n.classList.remove("btn-danger");
            }
        })
        document.getElementById("n" + i.toString()).addEventListener("click", function(event) {
            event.target.classList.add("btn-danger");
            var num = event.target.id.slice(1);
            var n = document.getElementById("y" + num);
            if (n.classList.contains("btn-success")) {
                n.classList.remove("btn-success");
            }
        })
    }

    if (labels != null) {
        for (var i = 0; i < labels.length; i++) {
            if (labels[i] == 1) {
                document.getElementById("y" + (i+1).toString()).classList.add("btn-success");
            } else {
                document.getElementById("n" + (i+1).toString()).classList.add("btn-danger");
            }
        }
    }
}

/*window.onbeforeunload = function(){
    return 'Are you sure you want to leave?';
};*/