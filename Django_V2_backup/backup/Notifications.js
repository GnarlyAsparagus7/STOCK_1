// Django_V2/frontend/src/components/Notifications.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        const fetchNotifications = async () => {
            const response = await axios.get('http://127.0.0.1:8000/api/notifications/', {
                headers: {
                    Authorization: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5ODQ1MzUwLCJpYXQiOjE3Mjk4NDUwNTAsImp0aSI6ImRhODRlMjlhNDEwYzQ0YmRiNjAwM2UyNWNhMGRhZGJmIiwidXNlcl9pZCI6MTN9.L0s_n1fcfxlBWK48_FDiY3CLlRPWukBlM2f2m-NSYI8`,  // Include your token
                },
            });
            setNotifications(response.data);
        };
        fetchNotifications();
    }, []);

    return (
        <div>
            <h2>Notifications</h2>
            <ul>
                {notifications.map(notification => (
                    <li key={notification.id}>
                        {notification.message} - {new Date(notification.created_at).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

const markAsRead = async (id) => {
    await axios.patch(`http://127.0.0.1:8000/api/notifications/${id}/`, {}, {
        headers: {
            Authorization: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5ODQ1MzUwLCJpYXQiOjE3Mjk4NDUwNTAsImp0aSI6ImRhODRlMjlhNDEwYzQ0YmRiNjAwM2UyNWNhMGRhZGJmIiwidXNlcl9pZCI6MTN9.L0s_n1fcfxlBWK48_FDiY3CLlRPWukBlM2f2m-NSYI8`,
        },
    });
    // Refresh notifications after marking as read
};

export default Notifications;
