

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



var annotation_string = "";
var index = 0;

function handleClick() {
    index++;
    
    var progressbar = document.getElementById("progressbar");
    var percent = (index/links.length)*100;
    progressbar.style = "width: " + percent.toString() + "%";
    progressbar.width = percent;
    if (index >= links.length || index >=10) {
        document.location.href = "http://localhost:8000/" +'edit/' + annotation_string;
    } else {
        var iframe = document.getElementById("iframe");
        iframe.src = "/url" + index,toString();
        if (labels != null && labels[index] == 0) {
            if (labels[index - 1] != 0) { //labels should be reversed, last homepage was green
                var not_homepage_button = document.getElementById('notHomepage');
                not_homepage_button.classList.remove('btn-primary');
                not_homepage_button.classList.add('btn-success');
                var homepage_button = document.getElementById('homepage');
                homepage_button.classList.remove('btn-success');
                homepage_button.classList.add('btn-primary');
            }
        } else if (labels != null) {
            if (labels[index - 1] != 1) {
                var homepage_button = document.getElementById('homepage');
                homepage_button.classList.remove('btn-primary');
                homepage_button.classList.add('btn-success');
                var not_homepage_button = document.getElementById('notHomepage');
                not_homepage_button.classList.remove('btn-success');
                not_homepage_button.classList.add('btn-primary');
            }
        }
    }
}



/*document.getElementById('notHomepage').addEventListener("click", function() {
    annotation_string = annotation_string.concat('0');
    handleClick();
});

document.getElementById('homepage').addEventListener("click", function() {
    annotation_string = annotation_string.concat('1');
    handleClick();
});*/

document.getElementById('submit_annotation').addEventListener("click", function(event) {
    var res = document.getElementsByClassName("ezO2md");
    annotation_string = "";
    for (var i = 0; i < res.length; i++) {
        if (res[i].style.background == 'green') {
            annotation_string += '1';
        } else {
            annotation_string += '0';
        }
    }
    document.location.href = "http://localhost:8000/" +'edit/' + annotation_string;
})

window.onload = function() {
    var res = document.getElementsByClassName("ezO2md");
    if (labels != null) {
        for (var i = 0; i < labels.length; i++) {
            if (labels[i] == 1) {
                res[i].style.background = 'green';
            }
        }
    }
    
    res[0].addEventListener("click", function(event) {
        var currentDiv = res[0];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
    })
    
    res[1].addEventListener("click", function(event) {
        var currentDiv = res[1];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[2].addEventListener("click", function(event) {
    var currentDiv = res[2];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[3].addEventListener("click", function(event) {
    var currentDiv = res[3];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
    })
res[4].addEventListener("click", function(event) {
    var currentDiv = res[4];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[5].addEventListener("click", function(event) {
    var currentDiv = res[5];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[6].addEventListener("click", function(event) {
    var currentDiv = res[6];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[7].addEventListener("click", function(event) {
    var currentDiv = res[7];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[8].addEventListener("click", function(event) {
    var currentDiv = res[8];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[9].addEventListener("click", function(event) {
    var currentDiv = res[9];
        if (currentDiv.style.background == 'green') {
            currentDiv.style.background = 'none';
        } else {
            currentDiv.style.background = 'green';
        }
})
res[0].addEventListener("dblclick", function(event) {
    window.open(links[0]);
    //alert("hello");
})
res[1].addEventListener("dblclick", function(event) {
    window.open(links[1]);
    //alert("hello");
})
res[2].addEventListener("dblclick", function(event) {
    window.open(links[2]);
    //alert("hello");
})
res[3].addEventListener("dblclick", function(event) {
    window.open(links[3]);
    //alert("hello");
})
res[4].addEventListener("dblclick", function(event) {
    window.open(links[4]);
    //alert("hello");
})
res[5].addEventListener("dblclick", function(event) {
    window.open(links[5]);
    //alert("hello");
})
res[6].addEventListener("dblclick", function(event) {
    window.open(links[6]);
    //alert("hello");
})
res[7].addEventListener("dblclick", function(event) {
    window.open(links[7]);
    //alert("hello");
})
res[8].addEventListener("dblclick", function(event) {
    window.open(links[8]);
    //alert("hello");
})
res[9].addEventListener("dblclick", function(event) {
    window.open(links[9]);
    //alert("hello");
})
}

/*window.onbeforeunload = function(){
    return 'Are you sure you want to leave?';
};*/