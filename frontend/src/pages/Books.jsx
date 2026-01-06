import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { toast } from 'react-toastify';
import BookForm from '../components/BookForm';
import { FaEdit, FaBookOpen } from 'react-icons/fa';
import GenericTable from '../components/GenericTable';

const Books = () => {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [totalPages, setTotalPages] = useState(1);
    const [page, setPage] = useState(1);
    const [authors, setAuthors] = useState([]);
    const [genres, setGenres] = useState([]);

    // Form and Editing State
    const [showForm, setShowForm] = useState(false);
    const [editingBook, setEditingBook] = useState(null);

    const fetchBooks = async (currentPage = 1) => {
        setLoading(true);
        try {
            const response = await api.books.list({ page: currentPage, limit: 10 });
            if (response.books) {
                setBooks(response.books);
                setTotalPages(response.total_pages);
            } else if (Array.isArray(response)) {
                setBooks(response);
            }
        } catch (error) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    const fetchDependencies = async () => {
        try {
            const [authorsData, genresData] = await Promise.all([
                api.authors.list(),
                api.genres.list()
            ]);
            setAuthors(authorsData.authors || authorsData);
            setGenres(genresData.genres || genresData);
        } catch (error) {
            console.error("Failed to load dropdowns", error);
            toast.error("Failed to load dependency data");
        }
    };

    useEffect(() => {
        fetchBooks(page);
    }, [page]);

    useEffect(() => {
        fetchDependencies();
    }, []);

    const handleEditClick = (book) => {
        setEditingBook(book);
        setShowForm(true);
    };

    const handleFormSubmitSuccess = () => {
        fetchBooks(page);
        setShowForm(false);
        setEditingBook(null);
    };

    const handleFormCancel = () => {
        setShowForm(false);
        setEditingBook(null);
    };

    const columns = [
        {
            header: "Book Details",
            render: (book) => (
                <div>
                    <div className="font-medium text-gray-900">{book.title}</div>
                    <div className="text-sm text-gray-500">ISBN: {book.isbn}</div>
                    {book.author && <div className="text-sm text-gray-500">By {book.author.name}</div>}
                </div>
            )
        },
        {
            header: "Genres",
            render: (book) => (
                <div className="flex flex-wrap gap-1">
                    {book.genres && book.genres.map(g => (
                        <span key={g.id} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                            {g.name}
                        </span>
                    ))}
                </div>
            )
        },
        {
            header: "Availability",
            render: (book) => (
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${book.available_copies > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {book.available_copies} / {book.total_copies} Left
                </span>
            )
        }
    ];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
                    <FaBookOpen className="text-indigo-600" /> Books
                </h1>
                <button
                    onClick={() => {
                        if (showForm) handleFormCancel();
                        else setShowForm(true);
                    }}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                >
                    {showForm ? 'Close Form' : 'Add New Book'}
                </button>
            </div>

            {showForm && (
                <div className="mb-8">
                    <BookForm
                        onBookCreated={handleFormSubmitSuccess}
                        authors={authors}
                        genres={genres}
                        initialData={editingBook}
                        onCancel={handleFormCancel}
                    />
                </div>
            )}

            <GenericTable
                columns={columns}
                data={books}
                loading={loading}
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
                actions={(book) => (
                    <div className="flex justify-end space-x-2">
                        <button
                            onClick={() => handleEditClick(book)}
                            className="text-indigo-600 hover:text-indigo-900"
                            title="Edit"
                        >
                            <FaEdit size={18} />
                        </button>
                    </div>
                )}
            />
        </div>
    );
};

export default Books;
