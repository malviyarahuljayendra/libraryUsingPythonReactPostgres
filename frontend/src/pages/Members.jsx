import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { toast } from 'react-toastify';
import { FaUserPlus, FaEdit } from 'react-icons/fa';
import GenericTable from '../components/GenericTable';

const Members = () => {
    const [members, setMembers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [actionLoading, setActionLoading] = useState(false);
    const [totalPages, setTotalPages] = useState(1);
    const [page, setPage] = useState(1);

    // Form State
    const [showForm, setShowForm] = useState(false);
    const [editingMember, setEditingMember] = useState(null);
    const [formData, setFormData] = useState({ name: '', email: '' });

    const fetchMembers = async (currentPage = 1) => {
        setLoading(true);
        try {
            const response = await api.members.list({ page: currentPage, limit: 10 });
            if (response.members) {
                setMembers(response.members);
                setTotalPages(response.total_pages);
            } else if (Array.isArray(response)) {
                setMembers(response);
            }
        } catch (error) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMembers(page);
    }, [page]);

    const handleEditClick = (member) => {
        setEditingMember(member);
        setFormData({ name: member.name, email: member.email });
        setShowForm(true);
    };

    const handleCancel = () => {
        setShowForm(false);
        setEditingMember(null);
        setFormData({ name: '', email: '' });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setActionLoading(true);
        try {
            if (editingMember) {
                await api.members.update(editingMember.id, formData);
                toast.success("Member updated successfully");
            } else {
                await api.members.create(formData);
                toast.success("Member created successfully");
            }
            handleCancel();
            fetchMembers(page);
        } catch (error) {
            toast.error(error.message);
        } finally {
            setActionLoading(false);
        }
    };

    const columns = [
        { header: "Name", accessor: "name" },
        { header: "Email", accessor: "email" }
    ];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Members</h1>
                <button
                    onClick={() => { handleCancel(); setShowForm(!showForm); }}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200 flex items-center gap-2"
                >
                    <FaUserPlus /> {showForm ? 'Close Form' : 'Add New Member'}
                </button>
            </div>

            {showForm && (
                <div className="mb-8 bg-white shadow-md rounded-lg p-6 max-w-lg mx-auto border border-indigo-100">
                    <h2 className="text-xl font-semibold mb-4">{editingMember ? 'Edit Member' : 'New Member'}</h2>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Name</label>
                            <input
                                type="text"
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email</label>
                            <input
                                type="email"
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            />
                        </div>
                        <div className="flex gap-4">
                            <button
                                type="submit"
                                disabled={actionLoading}
                                className={`flex-1 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${actionLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                            >
                                {actionLoading ? 'Saving...' : (editingMember ? 'Update Member' : 'Create Member')}
                            </button>
                            <button
                                type="button"
                                onClick={handleCancel}
                                disabled={actionLoading}
                                className="flex-1 flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            )}

            <GenericTable
                columns={columns}
                data={members}
                loading={loading}
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
                actions={(member) => (
                    <button
                        onClick={() => handleEditClick(member)}
                        className="text-indigo-600 hover:text-indigo-900 mx-2"
                        title="Edit Member"
                    >
                        <FaEdit size={18} />
                    </button>
                )}
            />
        </div>
    );
};

export default Members;
