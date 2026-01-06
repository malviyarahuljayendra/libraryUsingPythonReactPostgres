import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { Link } from 'react-router-dom';
import { FaBook, FaUsers, FaPenNib, FaTags } from 'react-icons/fa';

const StatCard = ({ title, count, icon, link, color }) => (
    <Link to={link} className={`bg-white overflow-hidden shadow rounded-lg p-5 hover:shadow-md transition duration-300 border-l-4 ${color}`}>
        <div className="flex items-center">
            <div className={`flex-shrink-0 p-3 rounded-md ${color.replace('border-', 'bg-').replace('500', '100')}`}>
                {React.cloneElement(icon, { className: `h-6 w-6 ${color.replace('border-', 'text-')}` })}
            </div>
            <div className="ml-5 w-0 flex-1">
                <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
                    <dd>
                        <div className="text-lg font-medium text-gray-900">{count !== null ? count : '-'}</div>
                    </dd>
                </dl>
            </div>
        </div>
    </Link>
);

const Dashboard = () => {
    const [stats, setStats] = useState({
        books: null,
        members: null,
        authors: null,
        genres: null
    });

    useEffect(() => {
        const fetchStats = async () => {
            // Fetch page 1 of each to get total_count
            try {
                const [books, members, authors, genres] = await Promise.all([
                    api.books.list({ limit: 1 }),
                    api.members.list({ limit: 1 }),
                    api.authors.list({ limit: 1 }),
                    api.genres.list({ limit: 1 })
                ]);

                setStats({
                    books: books.total_count,
                    members: members.total_count,
                    authors: authors.total_count,
                    genres: genres.total_count
                });
            } catch (e) {
                console.error("Failed to fetch stats", e);
            }
        };
        fetchStats();
    }, []);

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">Dashboard</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard title="Total Books" count={stats.books} icon={<FaBook />} link="/books" color="border-indigo-500" />
                <StatCard title="Members" count={stats.members} icon={<FaUsers />} link="/members" color="border-green-500" />
                <StatCard title="Authors" count={stats.authors} icon={<FaPenNib />} link="/authors" color="border-purple-500" />
                <StatCard title="Genres" count={stats.genres} icon={<FaTags />} link="/genres" color="border-yellow-500" />
            </div>

            <div className="mt-12 bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-800">Quick Actions</h2>
                <div className="flex space-x-4">
                    <Link to="/books" className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">Manage Books</Link>
                    <Link to="/members" className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Manage Members</Link>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
