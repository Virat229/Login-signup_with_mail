 // 60 seconds = 1 minute
let timerInterval;
let timeLeft = sessionStorage.getItem("timeLeft") ? parseInt(sessionStorage.getItem("timeLeft")) : 60;


// Start the timer immediately when the page loads
startTimer();

function startTimer() {
    updateTimer(); // Update the timer immediately on page load
    timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;

    // Add leading zero to seconds if less than 10
    if (seconds < 10) {
        seconds = "0" + seconds;
    }

    document.getElementById("timer").innerText = `${minutes}:${seconds}`;
    document.getElementById("remaining_time").value = seconds;
    sessionStorage.setItem("timeLeft", timeLeft);
    console.log(seconds);
    if (timeLeft === 0) {
        clearInterval(timerInterval);
        alert("OTP Expired");
        sessionStorage.removeItem("timeLeft");
    } else {
        timeLeft--;
    }
}
document.getElementById("resend-form").addEventListener("submit", function() {
    clearInterval(timerInterval);
    timeLeft = 60;
    sessionStorage.setItem("timeLeft", timeLeft);
    startTimer();
});
