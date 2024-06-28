const sendOtpBtn = document.getElementById('send-otp-btn');
const otpFields = document.getElementById('final-view');

sendOtpBtn.addEventListener('click', () => {
  // 1. Get form data (e.g., email) and send an AJAX request
  //    to your Django view to generate and send the OTP.

  // 2. After successful OTP generation and sending:
  sendOtpBtn.style.display = 'none';
  otpFields.style.display = 'block';
});