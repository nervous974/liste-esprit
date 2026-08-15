// Serveur local pour la PWA Tracker Esprits Fortnite
// Lance avec: node serve.js
// Accès: http://TON_IP_PC:3000 (depuis ton téléphone sur le même WiFi)

const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");

const PORT = 3000;
const ROOT = path.join(__dirname, "app-mobile");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
};

const server = http.createServer((req, res) => {
  let filePath = path.join(ROOT, req.url.split("?")[0]);

  // Index par défaut
  if (filePath === ROOT || filePath === ROOT + path.sep) {
    filePath = path.join(ROOT, "index.html");
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      // Fallback SPA
      fs.readFile(path.join(ROOT, "index.html"), (err2, data2) => {
        if (err2) {
          res.writeHead(404);
          res.end("Not found");
          return;
        }
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(data2);
      });
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const mime = MIME[ext] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": mime });
    res.end(data);
  });
});

server.listen(PORT, "0.0.0.0", () => {
  // Trouver l'IP locale du PC
  const nets = os.networkInterfaces();
  let localIp = "localhost";
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === "IPv4" && !net.internal) {
        localIp = net.address;
        break;
      }
    }
  }

  console.log("\n==============================================");
  console.log("  TRACKER ESPRITS FORTNITE – Serveur local");
  console.log("==============================================");
  console.log(`\n  PC (navigateur) : http://localhost:${PORT}`);
  console.log(`  Téléphone/tablette (même WiFi) :`);
  console.log(`  → http://${localIp}:${PORT}`);
  console.log(
    "\n  Sur ton téléphone, ouvre Chrome et tape l'adresse ci-dessus.",
  );
  console.log("  Ensuite: menu ⋮ → \"Ajouter à l'écran d'accueil\"");
  console.log(
    "  L'app s'installe comme une vraie appli, fonctionne sans PC ensuite.\n",
  );
  console.log("  Ctrl+C pour arrêter le serveur.\n");
});
