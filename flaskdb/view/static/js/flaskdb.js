$(function() {
  $("form").submit(function() {
    $(this).find(":submit").prop("disabled", true);
    setTimeout(function() {
      $(this).find(":submit").prop("disabled", false);
    }, 10000);
  });
});
