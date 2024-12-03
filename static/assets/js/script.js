// Get all seat elements
const seats = document.querySelectorAll('.seat');
const selectedSeats = []; // Array to store selected seat numbers

// Add click event listener to each seat
seats.forEach((seat, index) => {
  seat.addEventListener('click', () => {
    const seatNumber = index + 1;
    toggleSeatSelection(seat, seatNumber);
  });
});

// Function to toggle seat selection
function toggleSeatSelection(seatElement, seatNumber) {
  const isSelected = seatElement.classList.contains('selected');

  // Toggle the 'selected' class
  seatElement.classList.toggle('selected');

  // Update the selectedSeats array
  if (isSelected) {
    const index = selectedSeats.indexOf(seatNumber);
    selectedSeats.splice(index, 1);
  } else {
    selectedSeats.push(seatNumber);
  }

  console.log(`Selected seats: ${selectedSeats.join(', ')}`);
}

