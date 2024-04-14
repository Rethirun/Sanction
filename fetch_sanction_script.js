$(document).ready(function() {
    var initialProvisionStatus; // Variable to store the initial provision status

    // Function to show or hide the rejection reason field based on the selected option
    function toggleRejectionReason() {
        var selectedOption = $('#provisionStatus').val();
        if (selectedOption === 'Rejected') {
            $('#rejectionReasonGroup').show(); // Show the rejection reason field
            $('#rejectionReason').prop('required', true); // Make the field mandatory
        } else {
            $('#rejectionReasonGroup').hide(); // Hide the rejection reason field
            $('#rejectionReason').prop('required', false); // Remove the mandatory requirement
        }
    }

    // Call the function whenever the provision status field changes
    $('#provisionStatus').change(function() {
        toggleRejectionReason();
    });

    // AJAX request to fetch sanction details
    $('#sanctionForm').submit(function(event) {
        event.preventDefault(); // Prevent form submission
        var cfaSanctionNo = $('#cfaSanctionNo').val();

        $.ajax({
            type: 'POST',
            url: '/fetch_sanction_details',
            data: { cfaSanctionNo: cfaSanctionNo },
            success: function(response) {
                if (response.status === 'success') {
                    //console.log("Fetched data:", response.data); // Log fetched data
                    updateForm(response.data); // Update the form with fetched data
                    initialProvisionStatus = response.data.provisionStatus; // Store initial provision status
                    toggleRejectionReason(); // Show or hide rejection reason based on initial provision status
                } else {
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error fetching data:', error);
                alert('An error occurred while fetching data.');
            }
        });
    });

    // Update the form fields with fetched data
    function updateForm(data) {
        //console.log("Data received for form update:", data);

        // Loop through each key-value pair in the data object
        Object.keys(data).forEach(function(key) {
            //console.log("Updating field:", key, "with value:", data[key]);

            // Check if the field is a date field and format it accordingly
            if (key === 'cfaSanctionDate') {
                // Parse the date string as a Date object
                var date = new Date(data[key]);
                // Format the date as 'yyyy-MM-dd'
                var year = date.getFullYear();
                var month = (date.getMonth() + 1).toString().padStart(2, '0');
                var day = date.getDate().toString().padStart(2, '0');
                var formattedDate = `${year}-${month}-${day}`;
                $('#' + key).val(formattedDate);
            } else if (key === 'provisionStatus') {
                // Set the provision status field with fetched value
                //console.log("Targeting provisionStatus field...");
                $('#' + key).val(data[key]);
            } else {
                // For other fields, directly set the value
                $('#' + key).val(data[key]);
            }
        });

        // Show the details section, back button, and update button
        $('.sanctionDetails, .back-button, #updateButton').show();
    }

    // Handle click event for the update button
    $('#updateButton').click(function() {
        var newProvisionStatus = $('#provisionStatus').val();

        // Check if the provision status has been changed
        if (initialProvisionStatus === newProvisionStatus) {
            alert('Please select a different provision status.');
        } else {
            var formData = $('#sanctionForm').serialize();
            $.ajax({
                url: '/update_sanction_details',
                type: 'POST',
                data: formData,
                success: function(response) {
                    alert(response);
                },
                error: function(xhr, status, error) {
                    console.error('Error updating data:', error);
                    alert('An error occurred while updating data.');
                }
            });
        }
    });
});
