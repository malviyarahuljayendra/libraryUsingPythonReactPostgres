import React, { useState } from 'react';
import { api } from '../api';

const BorrowForm = ({ books, members, onBorrow }) => {
    const [selectedBook, setSelectedBook] = useState('');
    const [selectedMember, setSelectedMember] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedMember) {
            alert('Please select a member.');
            return;
        }
        if (!selectedBook) {
            alert('Please select a book.');
            return;
        }

        try {
            await api.loans.borrow({ book_id: selectedBook, member_id: selectedMember });
            alert('Book borrowed successfully!');
            setSelectedBook('');
            setSelectedMember('');
            if (onBorrow) onBorrow();
        } catch (error) {
            console.error('Error borrowing book:', error);
            alert(`Error: ${error.message}`);
        }
    };


    return (
        <div className="bg-white shadow rounded-lg p-6 mb-6 border border-gray-100">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Borrow Book</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 font-semibold mb-1">Select Member</label>
                    <select
                        value={selectedMember}
                        onChange={(e) => setSelectedMember(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2 bg-gray-50"
                        required
                    >
                        <option value="">-- Choose Member --</option>
                        {members.map((m) => (
                            <option key={m.id} value={m.id}>{m.name} ({m.email})</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 font-semibold mb-1">Select Book</label>
                    <select
                        value={selectedBook}
                        onChange={(e) => setSelectedBook(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2 bg-gray-50"
                        required
                    >
                        <option value="">-- Choose Book --</option>
                        {books.map((b) => (
                            <option
                                key={b.id}
                                value={b.id}
                                disabled={b.available_copies === 0}
                            >
                                {b.title} {b.author ? `by ${b.author.name}` : ''} ({b.available_copies} left) {b.available_copies === 0 ? '- OUT OF STOCK' : ''}
                            </option>
                        ))}
                    </select>
                </div>
                <button
                    type="submit"
                    className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                >
                    Borrow Book
                </button>
            </form>
        </div>
    );
};

export default BorrowForm;
