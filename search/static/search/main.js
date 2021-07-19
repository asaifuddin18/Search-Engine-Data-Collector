var dict_t = {
    "Professor": "FirstName LastName Institution\ne.g. Jian Peng UIUC",
    "Movie": "Name Year\ne.g. Avatar 2009",
    "Electronic": "Model Year/Model\ne.g. iPhone 12"
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
//var features = ["tf", "tf_mi"];

window.onload = function() {
    for (var key in dict_t) {
        document.getElementById(key).addEventListener("click", function(event) {
            var queryBox = document.getElementById("your_queries");
            queryBox.placeholder = "Enter queries following the template: " + dict_t[event.target.id];
            document.getElementById("dropdownMenuButton").textContent = event.target.id;
            var your_object = document.getElementById("your_object");
            your_object.value = event.target.id;
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