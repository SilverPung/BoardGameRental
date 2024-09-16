function confirmDelete(event) {
    if (!confirm("Czy jesteś pewien, że chcesz usunąć tę grę?")) {
        event.preventDefault();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var deleteButton = document.getElementById('delete-game-button');
    deleteButton.addEventListener('click', confirmDelete);
});

document.addEventListener('DOMContentLoaded', function() {
    // Store the initial quantity value
    let previousQuantity = parseInt(document.getElementById('quantity').value);
    
    // Add an event listener for input changes on the quantity field
    document.getElementById('quantity').addEventListener('input', function() {
        // Get the new quantity value from the input
        let newQuantity = parseInt(document.getElementById('quantity').value);
        
        // Calculate the difference between the new and previous quantity
        let quantityChange = newQuantity - previousQuantity;

        // Get the current accessible value
        let accessible = parseInt(document.getElementById('accessible').value);

        // Update the accessible value based on the quantity change
        accessible += quantityChange;

        // Ensure accessible doesn't drop below zero
        if (accessible < 0) {
            accessible = 0;
        }

        // Update the accessible input field
        document.getElementById('accessible').value = accessible;

        // Update the previous quantity to the new value
        previousQuantity = newQuantity;
    });
});