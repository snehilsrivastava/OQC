// function which defines what happens on clicking the cards
// function navigateToPage(pageUrl) {
//     window.location.href = pageUrl;
// }

function isTouchScreenDevice() {
    return 'ontouchstart' in window;
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.scrollcontainer');

    // Define scroll speed and interval
    const scrollSpeed = 200; // Adjust scroll speed (higher value for faster scrolling)
    const scrollInterval = 1500; // Adjust scroll interval in milliseconds
    let scrollDirection = 'right'; // Initial scroll direction

    // Function to scroll container automatically
    function autoScroll() {
        if (scrollDirection === 'right') {
            container.scrollLeft += scrollSpeed;
            // Check if reached end of scroll
            if (container.scrollLeft >= container.scrollWidth - container.clientWidth) {
                scrollDirection = 'left';
            }
        } else if (scrollDirection === 'left') {
            container.scrollLeft -= scrollSpeed;
            // Check if scrolled back to start
            if (container.scrollLeft <= 0) {
                scrollDirection = 'right';
            }
        }
    }

    // Start auto-scrolling
    let scrollIntervalId = setInterval(autoScroll, scrollInterval);

    if (!isTouchScreenDevice()) {
        // Stop auto-scrolling when mouse enters container
        container.addEventListener('mouseover', () => {
            clearInterval(scrollIntervalId);
        });

        // Resume auto-scrolling when mouse leaves container
        container.addEventListener('mouseout', () => {
            scrollIntervalId = setInterval(autoScroll, scrollInterval);
        });
    }
    else {
        container.addEventListener('touchstart', () => {
            clearInterval(scrollIntervalId);
        });
    
        // Resume auto-scrolling when mouse leaves container
        container.addEventListener('touchend', () => {
            setTimeout(() => {
                scrollIntervalId = setInterval(autoScroll, scrollInterval);
            }, 2000);
        });
    }

    // Optional: Stop auto-scrolling when clicking on a card
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            clearInterval(scrollIntervalId);
        });
    });
});
