// Get the user inputs
const inputs = document.querySelectorAll('.user-box input');

// Add event listeners to the inputs
inputs.forEach(input => {
    input.addEventListener('focus', () => {
        input.parentElement.classList.add('active');
    });

    input.addEventListener('blur', () => {
        if (input.value === '') {
            input.parentElement.classList.remove('active');
        }
    });
}); 
// Add a scroll event listener to the window
window.addEventListener('scroll', () => {
    // Get the footer element
    const footer = document.querySelector('.footer');

    // Check if the user has scrolled to the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        footer.classList.add('active');
    } else {
        footer.classList.remove('active');
    }
}); 
// Get the profile image element
const profileImg = document.querySelector('.pro-img');

// Add a click event listener to the profile image
profileImg.addEventListener('click', () => {
    // Toggle a class on the profile image element
    profileImg.classList.toggle('rotate');
}); 
// Get the navigation links
const navLinks = document.querySelectorAll('.nav-bar a');

// Add event listeners to the links
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        // Remove the 'active' class from all links
        navLinks.forEach(link => {
            link.classList.remove('active');
        });

        // Add the 'active' class to the clicked link
        link.classList.add('active');
    });
});

// Get the logout button
const logoutButton = document.querySelector('.nav-bar a.logout');

// Add a click event listener to the logout button
logoutButton.addEventListener('click', () => {
    // Send a POST request to the logout endpoint
    fetch('{% url "logout" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            csrfmiddlewaretoken: '{{ csrf_token }}'
        })
    })
    .then(response => {
        // Reload the page once the user has been logged out
        window.location.reload();
    })
    .catch(error => {
        console.error('Error logging out:', error);
    });
}); 
// Get the back button element
const backButton = document.querySelector('.backButtten');

// Add a click event listener to the back button
backButton.addEventListener('click', () => {
    // Navigate back to the previous page
    window.history.back();
});
