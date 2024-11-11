import { serveDir } from "@std/http/file-server";

let targetNumber = Math.floor(Math.random() * 1000000000) + 1; // Initial random number to guess

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

      // Check if the guess is correct
      const correct = userGuess === targetNumber;

      if (!correct) {
        // Generate a new random number if the guess was incorrect
        targetNumber = Math.floor(Math.random() * 1000000000) + 1;
      }

      return new Response(
        JSON.stringify({
          correct,
          correctNumber: correct ? undefined : targetNumber, // Show number if incorrect
        }),
        { headers: { "Content-Type": "application/json" } }
      );
    }

    // Serve static files
    return serveDir(req, { fsRoot: "./static" });
  }
);
