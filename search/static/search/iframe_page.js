const links = JSON.parse(document.getElementById('links').textContent);
var labels = null;
try {
    labels = JSON.parse(document.getElementById('labels').textContent);
} catch(error) {
}
var annotation_string = "";
var index = 0;
document.getElementById('notHomepage').addEventListener("click", function() {
        index++;
        var progressbar = document.getElementById("progressbar");
        var percent = (index/links.length)*100;
        progressbar.style = "width: " + percent.toString() + "%";
        progressbar.width = percent;
        annotation_string = annotation_string.concat('0');
        if (index >= links.length) {
            document.location.href = "http://localhost:8000/" +'edit/' + annotation_string;
        } else {
            var iframe = document.getElementById("iframe");
            iframe.src = links[index];
            if (labels != null && labels[index] == 0) {
                if (labels[index - 1] != 0) { //labels should be reversed, last homepage was green
                    var not_homepage_button = document.getElementById('notHomepage');
                    not_homepage_button.classList.remove('btn-primary');
                    not_homepage_button.classList.add('btn-success');
                    var homepage_button = document.getElementById('homepage');
                    homepage_button.classList.remove('btn-success');
                    homepage_button.classList.add('btn-primary');
                }
            } else {
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
});

document.getElementById('homepage').addEventListener("click", function() {
    index++;
    var progressbar = document.getElementById("progressbar");
    var percent = (index/links.length)*100;
    progressbar.style = "width: " + percent.toString() + "%";
    progressbar.width = percent;
    annotation_string = annotation_string.concat('1');
    if (index >= links.length) {
        document.location.href = "http://localhost:8000/" +'edit/' + annotation_string;
    } else {
        var iframe = document.getElementById("iframe");
        iframe.src = links[index];
        if (labels != null && labels[index] == 0) {
            if (labels[index - 1] != 0) { //labels should be reversed, last homepage was green
                var not_homepage_button = document.getElementById('notHomepage');
                not_homepage_button.classList.remove('btn-primary');
                not_homepage_button.classList.add('btn-success');
                var homepage_button = document.getElementById('homepage');
                homepage_button.classList.remove('btn-success');
                homepage_button.classList.add('btn-primary');
            }
        } else {
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
});

window.onload = function() {
    if (labels != null && labels[0] == 0) {
        var not_homepage_button = document.getElementById('notHomepage');
        not_homepage_button.classList.remove('btn-primary');
        not_homepage_button.classList.add('btn-success');
    } else if (labels != null) {
        var homepage_button = document.getElementById('homepage');
        homepage_button.classList.remove('btn-primary');
        homepage_button.classList.add('btn-success');
    }
};
