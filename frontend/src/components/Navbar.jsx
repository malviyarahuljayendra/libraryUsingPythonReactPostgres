import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'bg-indigo-700 text-white' : 'text-gray-300 hover:bg-indigo-700 hover:text-white';
    };

    return (
        <nav className="bg-indigo-800 shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="flex-shrink-0 text-white font-bold text-xl">
                            Library Sys
                        </Link>
                        <div className="hidden md:block">
                            <div className="ml-10 flex items-baseline space-x-4">
                                <Link to="/" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/')}`}>
                                    Dashboard
                                </Link>
                                <Link to="/books" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/books')}`}>
                                    Books
                                </Link>
                                <Link to="/members" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/members')}`}>
                                    Members
                                </Link>
                                <Link to="/authors" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/authors')}`}>
                                    Authors
                                </Link>
                                <Link to="/genres" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/genres')}`}>
                                    Genres
                                </Link>
                                <Link to="/loans" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/loans')}`}>
                                    Loans
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
