document.getElementById("submit-guess").addEventListener("click", async () => {
  const userGuess = document.getElementById("user-guess").value;
  const feedbackDiv = document.getElementById("feedback");

  // Clear previous feedback message
  feedbackDiv.textContent = "";
  feedbackDiv.className = ""; // Reset feedback styling

  // Check for empty input
  if (!userGuess) {
    feedbackDiv.textContent = "Please enter a guess.";
    feedbackDiv.className = "incorrect";
    return;
  }

  // Send the guess to the server
  const response = await fetch("/random", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `userGuess=${userGuess}`,
  });

  const result = await response.json();

  // Update feedback based on the server response
  if (result.correct) {
    feedbackDiv.textContent = "Congratulations! You guessed correctly!";
    feedbackDiv.className = "correct";
    document.getElementById("submit-guess").disabled = true; // Disable the button after a correct guess
  } else {
    feedbackDiv.textContent = `Incorrect! The number was ${result.correctNumber}. Try again!`;
    feedbackDiv.className = "incorrect";
  }

  // Clear the input for a new guess
  document.getElementById("user-guess").value = "";
});
