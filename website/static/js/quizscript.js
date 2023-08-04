var radios = document.getElementsByName("choice");

for (var i = 0; i < radios.length; i++) {
    radios[i].addEventListener("change", function() {
        var anyChecked = false;
        for (var j = 0; j < radios.length; j++) {
            if (radios[j].checked) {
                anyChecked = true;
                break;
            }
        }

        var submitButton = document.querySelector("input[type=submit]");
        if (anyChecked) {
            submitButton.style.backgroundColor = "green";
        } else {
            submitButton.style.backgroundColor = "red";
        }
    });
}

document.getElementById("quiz-form").addEventListener("submit", function(event) {
    var anyChecked = false;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            anyChecked = true;
            break;
        }
    }

    if (!anyChecked) {
        alert("You must choose an answer!");
        event.preventDefault();
    }
});
