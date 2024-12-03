/**
* Template Name: Logis
* Updated: Jan 29 2024 with Bootstrap v5.3.2
* Template URL: https://bootstrapmade.com/logis-bootstrap-logistics-website-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Sticky header on scroll
   */
  const selectHeader = document.querySelector('#header');
  if (selectHeader) {
    document.addEventListener('scroll', () => {
      window.scrollY > 100 ? selectHeader.classList.add('sticked') : selectHeader.classList.remove('sticked');
    });
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    const togglescrollTop = function() {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
    window.addEventListener('load', togglescrollTop);
    document.addEventListener('scroll', togglescrollTop);
    scrollTop.addEventListener('click', window.scrollTo({
      top: 0,
      behavior: 'smooth'
    }));
  }

  /**
   * Mobile nav toggle
   */
  const mobileNavShow = document.querySelector('.mobile-nav-show');
  const mobileNavHide = document.querySelector('.mobile-nav-hide');

  document.querySelectorAll('.mobile-nav-toggle').forEach(el => {
    el.addEventListener('click', function(event) {
      event.preventDefault();
      mobileNavToogle();
    })
  });

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavShow.classList.toggle('d-none');
    mobileNavHide.classList.toggle('d-none');
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navbar a').forEach(navbarlink => {

    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll('.navbar .dropdown > a');

  navDropdowns.forEach(el => {
    el.addEventListener('click', function(event) {
      if (document.querySelector('.mobile-nav-active')) {
        event.preventDefault();
        this.classList.toggle('active');
        this.nextElementSibling.classList.toggle('dropdown-active');

        let dropDownIndicator = this.querySelector('.dropdown-indicator');
        dropDownIndicator.classList.toggle('bi-chevron-up');
        dropDownIndicator.classList.toggle('bi-chevron-down');
      }
    })
  });

  /**
   * Initiate pURE cOUNTER
   */
  new PureCounter();

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Init swiper slider with 1 slide at once in desktop view
   */
  new Swiper('.slides-1', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    }
  });

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

});



const totalSeats = 38; // Total number of seats
const rows = 11; // Number of rows
const seatsPerRow = 4; // Number of seats per row

// Function to generate seats and add event listeners
function generateSeats() {
  const seatsContainer = document.getElementById('seats');
  let seatNumber = 1; // Initialize seat number

  for (let i = 0; i < rows; i++) {
    const rowContainer = document.createElement('div');
    rowContainer.classList.add('bus-row');

    // Create seats within each row
    for (let j = 0; j < seatsPerRow; j++) {
      const seat = document.createElement('button');
      seat.classList.add('seat');
      seat.dataset.seatNumber = seatNumber;
      seat.dataset.status = 'available';
      seat.addEventListener('click', toggleSeat);

      // Create image element for the seat
      const seatImage = document.createElement('img');
      seatImage.src = 'assets/seat.svg'; // Image of the seat
      seatImage.alt = `Seat ${seatNumber}`;
      seatImage.classList.add('seat-image'); // Add class to image
      seat.appendChild(seatImage); // Append image to button

      // Create span element for seat number
      const seatNumberSpan = document.createElement('span');
      seatNumberSpan.textContent = seatNumber;
      seatNumberSpan.classList.add('seat-number'); // Add class to span
      seat.appendChild(seatNumberSpan); // Append seat number to button

      rowContainer.appendChild(seat);
      seatNumber++; // Increment seat number
    }

    seatsContainer.appendChild(rowContainer);
  }
}

// Function to toggle seat selection
function toggleSeat(event) {
  const seat = event.currentTarget;
  if (seat.dataset.status === 'available') {
    seat.classList.toggle('selected');
  }
}

// Function to book selected seats
function bookSeats() {
  const selectedSeats = document.querySelectorAll('.seat.selected');
  if (selectedSeats.length === 0) {
    alert('Please select at least one seat.');
    return;
  }

  if (selectedSeats.length > totalSeats) {
    alert('You cannot book more seats than available.');
    return;
  }

  selectedSeats.forEach(seat => {
    seat.classList.remove('selected');
    seat.classList.add('booked');
    seat.dataset.status = 'booked';
    const seatImage = seat.querySelector('.seat-image');
    seatImage.style.filter = 'hue-rotate(100deg)'; // Change image color to red
  });

  alert(`Successfully booked ${selectedSeats.length} seat(s)!`);
}

// Initialize seats
generateSeats();
