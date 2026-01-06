import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { toast } from 'react-toastify';

const BookForm = ({ onBookCreated, authors, genres, initialData = null, onCancel }) => {
    const [title, setTitle] = useState('');
    const [authorId, setAuthorId] = useState('');
    const [isbn, setIsbn] = useState('');
    const [copies, setCopies] = useState(1);
    const [selectedGenreIds, setSelectedGenreIds] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (initialData) {
            setTitle(initialData.title);
            setAuthorId(initialData.author?.id || '');
            setIsbn(initialData.isbn);
            setCopies(initialData.total_copies || 0); // Note: total_copies might not be editable safely without check, but fine for now
            setSelectedGenreIds(initialData.genres ? initialData.genres.map(g => g.id) : []);
        }
    }, [initialData]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        if (!title.trim()) { toast.error('Please enter a book title.'); setLoading(false); return; }
        if (!authorId) { toast.error('Please select an author.'); setLoading(false); return; }
        if (!isbn.trim()) { toast.error('Please enter an ISBN.'); setLoading(false); return; }

        // Only validate copies on create for now, unless we want to allow updating totals
        // if (parseInt(copies) < 1) { toast.error('Initial copies must be at least 1.'); setLoading(false); return; }

        if (selectedGenreIds.length === 0) { toast.error('Please select at least one genre.'); setLoading(false); return; }

        try {
            const payload = {
                title: title.trim(),
                author_id: authorId,
                isbn: isbn.trim(),
                genre_ids: selectedGenreIds,
                initial_copies: parseInt(copies) || 0
            };

            if (initialData) {
                // Update
                await api.books.update(initialData.id, payload);
                toast.success("Book updated successfully");
            } else {
                // Create
                await api.books.create(payload);
                toast.success("Book created successfully");
            }

            // Reset form
            setTitle('');
            setAuthorId('');
            setIsbn('');
            setCopies(1);
            setSelectedGenreIds([]);

            if (onBookCreated) onBookCreated();
        } catch (error) {
            console.error('Error saving book:', error);
            toast.error(error.message);
        } finally {
            setLoading(false);
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
            <h2 className="text-xl font-bold mb-4 text-gray-800">{initialData ? 'Edit Book' : 'Add New Book'}</h2>
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
                {!initialData && (
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
                )}
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
                <div className="flex gap-4">
                    <button
                        type="submit"
                        disabled={loading}
                        className={`flex-1 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                        {loading ? 'Saving...' : (initialData ? 'Update Book' : 'Add Book')}
                    </button>
                    {onCancel && (
                        <button
                            type="button"
                            onClick={onCancel}
                            disabled={loading}
                            className="flex-1 inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                        >
                            Cancel
                        </button>
                    )}
                </div>
            </form>
        </div>
    );
};

export default BookForm;
