var dict_t = {
    "Professor": ["First Name", "Last Name", "Institution"],
    "Movie": ["Name", "Year"],
    "Electronic": ["Name", "Model No./Year"]
};

var models = {
    "rf": "Random Forest",
    "svm": "SVM"
};
var features = {
    "tf": "Term Frequency",
    "tf_mi": "Term Frequency * Mutual Information",
    "tf_idf": "Term Frequency * Inverse Doc. Freq."
};
var qs = ["q1", "q2", "q3", "q4", "q5", "q6"];
//var features = ["tf", "tf_mi"];

window.onload = function() {
    for (var key in dict_t) {
        document.getElementById(key).addEventListener("click", function(event) {
            //var queryBox = document.getElementById("your_queries");
            //queryBox.placeholder = "Enter queries following the template: " + dict_t[event.target.id];
            document.getElementById("dropdownMenuButton").textContent = event.target.id;
            var your_object = document.getElementById("your_object");
            your_object.value = event.target.id;
            for (var i = 0; i < qs.length; i++) {
                var curQ = document.getElementById(qs[i]);
                curQ.style.visibility = "hidden";
                curQ.required = false;
            }
            
            for (var i = 0; i < dict_t[event.target.id].length; i++) {
                var curQ = document.getElementById(qs[i]);
                curQ.style.visibility = "visible";
                curQ.placeholder = dict_t[event.target.id][i];
                curQ.required = true;
            }
        })
    }

    for (var model in models) {
        document.getElementById(model).addEventListener("click", function(event) {
            document.getElementById("dropdown_ml_models").textContent = models[event.target.id];
        })
    }

    for (var feature in features) {
        document.getElementById(feature).addEventListener("click", function(event) {
            document.getElementById("dropdown_features").textContent = features[event.target.id];
        })
    }
    document.getElementById("change_model").addEventListener("click", function(event) {
        var model = document.getElementById("dropdown_ml_models").textContent;
        var feature = document.getElementById("dropdown_features").textContent;
        document.location.href = "/model/" + model + "/" + feature;
    })
}