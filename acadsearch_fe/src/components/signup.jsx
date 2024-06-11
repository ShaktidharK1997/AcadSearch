import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Signup() {
    const [userDetails, setuserDetails] = useState({
        email : '',
        password : '',
        name : '',
        institution : '',
        dob : ''
    });

    const navigate = useNavigate();
    const base_url = `${window.location.protocol}//${window.location.hostname}:8000`;

    const handleSignup = async () => {
        const apiUrl = `${base_url}/AcadSearch/signup/`;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: userDetails.email,
                    password: userDetails.password,
                    name : userDetails.name,
                    institution : userDetails.institution,
                    dob : userDetails.dob
                })
            });

            if (response.ok) {
                navigate('/signin');
            } else {
                alert('Invalid credentials');
            }
        } catch (error) {
            console.error('Error during sign-up:', error);
        }
    }

    return (
        <div>
            <h2>Sign Up</h2>
            <form onSubmit={e => { e.preventDefault(); handleSignup(); }}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={userDetails.email}
                        onChange={e => setuserDetails({...userDetails, email : e.target.value})}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={userDetails.password}
                        onChange={e => setuserDetails({...userDetails, password : e.target.value})}
                        required
                    />
                </div>
                <div>
                    <label>Name:</label>
                    <input
                        type="text"
                        value={userDetails.name}
                        onChange={e => setuserDetails({...userDetails, name : e.target.value})}
                        required
                    />
                </div>
                <div>
                    <label>Institution:</label>
                    <input
                        type="text"
                        value={userDetails.institution}
                        onChange={e => setuserDetails({...userDetails, institution : e.target.value})}
                        required
                    />
                </div>
                <div>
                    <label>Date of Birth:</label>
                    <input
                        type="date"
                        value={userDetails.dob}
                        onChange={e => setuserDetails({...userDetails, dob : e.target.value})}
                        required
                    />
                </div>
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}