import React, { useEffect, useState } from 'react';

const OnlineUsers = () => {
    const [onlineUsers, setOnlineUsers] = useState([]);

    useEffect(() => {
        const base_url = `${window.location.protocol}//${window.location.hostname}:8000`;

        const fetchOnlineUsers = async () => {
            try {
                const response = await fetch(`${base_url}/AcadSearch/api/online-users/`, {
                    method: 'GET'
                });
                
                // Parse the JSON from the response
                const data = await response.json();
                
                // Set the online users from the parsed JSON data
                setOnlineUsers(data.online_users);
            } catch (error) {
                console.error("Error fetching online users:", error);
            }
        };
        
        fetchOnlineUsers(); // Initial fetch
        const interval = setInterval(fetchOnlineUsers, 6000); // Poll every minute

        return () => clearInterval(interval); // Clean up on unmount
    }, []);

    return (
        <div>
            <h3>Online Users</h3>
            <ul>
                {onlineUsers.map(user => (
                    <li key={user.username}>{user.username}</li>
                ))}
            </ul>
        </div>
    );
};

export default OnlineUsers;
