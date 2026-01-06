import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { toast } from 'react-toastify';
import GenericTable from '../components/GenericTable';
import BorrowForm from '../components/BorrowForm';
import { FaBookReader } from 'react-icons/fa';

const Loans = () => {
    const [loans, setLoans] = useState([]);
    const [loading, setLoading] = useState(false);
    const [actionLoading, setActionLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    const [showBorrowForm, setShowBorrowForm] = useState(false);
    const [books, setBooks] = useState([]);
    const [members, setMembers] = useState([]);
    const [filterMemberId, setFilterMemberId] = useState('');

    const fetchLoans = async (currentPage = 1) => {
        setLoading(true);
        try {
            let response;
            if (filterMemberId) {
                response = await api.loans.listMemberLoans(filterMemberId, { page: currentPage, limit: 10 });
            } else {
                response = await api.loans.listAll({ page: currentPage, limit: 10 });
            }

            if (response.loans) {
                setLoans(response.loans);
                setTotalPages(response.total_pages);
            } else {
                setLoans([]);
                setTotalPages(0); // Reset pages if no data
            }
        } catch (error) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    const fetchDependencies = async () => {
        try {
            const [booksRes, membersRes] = await Promise.all([
                api.books.list({ limit: 100 }), // Fetch more for dropdown
                api.members.list({ limit: 100 })
            ]);
            setBooks(booksRes.books || []);
            setMembers(membersRes.members || []);
        } catch (error) {
            console.error("Failed to load dependencies", error);
        }
    };

    useEffect(() => {
        fetchLoans(page);
    }, [page, filterMemberId]); // Refetch when page or filter changes

    useEffect(() => {
        // Load members for filter dropdown and mapping
        const loadMembers = async () => {
            try {
                const res = await api.members.list({ limit: 100 });
                setMembers(res.members || []);
            } catch (e) {
                console.error("Failed to load members", e);
            }
        };
        loadMembers();
    }, []);

    useEffect(() => {
        if (showBorrowForm) {
            fetchDependencies();
        }
    }, [showBorrowForm]);

    const handleReturn = async (loan) => {
        console.log("handleReturn function called", loan);
        // Removed window.confirm as it is blocked in some environments

        setActionLoading(true);
        toast.info("Processing return...");
        try {
            await api.loans.returnBook({ loan_id: loan.id });
            toast.success("Book returned successfully");
            fetchLoans(page);
        } catch (error) {
            toast.error(error.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleBorrowSuccess = () => {
        setShowBorrowForm(false);
        fetchLoans(page);
    };

    const columns = [
        { header: "Book Title", accessor: "book_title" },
        {
            header: "Member Name",
            accessor: "member_name"
        },
        {
            header: "Member Email",
            accessor: "member_email"
        },
        { header: "Borrowed At", render: (l) => new Date(l.borrowed_at).toLocaleDateString() },
        {
            header: "Status",
            render: (l) => (
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${l.returned_at ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {l.returned_at ? 'Returned' : 'Active'}
                </span>
            )
        }
    ];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
                    <FaBookReader className="text-indigo-600" /> Loans Management
                </h1>

                <div className="flex items-center gap-4">
                    <select
                        value={filterMemberId}
                        onChange={(e) => {
                            setFilterMemberId(e.target.value);
                            setPage(1); // Reset to first page on filter change
                        }}
                        className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    >
                        <option value="">All Members</option>
                        {members.map(m => (
                            <option key={m.id} value={m.id}>{m.name}</option>
                        ))}
                    </select>
                    <button
                        onClick={() => setShowBorrowForm(!showBorrowForm)}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                    >
                        {showBorrowForm ? 'Cancel Borrow' : 'Borrow Book'}
                    </button>
                </div>
            </div>

            {showBorrowForm && (
                <div className="mb-8">
                    <BorrowForm books={books} members={members} onBorrow={handleBorrowSuccess} />
                </div>
            )}

            <GenericTable
                columns={columns}
                data={loans}
                loading={loading}
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
                actions={(loan) => (
                    !loan.returned_at && (
                        <button
                            type="button"
                            onClick={(e) => {
                                e.stopPropagation();
                                console.log("Return clicked for:", loan);
                                handleReturn(loan);
                            }}
                            disabled={actionLoading}
                            className="bg-red-100 text-red-700 hover:bg-red-200 text-xs font-bold py-1 px-3 rounded cursor-pointer hover:underline relative z-10 pointer-events-auto"
                        >
                            Return
                        </button>
                    )
                )}
            />
        </div>
    );
};

export default Loans;
