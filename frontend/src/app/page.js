"use client"; // ✅ Ensure this is a Client Component

import { useState, useEffect } from "react";

export default function Home() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!query) {
            setResults([]);
            setSuggestions([]);
            return;
        }

        const delayDebounce = setTimeout(() => {
            handleSearch();
            fetchSuggestions();
        }, 500); // ✅ Wait 500ms before making the API call

        return () => clearTimeout(delayDebounce); // Cleanup timeout
    }, [query]);
    
    const fetchSuggestions = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/suggest/?q=${query}`);
            if (!response.ok) throw new Error("Failed to fetch suggestions");
            const data = await response.json();
            setSuggestions(data.suggestions);
        }
        catch (err) {
            console.error("Suggestion error:", err);
        }
    }

    const handleSearch = async () => {
        setLoading(true);
        setError("");

        try {
            const response = await fetch(`http://127.0.0.1:8000/search/?q=${query}&top_k=5`);
            if (!response.ok) throw new Error("Failed to fetch results");
            
            const data = await response.json();
            setResults(data.results);
        } catch (err) {
            setError("Something went wrong. Try again.");
            console.error("Search error:", err);
        }

        setLoading(false);
    };

    const selectSuggestion = (suggestion) => {
        setQuery(suggestion);
        setSuggestions([]);
        handleSearch();
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-100">
            <h1 className="text-3xl font-bold mb-4">AI-Powered Search</h1>
            
            <input
                type="text"
                placeholder="Search for AI topics..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="p-2 border rounded-md w-80"
            />

            {suggestions.length > 0 && (
                <ul className="absolute bg-white border mt-1 w-80 rounded-md shadow-md">
                    {suggestions.map((suggestion, index) => (
                        <li
                            key={index}
                            className="p-2 hover:bg-gray-200 cursor-pointer"
                            onClick={() => selectSuggestion(suggestion)}
                        >
                            {suggestion}
                        </li>
                    ))}
                </ul>
            )}

            {loading && <p className="mt-2 text-gray-600">🔄 Searching...</p>}
            {error && <p className="mt-2 text-red-500">{error}</p>}

            {results.length > 0 && (
                <div className="mt-4 w-80">
                    <h2 className="text-xl font-semibold">Results:</h2>
                    <ul className="mt-2">
                        {results.map((res, index) => (
                            <li key={index} className="p-2 border rounded-md mb-2 bg-white">
                                <strong>ID:</strong> {res.id} <br />
                                <strong>Score:</strong> {res.score.toFixed(2)}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
