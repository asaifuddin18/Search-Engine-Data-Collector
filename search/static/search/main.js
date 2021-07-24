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
var past_accuracy = null;
var past_precision = null;
var past_f1 = null;
var past_recall = null;
var data_x = null;
var order = null;
try {
    past_accuracy = JSON.parse(document.getElementById('past_accuracy').textContent);
    past_precision = JSON.parse(document.getElementById('past_precision').textContent);
    past_f1 = JSON.parse(document.getElementById('past_f1').textContent);
    past_recall = JSON.parse(document.getElementById('past_recall').textContent);
    data_x = JSON.parse(document.getElementById('data_x').textContent);
    order = JSON.parse(document.getElementById('order').textContent);
} catch(error) {

}
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
    var metrics = ["accuracy", "precision", "recall", "f1"];
    for (var i = 0; i < metrics.length; i++) {
        document.getElementById(metrics[i]).addEventListener("click", function(event) {
            
            document.getElementById("graph_view").textContent = event.target.textContent;
            var i = 0;
            if (event.target.id === "accuracy") {
                myChart.data.datasets.forEach((dataset) => {
                    
                    if (i == 0) {
                        dataset.data = past_accuracy;
                    } else {
                        dataset.data = [];
                    }
                    i++;
                });
            } else if (event.target.id == "precision") {
                myChart.data.datasets.forEach((dataset) => {
                    dataset.data = past_precision[i];
                    i++;
                });
            } else if (event.target.id == "f1") {
                myChart.data.datasets.forEach((dataset) => {
                    dataset.data = past_f1[i];
                    i++;
                });
            } else if (event.target.id == "recall") {
                myChart.data.datasets.forEach((dataset) => {
                    dataset.data = past_recall[i];
                    i++;
                });
            }
            myChart.update();
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

var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data_x,
        datasets: [{
            data: past_accuracy,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#0275d8',
            borderWidth: 4,
            pointBackgroundColor: '#0275d8',
            label: order[0]
          },
          {
            data: [],
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#5cb85c',
            borderWidth: 4,
            pointBackgroundColor: '#5cb85c',
            label: order[1]
          },
          {
            data: [],
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#5bc0de',
            borderWidth: 4,
            pointBackgroundColor: '#5bc0de',
            label: order[2]
          },
          {
            data: [],
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#f0ad4e',
            borderWidth: 4,
            pointBackgroundColor: '#f0ad4e',
            label: order[3]
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                max: 1
              }
            }]
          },
          legend: {
            position: 'top',

        }
    }
});