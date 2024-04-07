$(document).ready(function () {
  $("form").on("submit", function (event) {
    event.preventDefault();

    $.ajax({
      url: "/feedback",
      type: "POST",
      data: $(this).serialize(),
      dataType: "json",
      success: function (response) {
        if (response.success) {
          $("form")[0].reset();
          document.getElementById("message").innerHTML =
            "<span style='color: green'>Feedback added successfully.</span>";
          setTimeout(function () {
            document.getElementById("message").innerHTML = "";
          }, 5000);
          response.success = false;
        }
      },
    });
  });
});
