require('dotenv').config();
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.FRONTEND_PORT || 5001;

// Dossier racine des fichiers statiques
const publicDir = path.join(__dirname, 'public');

const server = http.createServer((req, res) => {
    console.log('Requête reçue :', req.url); // <== Ajoute ça
    // Prévenir les attaques par traversal de chemin
    const decodedUrl = decodeURIComponent(req.url.split('?')[0]);
    const safePath = path.normalize(decodedUrl).replace(/^(\.\.[\/\\])+/, '');
    const finalPath = (safePath === '/' || safePath === '\\') ? 'index.html' : safePath;
    let filePath = path.join(publicDir, finalPath);
    console.log('Chemin de fichier :', filePath); // <== Ajoute ça

    const extname = path.extname(filePath);
    let contentType = 'text/html';

    switch (extname) {
        case '.js':
            contentType = 'application/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.jpg':
        case '.jpeg':
            contentType = 'image/jpeg';
            break;
        case '.svg':
            contentType = 'image/svg+xml';
            break;
    }

    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                res.end('Fichier non trouvé');
            } else {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Erreur serveur');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

server.listen(PORT, () => {
    console.log(`Serveur frontend démarré sur http://localhost:${PORT}`);
});
