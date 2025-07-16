import React from 'react';
import Sidebar from './Sidebar';

function Layout({ children }) {
  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 p-6 lg:p-10 mt-16 lg:mt-0">
        {children}
      </main>
    </div>
  );
}

export default Layout;
