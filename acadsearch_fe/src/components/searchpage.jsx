import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './searchpage.css';

export default function SearchPage() {

    const [searchResults, setSearchResults] = useState([]);
    const base_url = `${window.location.protocol}//${window.location.hostname}:8000`;
    const [query, setQuery] = useState('');

    const storedUser = localStorage.getItem('user');
    const user = storedUser && storedUser !== 'undefined' ? JSON.parse(storedUser) : null;

    const handleSearch = async () => {
        const apiUrl = `${base_url}/AcadSearch/search/?query=${query}`;

        try {
            const response = await fetch(apiUrl);
            const data = await response.json();
            setSearchResults(data.results);
        } catch (error) {
            console.error(error);
        }
    };

    const navigate = useNavigate();

    const handleSignin = () => {
        navigate('/signin');
    }

    const handleProfile = () => {
        navigate('/profile');
    }

    return (
        <div className='search-page'>
            <div className='header'>
                <h1>AcadSearch</h1>

                {user ? (
                    <button className='profile-button' onClick={handleProfile}>
                        My Profile
                    </button>
                ) : (
                    <button className='signin-button' onClick={handleSignin}>
                        Sign In
                    </button>
                )}
            </div>
            <div className='search-container'>
                <input
                    className='search-input'
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search papers..."
                />

                <button className='search-button' onClick={handleSearch}>Search</button>
            </div>
            <div className='results-container'>
                {searchResults.length > 0 ? (
                    searchResults.map((paper, index) => (
                        <div key={index} className="paper">
                            <h4>
                                {paper.title}
                            </h4>
                            <p><strong>Authors:</strong> {paper.authors.map(author => author.name).join(', ')}</p>
                            <p><strong>Citations:</strong> {paper.citationCount === 0 ? 'Not Available' : paper.citationCount}</p>
                            <p><strong>Year:</strong> {paper.year}</p>
                        </div>
                    ))
                ) : (
                    <p>One Stop portal for searching anything academic!</p>
                )}
            </div>
        </div>
    );
}
