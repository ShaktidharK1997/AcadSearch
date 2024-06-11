import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Signin() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const base_url = `${window.location.protocol}//${window.location.hostname}:8000`;

    const handleSignin = async () => {
        setLoading(true);
        const apiUrl = `${base_url}/AcadSearch/signin/`;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            setLoading(false);

            if (response.ok) {
                const data = await response.json();
                // Store the token securely, consider using httpOnly cookies
                localStorage.setItem('authToken', data.token); 
                navigate('/search');
            } else {
                alert('Invalid credentials');
            }
        } catch (error) {
            setLoading(false);
            console.error('Error during sign-in:', error);
        }
    };

    return (
        <div>
            <h2>Sign In</h2>
            <form onSubmit={e => { e.preventDefault(); handleSignin(); }}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Signing in...' : 'Sign In'}
                </button>
                <button onClick={() => navigate('/signup')}>Sign Up</button>
            </form>
        </div>
    );
}



