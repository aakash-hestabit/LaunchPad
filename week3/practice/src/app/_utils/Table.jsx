import React from 'react';

const Table = () => {
    const data = [
        { id: 1, name: 'John Doe', email: 'john.doe@example.com', age: 28, country: 'USA' },
        { id: 2, name: 'Jane Smith', email: 'jane.smith@example.com', age: 34, country: 'Canada' },
        { id: 3, name: 'Alice Johnson', email: 'alice.johnson@example.com', age: 25, country: 'UK' },
        { id: 4, name: 'Bob Brown', email: 'bob.brown@example.com', age: 40, country: 'Australia' },
        { id: 5, name: 'Charlie Davis', email: 'charlie.davis@example.com', age: 31, country: 'Germany' },
        { id: 6, name: 'David Wilson', email: 'david.wilson@example.com', age: 27, country: 'USA' },
        { id: 7, name: 'Emma White', email: 'emma.white@example.com', age: 22, country: 'France' },
        { id: 8, name: 'Frank Harris', email: 'frank.harris@example.com', age: 35, country: 'Italy' },
        { id: 9, name: 'Grace Clark', email: 'grace.clark@example.com', age: 29, country: 'Spain' },
        { id: 10, name: 'Henry Lewis', email: 'henry.lewis@example.com', age: 38, country: 'USA' }
    ];

    return (
        <div className="overflow-x-auto bg-white shadow-lg rounded-lg p-4">
            <table className="min-w-full table-auto">
                <thead>
                    <tr className="bg-gray-100 border-b">
                        <th className="py-2 px-4 text-left">ID</th>
                        <th className="py-2 px-4 text-left">Name</th>
                        <th className="py-2 px-4 text-left">Email</th>
                        <th className="py-2 px-4 text-left">Age</th>
                        <th className="py-2 px-4 text-left">Country</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row) => (
                        <tr key={row.id} className="border-b hover:bg-gray-50">
                            <td className="py-2 px-4">{row.id}</td>
                            <td className="py-2 px-4">{row.name}</td>
                            <td className="py-2 px-4">{row.email}</td>
                            <td className="py-2 px-4">{row.age}</td>
                            <td className="py-2 px-4">{row.country}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Table;
