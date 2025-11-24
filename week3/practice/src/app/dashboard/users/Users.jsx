'use client'
import React, { useState } from 'react';
import { RxCross2 } from 'react-icons/rx';
import Modal from '@/components/ui/Modal';

const data = [
  { id: 1, name: 'John Doe', email: 'john.doe@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 2, name: 'Jane Smith', email: 'jane.smith@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 3, name: 'Alice Johnson', email: 'alice.johnson@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 4, name: 'Bob Brown', email: 'bob.brown@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 5, name: 'Charlie Davis', email: 'charlie.davis@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 6, name: 'David Wilson', email: 'david.wilson@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 7, name: 'Emma White', email: 'emma.white@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 8, name: 'Frank Harris', email: 'frank.harris@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 9, name: 'Grace Clark', email: 'grace.clark@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' },
  { id: 10, name: 'Henry Lewis', email: 'henry.lewis@example.com', role: 'User', createdAt: '24/11/2025 00:00', updatedAt: '24/11/2025 00:00' }
];


const Users = () => {
  const [showModal, setShowModal] = useState(false);
  const [modalDetails, setModalDetails] = useState("");

  const handleModalClose = () => {
    setShowModal(false);
    setModalDetails("");
  };

  const handleModalOpen = (user) => {
    const details = `These are the details for the user ${user.name}: \n\nEmail: ${user.email}\nRole: ${user.role}\nCreated At: ${user.createdAt}\nUpdated At: ${user.updatedAt}`;
    setModalDetails(details);
    setShowModal(true);
  };

  return (
    <div className="p-4 overflow-x-auto">
      <h2 className="text-2xl font-bold mb-4">Users List</h2>
            <div className="overflow-x-auto max-w-full sm:rounded-lg">

        <table className="w-full text-sm text-left text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-200">
            <tr>
              <th scope="col" className="px-6 py-3 whitespace-nowrap">
                Name
              </th>
              <th scope="col" className="px-6 py-3 whitespace-nowrap">
                Email
              </th>
              <th scope="col" className="px-6 py-3 whitespace-nowrap">
                Role
              </th>
              <th scope="col" className="px-6 py-3 whitespace-nowrap">
                Created At
              </th>
              <th scope="col" className="px-6 py-3 whitespace-nowrap">
                Updated At
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((user) => (
              <tr
                key={user.id}
                className="bg-white border-b hover:bg-gray-100 cursor-pointer"
                onClick={() => handleModalOpen(user)}
              >
                <td className="px-6 py-4">{user.name}</td>
                <td className="px-6 py-4">{user.email}</td>
                <td className="px-6 py-4">{user.role}</td>
                <td className="px-6 py-4">{user.createdAt}</td>
                <td className="px-6 py-4">{user.updatedAt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && <Modal handleModalClose={handleModalClose} modalDetails={modalDetails} />}
    </div>
  );
};

export default Users;
