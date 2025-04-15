let count = 0;

function checkCredentials() {
    count++;
    var email = $('#email').val();
    var password = $('#password').val();
    var data_d = {'email': email, 'password': password};

    $.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success: function (returned_data) {
            try {
                returned_data = JSON.parse(returned_data);

                if (returned_data.success === 1) {
                    window.location.href = returned_data.redirect;  // Redirects to /home
                } else {
                    $('#error-message').html(`Authentication failed. Attempts: ${count}`);
                }
            } catch (error) {
                console.error("Error parsing JSON:", error);
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX Error:", status, error);
        }
    });
}