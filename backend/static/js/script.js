document.addEventListener('DOMContentLoaded', function() {
  var input = document.getElementById("filterInput");
  input.addEventListener("input", function() {
    var filter = input.value.toUpperCase();
    var table = document.getElementById("data-table");
    var tr = table.getElementsByTagName("tr");

    for (var i = 1; i < tr.length; i++) { // Начинаем с 1, чтобы пропустить заголовок
      var display = false;
      var td = tr[i].getElementsByTagName("td");

      for (var j = 0; j < td.length; j++) {
        var txtValue = td[j].textContent || td[j].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          display = true;
          break;
        }
      }

      if (display) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  });
});
