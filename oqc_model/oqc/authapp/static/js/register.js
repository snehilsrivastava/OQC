document.addEventListener('DOMContentLoaded', function () {
    const sendOtpBtn = document.getElementById('send-otp-btn');
    const initialView = document.querySelector('.initial-view');
    const finalView = document.querySelector('.final-view');
    const initialForm = initialView.querySelector('form');
    const finalForm = finalView.querySelector('form');
    const messagesContainer = document.getElementById('messages');

    sendOtpBtn.addEventListener('click', function(){
        const formData = new FormData(initialForm);
        fetch('send_otp/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
            // Redirect to the specified URL
            window.location.href = data.redirect_url;
            }
            else if (data.warning) {
                // Show warning message
                const warningMessage = document.createElement('div');
                warningMessage.classList.add('alert', 'alert-warning', 'alert-dismissible', 'fade', 'show');
                warningMessage.setAttribute('role', 'alert');
                warningMessage.innerHTML = data.message;
                messagesContainer.appendChild(warningMessage);                
            }
            else if (data.success) {
                // Set values in the final form fields
                finalForm.querySelector('input[name="first_name"]').value = formData.get('first_name');
                finalForm.querySelector('input[name="last_name"]').value = formData.get('last_name');
                finalForm.querySelector('input[name="username"]').value = formData.get('username');
                finalForm.querySelector('input[name="password"]').value = formData.get('password');

                // Make fields readonly
                finalForm.querySelector('input[name="first_name"]').readOnly = true;
                finalForm.querySelector('input[name="last_name"]').readOnly = true;
                finalForm.querySelector('input[name="username"]').readOnly = true;
                finalForm.querySelector('input[name="password"]').readOnly = true;
                
                // Toggle views
                initialView.style.display = 'none';
                finalView.style.display = 'block';
            } 
            else {
                // Handle error
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});