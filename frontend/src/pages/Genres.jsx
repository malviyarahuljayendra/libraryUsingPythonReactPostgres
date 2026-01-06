import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { toast } from 'react-toastify';

const Genres = () => {
    const [genres, setGenres] = useState([]);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [name, setName] = useState('');

    const fetchGenres = async (currPage = 1) => {
        try {
            const response = await api.genres.list({ page: currPage, limit: 10 });
            if (response.genres) {
                setGenres(response.genres);
                setTotalPages(response.total_pages);
            } else if (Array.isArray(response)) {
                setGenres(response);
            }
        } catch (error) {
            toast.error(error.message);
        }
    };

    useEffect(() => {
        fetchGenres(page);
    }, [page]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.genres.create({ name });
            toast.success("Genre added!");
            setName('');
            fetchGenres(page);
        } catch (error) {
            toast.error(error.message);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Genres</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="md:col-span-1">
                    <div className="bg-white shadow rounded-lg p-6">
                        <h2 className="text-xl font-semibold mb-4">Add Genre</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <input
                                type="text"
                                placeholder="Name"
                                required
                                className="w-full border rounded p-2"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                            <button type="submit" className="w-full bg-indigo-600 text-white p-2 rounded hover:bg-indigo-700">Add</button>
                        </form>
                    </div>
                </div>

                <div className="md:col-span-2">
                    <div className="bg-white shadow rounded-lg overflow-hidden">
                        <ul className="divide-y divide-gray-200">
                            {genres.map(g => (
                                <li key={g.id} className="p-4 hover:bg-gray-50">
                                    <div className="font-bold">{g.name}</div>
                                </li>
                            ))}
                        </ul>
                        <div className="p-4 bg-gray-50 border-t flex justify-between">
                            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="px-3 py-1 border rounded disabled:opacity-50">Prev</button>
                            <span>Page {page} of {totalPages}</span>
                            <button onClick={() => setPage(p => (page < totalPages ? p + 1 : p))} disabled={page >= totalPages} className="px-3 py-1 border rounded disabled:opacity-50">Next</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Genres;
