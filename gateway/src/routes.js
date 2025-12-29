const express = require('express');
const router = express.Router();
const client = require('./client');

// --- Authors ---
router.get('/authors', (req, res) => {
    client.ListAuthors({}, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response.authors);
    });
});

router.post('/authors', (req, res) => {
    const { name, bio } = req.body;
    client.CreateAuthor({ name, bio }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.status(201).json(response);
    });
});

// --- Genres ---
router.get('/genres', (req, res) => {
    client.ListGenres({}, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response.genres);
    });
});

router.post('/genres', (req, res) => {
    const { name } = req.body;
    client.CreateGenre({ name }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.status(201).json(response);
    });
});

// --- Books ---
router.get('/books', (req, res) => {
    client.ListBooks({}, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response.books);
    });
});

router.post('/books', (req, res) => {
    console.log("Gateway POST /books Body:", req.body);
    const { title, author_id, isbn, genre_ids, initial_copies } = req.body;
    if (!title || !isbn) {
        return res.status(400).json({ error: "Missing required fields (title, isbn)" });
    }

    const grpcRequest = {
        title,
        author_id,
        isbn,
        genre_ids: genre_ids || [],
        initial_copies: parseInt(initial_copies) || 0
    };
    console.log("Sending CreateBook to gRPC:", grpcRequest);

    client.CreateBook(grpcRequest, (err, response) => {
        if (err) {
            console.error("gRPC CreateBook Error:", err);
            if (err.code === 6) return res.status(409).json({ error: err.details });
            return res.status(500).json({ error: err.details });
        }
        res.status(201).json(response);
    });
});

router.put('/books/:id', (req, res) => {
    const { id } = req.params;
    const { title, author_id, isbn, genre_ids } = req.body;

    client.UpdateBook({ id, title, author_id, isbn, genre_ids: genre_ids || [] }, (err, response) => {
        if (err) {
            if (err.code === 5) return res.status(404).json({ error: err.details });
            if (err.code === 6) return res.status(409).json({ error: err.details });
            return res.status(500).json({ error: err.details });
        }
        res.json(response);
    });
});

// --- Copies ---
router.post('/books/:id/copies', (req, res) => {
    client.AddBookCopy({ book_id: req.params.id }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.status(201).json(response);
    });
});

router.get('/books/:id/copies', (req, res) => {
    client.ListBookCopies({ book_id: req.params.id }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response.copies);
    });
});

// --- Members ---
router.post('/members', (req, res) => {
    const { name, email } = req.body;
    client.CreateMember({ name, email }, (err, response) => {
        if (err) {
            if (err.code === 6) return res.status(409).json({ error: err.details });
            return res.status(500).json({ error: err.details });
        }
        res.status(201).json(response);
    });
});

router.put('/members/:id', (req, res) => {
    const { id } = req.params;
    const { name, email } = req.body;

    client.UpdateMember({ id, name, email }, (err, response) => {
        if (err) {
            if (err.code === 5) return res.status(404).json({ error: err.details });
            if (err.code === 6) return res.status(409).json({ error: err.details });
            return res.status(500).json({ error: err.details });
        }
        res.json(response);
    });
});

router.get('/members', (req, res) => {
    client.ListMembers({}, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response.members);
    });
});

// --- Loans ---
router.post('/borrow', (req, res) => {
    const { member_id, book_id, copy_id } = req.body;
    client.BorrowBook({ member_id, book_id, copy_id }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response);
    });
});

router.post('/return', (req, res) => {
    const { loan_id } = req.body;
    client.ReturnBook({ loan_id }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response);
    });
});

router.get('/loans/:member_id', (req, res) => {
    client.ListMemberLoans({ member_id: req.params.member_id }, (err, response) => {
        if (err) return res.status(500).json({ error: err.details });
        res.json(response.loans);
    });
});

module.exports = router;
