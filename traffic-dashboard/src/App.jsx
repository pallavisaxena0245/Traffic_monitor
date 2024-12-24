import React, { useState, useEffect } from 'react';

function App() {
    const [requests, setRequests] = useState([]);

    useEffect(() => {
        // Fetch data from backend
        fetch('http://localhost:5000/api/requests')  // Update with your backend URL
            .then(response => response.json())
            .then(data => setRequests(data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div className="App">
            <h1>Traffic Monitoring Dashboard</h1>
            <table>
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>Method</th>
                        <th>Response Code</th>
                        <th>Test Result</th>
                        <th>Impact</th>
                        <th>Severity</th>
                    </tr>
                </thead>
                <tbody>
                    {requests.map((request, index) => (
                        <tr key={index}>
                            <td>{request.url}</td>
                            <td>{request.method}</td>
                            <td>{request.response_code}</td>
                            <td>{request.test_result ? request.test_result.name : 'N/A'}</td>
                            <td>{request.impact}</td>
                            <td>{request.severity}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;
