const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

const generateUUID = () => {
    // Check if crypto APIs are available (Secure Context)
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
        return crypto.randomUUID();
    }
    // Fallback for non-secure contexts
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
};

const fetchWithContext = (url, options = {}) => {
    const headers = options.headers || {};
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    // Inject Request ID
    headers['X-Request-ID'] = generateUUID();

    return fetch(url, {
        ...options,
        headers
    });
};

const handleResponse = async (response) => {
    if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        let errorMessage = `API Request failed: ${response.statusText}`;

        if (payload.error) {
            if (typeof payload.error === 'object' && payload.error.message) {
                // New structured error: { error: { code, message, ... } }
                errorMessage = payload.error.message;
            } else if (typeof payload.error === 'string') {
                // Legacy or simple error: { error: "message" }
                errorMessage = payload.error;
            }
        }

        throw new Error(errorMessage);
    }
    return response.json();
};

const getQueryString = (params) => {
    if (!params) return '';
    const query = new URLSearchParams(params);
    return `?${query.toString()}`;
};

export const api = {
    books: {
        list: (params) => fetchWithContext(`${API_URL}/api/books${getQueryString(params)}`).then(handleResponse),
        create: (data) => fetchWithContext(`${API_URL}/api/books`, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then(handleResponse),
        update: (id, data) => fetchWithContext(`${API_URL}/api/books/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        }).then(handleResponse),
        addCopy: (id) => fetchWithContext(`${API_URL}/api/books/${id}/copies`, {
            method: 'POST',
        }).then(handleResponse),
        listCopies: (id, params) => fetchWithContext(`${API_URL}/api/books/${id}/copies${getQueryString(params)}`).then(handleResponse),
    },
    members: {
        list: (params) => fetchWithContext(`${API_URL}/api/members${getQueryString(params)}`).then(handleResponse),
        create: (data) => fetchWithContext(`${API_URL}/api/members`, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then(handleResponse),
        update: (id, data) => fetchWithContext(`${API_URL}/api/members/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        }).then(handleResponse),
    },
    authors: {
        list: (params) => fetchWithContext(`${API_URL}/api/authors${getQueryString(params)}`).then(handleResponse),
        create: (data) => fetchWithContext(`${API_URL}/api/authors`, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then(handleResponse),
    },
    genres: {
        list: (params) => fetchWithContext(`${API_URL}/api/genres${getQueryString(params)}`).then(handleResponse),
        create: (data) => fetchWithContext(`${API_URL}/api/genres`, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then(handleResponse),
    },
    loans: {
        borrow: (data) => fetchWithContext(`${API_URL}/api/borrow`, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then(handleResponse),
        returnBook: (data) => fetchWithContext(`${API_URL}/api/return`, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then(handleResponse),
        listMemberLoans: (memberId, params) => fetchWithContext(`${API_URL}/api/loans/${memberId}${getQueryString(params)}`).then(handleResponse),
        listAll: (params) => fetchWithContext(`${API_URL}/api/loans${getQueryString(params)}`).then(handleResponse),
    },
};

export default api;
