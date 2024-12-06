$(document).ready(function() {
    const $resizer = $('#resizer');
    const $tableContainer = $('#table-container');
    let isResizing = false;

    // Start resizing when dragging starts
    $resizer.on('mousedown', function(e) {
        isResizing = true;
        $('body').css('user-select', 'none'); // Prevent text selection during resize
    });

    // Stop resizing when mouse button is released
    $(document).on('mouseup', function() {
        isResizing = false;
        $('body').css('user-select', ''); // Re-enable text selection
    });

    // Resize the table section as the mouse moves
    $(document).on('mousemove', function(e) {
        if (!isResizing) return;
        const newHeight = e.clientY - $tableContainer.offset().top;
        $tableContainer.height(newHeight);
    });
});

// Function to Submit the Form
function submitForm() {
    $('#medicineForm').submit();
}

// Function to Close the Form
function closeForm() {
    $('#medicineForm')[0].reset();
}