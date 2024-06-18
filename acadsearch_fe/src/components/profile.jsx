import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Profile() {
    const [userDetails, setuserDetails] = useState({
        email : '',
        password : '',
        name : '',
        institution : '',
        dob : ''
    });

    const user = localStorage.getItem('user') ? (localStorage.getItem('user')) : null;

    const navigate = useNavigate();
    const base_url = `${window.location.protocol}//${window.location.hostname}:8000`;

    const handleProfile = async () => {
        const apiUrl = `${base_url}/AcadSearch/profile/?user=${user}`;

        try {
            const response = await fetch(apiUrl, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${localStorage.getItem('authToken')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setuserDetails(data);
            } else {
                alert('Invalid credentials');
            }
        } catch (error) {
            console.error('Error during fetching profile:', error);
        }
    }

    useEffect(() => {
        handleProfile();
    }, []);

    return (
        <div>
            <h2>My Profile</h2>
            <div>
                <label>Email:</label>
                <input
                    type="email"
                    value={userDetails.email}
                    readOnly
                />
            </div>
            <div>
                <label>Name:</label>
                <input
                    type="text"
                    value={userDetails.name}
                    readOnly
                />
            </div>
            <div>
                <label>Institution:</label>
                <input
                    type="text"
                    value={userDetails.institution}
                    readOnly
                />
            </div>
            <div>
                <label>Date of Birth:</label>
                <input
                    type="date"
                    value={userDetails.dob}
                    readOnly
                />
            </div>
        </div>
    );
}