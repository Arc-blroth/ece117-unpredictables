import { serveDir } from "@std/http/file-server";

// Function to generate a random target number
const generateRandomNumber = () => Math.floor(Math.random() * 1000000000) + 1;

// for debugging reconstructions of the single-packet-attack
let seq: number = 0;

Deno.serve(
  {
    port: 3443,
    cert: await Deno.readTextFile("cert.pem"),
    key: await Deno.readTextFile("key.pem"),
  },
  async (req: Request) => {
    const pathname = new URL(req.url).pathname;

    if (pathname === "/random" && req.method === "POST") {
      // Parse the user's guess from the request
      const formData = new URLSearchParams(await req.text());
      const userGuess = parseInt(formData.get("userGuess") || "0", 10);

      // Generate a new random number for each guess
      const targetNumber = generateRandomNumber();

      // Check if the guess is correct
      const correct = userGuess === targetNumber;

      // Return the feedback and the new random number for the next guess
      return new Response(
        JSON.stringify({
          seq: seq++,
          correct,
          correctNumber: correct ? undefined : targetNumber, // Show the number if incorrect
        }),
        { headers: { "Content-Type": "application/json" } }
      );
    }

    // Serve static files
    return serveDir(req, { fsRoot: "./static" });
  }
);
