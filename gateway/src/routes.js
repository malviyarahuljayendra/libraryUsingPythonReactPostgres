const express = require('express');
const router = express.Router();
const client = require('./client');
const { grpcAsync } = require('./utils/grpcHelper');

// Helper to wrap async routes
const asyncHandler = fn => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

// --- Authors ---
router.get('/authors', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListAuthors', { page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

router.post('/authors', asyncHandler(async (req, res) => {
    const { name, bio } = req.body;
    const response = await grpcAsync(client, 'CreateAuthor', { name, bio }, req);
    res.status(201).json(response);
}));

// --- Genres ---
router.get('/genres', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListGenres', { page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

router.post('/genres', asyncHandler(async (req, res) => {
    const { name } = req.body;
    const response = await grpcAsync(client, 'CreateGenre', { name }, req);
    res.status(201).json(response);
}));

// --- Books ---
router.get('/books', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListBooks', { page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

router.post('/books', asyncHandler(async (req, res) => {
    const { title, author_id, isbn, genre_ids, initial_copies } = req.body;
    // Basic validation still useful here but could rely on backend
    if (!title || !isbn) {
        // Manually throw object to be caught by handler if desired, 
        // OR just return custom error.
        // For consistency, let's keep basic HTTP valid here:
        return res.status(400).json({ error: { code: "INVALID_ARGUMENT", message: "Missing title or isbn" } });
    }

    const grpcRequest = {
        title,
        author_id,
        isbn,
        genre_ids: genre_ids || [],
        initial_copies: parseInt(initial_copies) || 0
    };

    const response = await grpcAsync(client, 'CreateBook', grpcRequest, req);
    res.status(201).json(response);
}));

router.put('/books/:id', asyncHandler(async (req, res) => {
    const { id } = req.params;
    const { title, author_id, isbn, genre_ids } = req.body;
    const response = await grpcAsync(client, 'UpdateBook', { id, title, author_id, isbn, genre_ids: genre_ids || [] }, req);
    res.json(response);
}));

// --- Copies ---
router.post('/books/:id/copies', asyncHandler(async (req, res) => {
    const response = await grpcAsync(client, 'AddBookCopy', { book_id: req.params.id }, req);
    res.status(201).json(response);
}));

router.get('/books/:id/copies', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListBookCopies', { book_id: req.params.id, page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

// --- Members ---
router.post('/members', asyncHandler(async (req, res) => {
    const { name, email } = req.body;
    const response = await grpcAsync(client, 'CreateMember', { name, email }, req);
    res.status(201).json(response);
}));

router.put('/members/:id', asyncHandler(async (req, res) => {
    const { id } = req.params;
    const { name, email } = req.body;
    const response = await grpcAsync(client, 'UpdateMember', { id, name, email }, req);
    res.json(response);
}));

router.get('/members', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListMembers', { page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

// --- Loans ---
router.post('/borrow', asyncHandler(async (req, res) => {
    const { member_id, book_id, copy_id } = req.body;
    const response = await grpcAsync(client, 'BorrowBook', { member_id, book_id, copy_id }, req);
    res.json(response);
}));

router.post('/return', asyncHandler(async (req, res) => {
    const { loan_id } = req.body;
    const response = await grpcAsync(client, 'ReturnBook', { loan_id }, req);
    res.json(response);
}));

router.get('/loans', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListAllLoans', { page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

router.get('/loans/:member_id', asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const response = await grpcAsync(client, 'ListMemberLoans', { member_id: req.params.member_id, page: parseInt(page), limit: parseInt(limit) }, req);
    res.json(response);
}));

module.exports = router;
