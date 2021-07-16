var dict = {
    "Professor": "FirstName LastName Institution\ne.g. Jian Peng UIUC",
    "Movie": "Name Year\ne.g. Avatar 2009",
    "Electronic": "Model Year/Model\ne.g. iPhone 12"
};

window.onload = function() {
    for (var key in dict) {
        document.getElementById(key).addEventListener("click", function(event) {
            var queryBox = document.getElementById("your_queries");
            queryBox.placeholder = "Enter queries following the template: " + dict[event.target.id];
            document.getElementById("dropdownMenuButton").textContent = event.target.id;
            var your_object = document.getElementById("your_object");
            your_object.value = event.target.id;
        })
    }
    document.getElementById("download_dataset").addEventListener("click", function(event) {
        alert('hi');
        document.location.href = "/download_dataset";
    })
}