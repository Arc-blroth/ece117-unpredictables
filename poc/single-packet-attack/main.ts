import { serveDir } from "@std/http/file-server";

Deno.serve(
  {
    port: 3443,
    cert: await Deno.readTextFile("cert.pem"),
    key: await Deno.readTextFile("key.pem"),
  },
  (req: Request) => {
    const pathname = new URL(req.url).pathname;
    if (pathname === "/random") {
      return new Response(
        (Math.floor(Math.random() * 10000) + 1).toString(),
        {
          headers: { "content-type": "application/json" },
        },
      );
    }
    return serveDir(req, { fsRoot: "./static" });
  },
);
