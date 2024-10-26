const submitGuessBtn = document.getElementById('submitGuess');
const restartButton = document.getElementById('restartButton');
const message = document.getElementById('message');
const winningNumbers = document.getElementById('winningNumbers');
let guessCount = 0;
let winningNums = [];

// Function to generate random winning numbers
function generateWinningNumbers() {
  const nums = new Set();
  while (nums.size < 5) {
    nums.add(Math.floor(Math.random() * 69) + 1); // Generate numbers between 1 and 69
  }
  winningNums = Array.from(nums);
}

// Function to check if the user has won (all guesses must match)
function checkWin(guesses) {
  return guesses.length === 5 && winningNums.every((num) => guesses.includes(num));
}

// Event listener for submitting guesses
submitGuessBtn.addEventListener('click', () => {
  const guesses = [
    parseInt(document.getElementById('guess1').value),
    parseInt(document.getElementById('guess2').value),
    parseInt(document.getElementById('guess3').value),
    parseInt(document.getElementById('guess4').value),
    parseInt(document.getElementById('guess5').value),
  ];

  // Validate guesses
  const invalidInputs = guesses.map((guess, index) => {
    if (!guess || guess < 1 || guess > 69) {
      return `Guess ${index + 1} is invalid.`;
    }
    return null;
  }).filter(Boolean);

  if (invalidInputs.length > 0) {
    message.textContent = invalidInputs.join(' ');
    return;
  }

  guessCount++;

  // Generate winning numbers only on the first submission
  if (guessCount === 1) {
    generateWinningNumbers();
    const winningBalls = winningNumbers.querySelectorAll('.ball');
    winningBalls.forEach((ball, index) => {
      ball.textContent = winningNums[index];
    });
  }

  // Check for winning numbers
  const allCorrect = checkWin(guesses);
  if (allCorrect) {
    message.textContent = "Congratulations! You won! \n here is the flag: cyber{flag}";
  } else {
    message.textContent = "You lost! Better luck next time.";
  }

  // Disable button after the first guess
  submitGuessBtn.disabled = true;
});

// Event listener for restarting the game
restartButton.addEventListener('click', () => {
  // Reset everything
  guessCount = 0;
  document.getElementById('guess1').value = '';
  document.getElementById('guess2').value = '';
  document.getElementById('guess3').value = '';
  document.getElementById('guess4').value = '';
  document.getElementById('guess5').value = '';
  
  message.textContent = '';
  submitGuessBtn.disabled = false;

  // Reset winning numbers
  const winningBalls = winningNumbers.querySelectorAll('.ball');
  winningBalls.forEach(ball => {
    ball.textContent = '???';
  });
});
