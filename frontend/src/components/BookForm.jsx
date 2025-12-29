import React, { useState } from 'react';
import { api } from '../api';

const BookForm = ({ onBookCreated, authors, genres }) => {
    const [title, setTitle] = useState('');
    const [authorId, setAuthorId] = useState('');
    const [isbn, setIsbn] = useState('');
    const [copies, setCopies] = useState(1);
    const [selectedGenreIds, setSelectedGenreIds] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!title.trim()) { alert('Please enter a book title.'); return; }
        if (!authorId) { alert('Please select an author.'); return; }
        if (!isbn.trim()) { alert('Please enter an ISBN.'); return; }
        if (parseInt(copies) < 1) { alert('Initial copies must be at least 1.'); return; }
        if (selectedGenreIds.length === 0) { alert('Please select at least one genre.'); return; }

        try {
            await api.books.create({
                title: title.trim(),
                author_id: authorId,
                isbn: isbn.trim(),
                genre_ids: selectedGenreIds,
                initial_copies: parseInt(copies) || 1
            });

            setTitle('');
            setAuthorId('');
            setIsbn('');
            setCopies(1);
            setSelectedGenreIds([]);
            if (onBookCreated) onBookCreated();
        } catch (error) {
            console.error('Error creating book:', error);
            alert(`Error: ${error.message}`);
        }
    };

    const handleGenreChange = (genreId) => {
        setSelectedGenreIds(prev =>
            prev.includes(genreId)
                ? prev.filter(id => id !== genreId)
                : [...prev, genreId]
        );
    };

    return (
        <div className="bg-white shadow rounded-lg p-6 mb-6 border border-gray-100">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Add New Book</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Title</label>
                    <input
                        type="text"
                        required
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                        placeholder="Harry Potter..."
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Author</label>
                    <select
                        required
                        value={authorId}
                        onChange={(e) => setAuthorId(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    >
                        <option value="">Select an Author</option>
                        {authors.map(author => (
                            <option key={author.id} value={author.id}>{author.name}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">ISBN</label>
                    <input
                        type="text"
                        required
                        value={isbn}
                        onChange={(e) => setIsbn(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                        placeholder="ISBN-12345"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Initial Copies</label>
                    <input
                        type="number"
                        min="1"
                        required
                        value={copies}
                        onChange={(e) => setCopies(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Genres</label>
                    <div className="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto p-2 border rounded-md">
                        {genres.map(genre => (
                            <label key={genre.id} className="flex items-center space-x-2 text-sm text-gray-600">
                                <input
                                    type="checkbox"
                                    checked={selectedGenreIds.includes(genre.id)}
                                    onChange={() => handleGenreChange(genre.id)}
                                    className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                                />
                                <span>{genre.name}</span>
                            </label>
                        ))}
                    </div>
                </div>
                <button
                    type="submit"
                    className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                >
                    Add Book
                </button>
            </form>
        </div>
    );
};

export default BookForm;
