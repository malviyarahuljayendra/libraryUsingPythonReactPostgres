import React from 'react';

const BookList = ({ books }) => {
    return (
        <div className="bg-white shadow rounded-lg p-6 border border-gray-100">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Available Books</h2>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Author</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Genres</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISBN</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {books.length === 0 ? (
                            <tr>
                                <td colSpan="5" className="px-6 py-4 text-center text-sm text-gray-500 italic">No books found.</td>
                            </tr>
                        ) : (
                            books.map((book) => (
                                <tr key={book.id} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">{book.title}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                        {book.author ? book.author.name : 'Unknown'}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-xs text-gray-500">
                                        <div className="flex flex-wrap gap-1">
                                            {book.genres && book.genres.length > 0 ? (
                                                book.genres.map(g => (
                                                    <span key={g.id} className="bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full border border-blue-100">
                                                        {g.name}
                                                    </span>
                                                ))
                                            ) : (
                                                <span className="text-gray-400">-</span>
                                            )}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{book.isbn}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex flex-col">
                                            <span className={`text-sm font-bold ${book.available_copies > 0 ? 'text-green-600' : 'text-red-500'}`}>
                                                {book.available_copies} / {book.total_copies}
                                            </span>
                                            <span className="text-xs text-gray-400">available</span>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default BookList;
