const API_URL = import.meta.env.VITE_API_URL;

const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'API request failed');
    }
    return response.json();
};

export const api = {
    books: {
        list: () => fetch(`${API_URL}/api/books`).then(handleResponse),
        create: (data) => fetch(`${API_URL}/api/books`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(handleResponse),
    },
    members: {
        list: () => fetch(`${API_URL}/api/members`).then(handleResponse),
        create: (data) => fetch(`${API_URL}/api/members`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(handleResponse),
    },
    authors: {
        list: () => fetch(`${API_URL}/api/authors`).then(handleResponse),
    },
    genres: {
        list: () => fetch(`${API_URL}/api/genres`).then(handleResponse),
    },
    loans: {
        borrow: (data) => fetch(`${API_URL}/api/borrow`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(handleResponse),
    },
};
