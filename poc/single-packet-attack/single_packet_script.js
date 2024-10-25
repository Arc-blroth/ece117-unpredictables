function haxxor() {
  const f = Math.random;
  Math.random = () => {
    derp = f();
    console.log(derp);
    return derp;
  };

  outputs = [];

  const inputField = document.querySelector("#userGuess");
  const button = document.querySelector("button");
  const result = document.querySelector("#result");
  for (let i = 0; i < 1000; i++) {
    inputField.value = "1";
    button.click();

    const regex = /\d+/;
    const match = result.innerText.match(regex);
    if (match) {
      outputs.push(parseInt(match[0], 10));
    }
  }
  return outputs;
}
