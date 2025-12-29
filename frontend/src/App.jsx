import React, { useEffect, useState } from 'react';
import BookList from './components/BookList';
import BookForm from './components/BookForm';
import BorrowForm from './components/BorrowForm';
import { api } from './api';

function App() {
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [authors, setAuthors] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [booksData, membersData, authorsData, genresData] = await Promise.all([
        api.books.list(),
        api.members.list(),
        api.authors.list(),
        api.genres.list()
      ]);

      setBooks(booksData);
      setMembers(membersData);
      setAuthors(authorsData);
      setGenres(genresData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-extrabold text-gray-900 text-center mb-10">
          Library Management System
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-6">
            <BookForm onBookCreated={fetchData} authors={authors} genres={genres} />
            <BorrowForm books={books} members={members} onBorrow={fetchData} />
          </div>

          <div>
            <BookList books={books} />
          </div>
        </div>

        {loading && (
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
            <div className="text-white text-xl">Loading...</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
