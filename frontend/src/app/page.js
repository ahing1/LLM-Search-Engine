"use client";

import { useState } from "react";

export default function Home() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query) return;
        setLoading(true);
        
        try {
            console.log("Query:", query);
            const response = await fetch(`http://127.0.0.1:8000/search/?q=${query}&top_k=5`);
            const data = await response.json();
            console.log("Data:", data);
            setResults(data.results);
        } catch (error) {
            console.error("Search error:", error);
        }

        setLoading(false);
    };

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
            <button
                onClick={handleSearch}
                className="mt-2 p-2 bg-blue-500 text-white rounded-md"
                disabled={loading}
            >
                {loading ? "Searching..." : "Search"}
            </button>

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
