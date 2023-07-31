var dropdown = document.getElementById("myDropdown");
var mainContainer = document.getElementById("main-container");
var isRotated = false; // Variable to keep track of button rotation state

function dropdownMenu() {
  dropdown.classList.toggle("show");

  // Toggle the rotation class on the button
  var button = document.querySelector('.dropbtn');
  isRotated = !isRotated;
  button.classList.toggle("rotate", isRotated);

  // Add margin-top to main-container element
  if (dropdown.classList.contains('show')) {
    mainContainer.style.marginTop = dropdown.offsetHeight + 'px';
  } else {
    mainContainer.style.marginTop = '';
  }
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }

    // Reset button rotation state when clicking outside the dropdown
    var button = document.querySelector('.dropbtn');
    if (isRotated) {
      isRotated = false;
      button.classList.remove("rotate");
    }

    // Remove margin-top from main-container element
    mainContainer.style.marginTop = '';
  }
}


