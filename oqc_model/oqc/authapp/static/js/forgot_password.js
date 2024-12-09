document.addEventListener("DOMContentLoaded", function() {
    const sendOtpBtn = document.getElementById("send-otp-btn");
    const initialView = document.querySelector(".initial-view");
    const initialForm = initialView.querySelector('form');

    const verifyOtpBtn = document.getElementById("verify-otp-btn");
    const otpView = document.querySelector(".otp-view");
    const otpForm = otpView.querySelector('form');

    const submitBtn = document.getElementById("submit-btn"); 
    const finalView = document.querySelector(".final-view");
    const finalForm = finalView.querySelector('form');

    sendOtpBtn.addEventListener("click", function(e) {
        e.preventDefault();
        const formData = new FormData(initialForm);
        fetch("send_otp/", {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                otpForm.querySelector('input[name="username"]').value = formData.get('username');
                otpForm.querySelector('input[name="username"]').readOnly = true;

                initialView.style.display = "none";
                otpView.style.display = "block";
                finalView.style.display = "none";

                const messagesContainer = document.getElementById("messages-2");
                const successMessage = document.createElement('div');
                successMessage.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show');
                successMessage.setAttribute('role', 'alert');
                successMessage.innerHTML = `<span class="message-span">${data.message}</span>
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                            </button>`;
                messagesContainer.appendChild(successMessage);
            } 
            else if (data.error) {
                const messagesContainer = document.getElementById("messages-1");
                const errorMessage = document.createElement('div');
                errorMessage.classList.add('alert', 'alert-error', 'alert-dismissible', 'fade', 'show');
                errorMessage.setAttribute('role', 'alert');
                errorMessage.innerHTML = `<span class="message-span">${data.message}</span>
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                            </button>`;
                messagesContainer.appendChild(errorMessage);
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

    verifyOtpBtn.addEventListener("click", function(e) {
        e.preventDefault();
        const formData = new FormData(otpForm);
        fetch("verify_otp/", {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                finalForm.querySelector('input[name="username"]').value = formData.get('username');
                finalForm.querySelector('input[name="username"]').readOnly = true;

                initialView.style.display = "none";
                otpView.style.display = "none";
                finalView.style.display = "block";

                const messagesContainer = document.getElementById("messages-3");
                const successMessage = document.createElement('div');
                successMessage.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show');
                successMessage.setAttribute('role', 'alert');
                successMessage.innerHTML = `<span class="message-span">${data.message}</span>
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                            </button>`;
                messagesContainer.appendChild(successMessage);
            } 
            else if (data.error) {
                const messagesContainer = document.getElementById("messages-2");
                const errorMessage = document.createElement('div');
                errorMessage.classList.add('alert', 'alert-error', 'alert-dismissible', 'fade', 'show');
                errorMessage.setAttribute('role', 'alert');
                errorMessage.innerHTML = `<span class="message-span">${data.message}</span>
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                            </button>`;
                messagesContainer.appendChild(errorMessage);
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

    submitBtn.addEventListener("click", function(e) {
        e.preventDefault();
        const formData = new FormData(finalForm);
        fetch("update_password/", {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                // Redirect to the specified URL
                window.location.href = data.redirect_url;
            } 
            else if (data.error) {
                const messagesContainer = document.getElementById("messages-3");
                const errorMessage = document.createElement('div');
                errorMessage.classList.add('alert', 'alert-error', 'alert-dismissible', 'fade', 'show');
                errorMessage.setAttribute('role', 'alert');
                errorMessage.innerHTML = `<span class="message-span">${data.message}</span>
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                            </button>`;
                messagesContainer.appendChild(errorMessage);
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

})

document.addEventListener("DOMContentLoaded", function () {
    var otpInputs = document.querySelectorAll(".otp-input");
  
    function setupOtpInputListeners(inputs) {
      inputs.forEach(function (input, index) {
        input.addEventListener("paste", function (ev) {
          var clip = ev.clipboardData.getData("text").trim();
          if (!/^\d{6}$/.test(clip)) {
            ev.preventDefault();
            return;
          }
  
          var characters = clip.split("");
          inputs.forEach(function (otpInput, i) {
            otpInput.value = characters[i] || "";
          });
  
          enableNextBox(inputs[0], 0);
          inputs[5].removeAttribute("disabled");
          inputs[5].focus();
          updateOTPValue(inputs);
        });
  
        input.addEventListener("input", function () {
          var currentIndex = Array.from(inputs).indexOf(this);
          var inputValue = this.value.trim();
  
          if (!/^\d$/.test(inputValue)) {
            this.value = "";
            return;
          }
  
          if (inputValue && currentIndex < 5) {
            inputs[currentIndex + 1].removeAttribute("disabled");
            inputs[currentIndex + 1].focus();
          }
  
          if (currentIndex === 4 && inputValue) {
            inputs[5].removeAttribute("disabled");
            inputs[5].focus();
          }
  
          updateOTPValue(inputs);
        });
  
        input.addEventListener("keydown", function (ev) {
          var currentIndex = Array.from(inputs).indexOf(this);
  
          if (!this.value && ev.key === "Backspace" && currentIndex > 0) {
            inputs[currentIndex - 1].focus();
          }
        });
      });
    }
  
    function updateOTPValue(inputs) {
        var otpValue = "";
        inputs.forEach(function (input) {
            otpValue += input.value;
        });
    
        if (inputs === otpInputs) {
            document.getElementById("OTP-code").value = otpValue;
        }
    }
  
    // Setup listeners for OTP inputs
    setupOtpInputListeners(otpInputs);
  
    // Initial focus on first OTP input field
    otpInputs[0].focus();
});