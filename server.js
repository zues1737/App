import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = process.env.PORT || 3000;
const DIST_DIR = path.join(__dirname, "dist");
const BASE_DIR = fs.existsSync(DIST_DIR) ? DIST_DIR : __dirname;

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".ico": "image/x-icon"
};

const server = http.createServer((req, res) => {
  const urlPath = req.url.split("?")[0];
  let safePath = path.normalize(decodeURIComponent(urlPath)).replace(/^(\.\.[\/\\])+/, "");
  if (safePath === "/" || safePath === "\\") {
    safePath = "/index.html";
  }

  let filePath = path.join(BASE_DIR, safePath);

  // If path doesn't exist, try falling back to index.html for SPA routing
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(BASE_DIR, "index.html");
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("404 Not Found");
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || "application/octet-stream";
    res.writeHead(200, {
      "Content-Type": contentType,
      "Cache-Control": ext === ".html" ? "no-cache" : "public, max-age=31536000, immutable"
    });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`PCDP Portal server listening on port ${PORT}`);
});
