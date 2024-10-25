const powerballOdds = 292200000;  // 1 in 292.2 million
let lotteryNumber = generateNumber();

function generateNumber() {
    return Math.floor(Math.random() * 1000000000) + 1;  // Generates a random number between 1 and 1 billion
}

function simulateWin(odds) {
    return Math.random() * odds < 1;  // 1 in X chance, win if random number is less than 1
}

function makeGuess() {
    const userGuess = document.getElementById("userGuess").value;
    const resultText = document.getElementById("result");

    if (userGuess) {
        const isPowerballWin = simulateWin(powerballOdds);

        if (isPowerballWin) {
            resultText.textContent = "Congratulations! You beat the odds and won the Powerball!";
        } else {
            resultText.textContent = `Too bad! The correct number was: ${lotteryNumber}. Try again!`;
        }

        lotteryNumber = generateNumber();  // Generate a new number for the next guess
    } else {
        resultText.textContent = "Please enter a valid guess!";
    }

    document.getElementById("userGuess").value = '';  // Clear the input field after each guess
}
}
