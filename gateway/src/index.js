const express = require('express');
const cors = require('cors');
require('dotenv').config();

const routes = require('./routes');

const app = express();
const PORT = process.env.PORT;

// Middleware
app.use(cors());
app.use(express.json());

// Request ID Middleware
app.use((req, res, next) => {
    if (!req.headers['x-request-id']) {
        req.headers['x-request-id'] = require('crypto').randomUUID();
    }
    next();
});

// Routes
app.use('/api', routes);

// Root Landing Page
app.get('/', (req, res) => {
    res.send(`
        <div style="font-family: sans-serif; padding: 40px; text-align: center;">
            <h1 style="color: #4f46e5;">📚 Library API Gateway</h1>
            <p style="color: #4b5563;">Status: <span style="color: #059669;">Running</span></p>
            <hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0;" />
            <p>This is the RESTful entry point for the backend. Use <strong>/api</strong> for data endpoints or <strong>/health</strong> for status.</p>
            <p><a href="http://localhost:5173" style="color: #4f46e5; text-decoration: none; font-weight: bold;">Go to Frontend UI →</a></p>
        </div>
    `);
});

// Health Check
app.get('/health', (req, res) => {
    res.json({ status: 'OK', service: 'library-gateway' });
});

const errorHandler = require('./middleware/errorHandler');

// ... (routes) ...
app.use('/api', routes);

// ... (other routes) ...

// Global Error Handler (MUST be last)
app.use(errorHandler);

app.listen(PORT, () => {
    console.log(`Gateway running on http://localhost:${PORT}`);
    console.log(`Connected to Backend at ${process.env.BACKEND_HOST}`);
});
