document.addEventListener("DOMContentLoaded", function() {
    const ifaConcurrenceSelect = document.getElementById("ifaConcurrence");
    const ifaConcurrenceNoGroup = document.getElementById("ifaConcurrenceNoGroup");
    const rejectionReasonGroup = document.getElementById("rejectionReasonGroup");
    const provisionStatusSelect = document.getElementById("provisionStatus");

    // Event listener for ifaConcurrence field
    ifaConcurrenceSelect.addEventListener("change", function() {
        if (ifaConcurrenceSelect.value === "Yes") {
            ifaConcurrenceNoGroup.style.display = "block";
            // Make ifaConcurrenceNo field mandatory
            document.getElementById("ifaConcurrenceNo").required = true;
        } else {
            ifaConcurrenceNoGroup.style.display = "none";
            // Make ifaConcurrenceNo field non-mandatory
            document.getElementById("ifaConcurrenceNo").required = false;
        }
    });

    // Event listener for provisionStatus field
    provisionStatusSelect.addEventListener("change", function() {
        if (provisionStatusSelect.value === "Rejected") {
            rejectionReasonGroup.style.display = "block";
            // Make rejectionReason field mandatory
            document.getElementById("rejectionReason").required = true;
        } else {
            rejectionReasonGroup.style.display = "none";
            // Make rejectionReason field non-mandatory
            document.getElementById("rejectionReason").required = false;
        }
    });

    // Form submission handling
    const form = document.getElementById("sanctionForm");
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Perform AJAX request or form submission
        const formData = new FormData(form);
        fetch("/sanction_details_edit", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Sanction details stored successfully!") {
                alert(data.message);
                form.reset(); // Reset the form after successful submission
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again later.");
        });
    });
});

function clearDefaultValue(input) {
    if (input.value === "please enter your name") {
        input.value = "";
    }
}
