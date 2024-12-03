// Event listener for form submission
bookingForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent form submission
  
    // Get form data
    const formData = new FormData(event.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const phone = formData.get('phone');
    const destination = formData.get('destination');
    const boarding = formData.get('boarding');
    const selectedSeats = selectedSeatsInput.value.split(',').map(Number);
  
    // Create a JavaScript object with the form data
    const booking = {
      name,
      email,
      phone,
      destination,
      boarding,
      seats: selectedSeats.join(','),
    };
  
    // Send the booking data to the server using an AJAX request
    fetch('/book/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}', // Include the CSRF token
      },
      body: JSON.stringify(booking),
    })
    .then(response => {
      if (response.ok) {
        // Handle successful response
        console.log('Booking successful');
        // Reset the form
        event.target.reset();
        selectedSeatsInput.value = '';
      } else {
        // Handle error response
        console.error('Booking failed');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });