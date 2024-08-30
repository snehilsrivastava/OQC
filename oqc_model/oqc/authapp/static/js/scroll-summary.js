function navigateToPage(card) {
    const productName = card.querySelector('.card-prod').textContent.trim();
    const stageName = card.querySelector('.card-heading .stage').textContent.trim();
    const modelName = card.querySelector('.card-heading .model').textContent.trim();

    const filterForm = document.querySelector('#filter-form');
    const filterProdField = filterForm.querySelector('select#product');
    const filterStageField = filterForm.querySelector('select#test_stage');
    const filterModelField = filterForm.querySelector('select#model_name');

    filterProdField.value = productName;
    filterStageField.value = stageName;
    populateModels();
    filterModelField.value = modelName;
    filterForm.submit();
}

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

function displayStatusPerTeam(button, event, sum) {
    event.stopPropagation();
    const team = button.textContent.trim();
    const testCounts = button.parentElement.parentElement.parentElement.previousElementSibling;
    
    if (team === "Product") {
        lists = testCounts.querySelectorAll('li');
        lists.forEach((testCount, index) => {
            let splitText = testCount.textContent.split(': ');
            testCount.textContent = splitText[0] + ": " + sum.Count.PO[index];
        });
    } else if (team === "Brand") {
        lists = testCounts.querySelectorAll('li');
        lists.forEach((testCount, index) => {
            let splitText = testCount.textContent.split(': ');
            testCount.textContent = splitText[0] + ": " + sum.Count.BT[index];
        });
    } else if (team === "Legal") {
        lists = testCounts.querySelectorAll('li');
        lists.forEach((testCount, index) => {
            let splitText = testCount.textContent.split(': ');
            testCount.textContent = splitText[0] + ": " + sum.Count.LT[index];
        });
    }
}