$(document).ready(function () {
  $("form").on("submit", function (event) {
    event.preventDefault();

    $.ajax({
      url: "/grades",
      type: "POST",
      data: $(this).serialize(),
      dataType: "json",
      success: function (response) {
        if (response.regrade_exists) {
          document.getElementById("message").innerHTML =
            "<span style='color: red'>The regrade request already exists.</span>";
        } else {
          document.getElementById("message").innerHTML =
            "<span style='color: green'>Regrade request added successfully.</span>";
        }
      },
    });
    $("#assesment").on("change", function () {
      document.getElementById("message").innerHTML = "";
    });
  });
});
