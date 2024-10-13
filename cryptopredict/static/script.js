// prediction button functionality
const hours = 3 * 60 * 1000;

function handleButtonClick() {
    const button = document.getElementById('predictBtn');
    button.disabled = true;
    localStorage.setItem('disableTime', Date.now());
    button.innerText = "Please wait for 3 hours...";
}

function checkButtonState() {
    const disableTime = localStorage.getItem('disableTime');
    const button = document.getElementById('predictBtn');
    
    if (disableTime) {
        const elapsedTime = Date.now() - disableTime;
        if (elapsedTime < hours) {
            button.disabled = true; 
            button.innerText = "Please wait for 3 hours...";
        } else {
            button.disabled = false;
            button.innerText = "Get Started";
            localStorage.removeItem('disableTime');
        }
    }
}

// Wait for the DOM to be fully loaded before running the scripts
document.addEventListener('DOMContentLoaded', function() {
    // Initial state check for the prediction button
    checkButtonState();

    // Expose handleButtonClick to global scope for the button click
    window.handleButtonClick = handleButtonClick;

    // Account page functionality
    const LoginForm = document.getElementById("LoginForm");
    const RegForm = document.getElementById("RegForm");
    const Indicator = document.getElementById("Indicator");

    function register() {
        RegForm.style.transform = "translateX(0px)";
        LoginForm.style.transform = "translateX(0px)";
        Indicator.style.transform = "translateX(100px)";
    }

    function login() {
        RegForm.style.transform = "translateX(300px)";
        LoginForm.style.transform = "translateX(300px)";
        Indicator.style.transform = "translateX(0px)";
    }

    // Call login function by default
    login();

    // Handle pop-up messages using JavaScript
    var messages = {{ messages|json_script:"messages" }};
    if (messages.length > 0) {
        messages.forEach(function(message) {
            alert(message);
        });
    }
});
