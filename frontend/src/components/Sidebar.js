import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 text-white p-4 fixed inset-y-0 left-0 overflow-y-auto lg:static lg:translate-x-0 transform -translate-x-full transition-transform duration-200 ease-in-out">
      <div className="text-2xl font-bold mb-6">Sistema Clínicas</div>
      <nav>
        <ul>
          <li className="mb-2">
            <Link to="/" className="block py-2 px-4 rounded hover:bg-gray-700">Dashboard</Link>
          </li>
          <li className="mb-2">
            <Link to="/pacientes" className="block py-2 px-4 rounded hover:bg-gray-700">Pacientes</Link>
          </li>
          <li className="mb-2">
            <Link to="/clinicas" className="block py-2 px-4 rounded hover:bg-gray-700">Clínicas</Link>
          </li>
          <li className="mb-2">
            <Link to="/agendamentos" className="block py-2 px-4 rounded hover:bg-gray-700">Agendamentos</Link>
          </li>
          <li className="mb-2">
            <Link to="/prontuarios" className="block py-2 px-4 rounded hover:bg-gray-700">Prontuários</Link>
          </li>
          <li className="mb-2">
            <Link to="/estoque" className="block py-2 px-4 rounded hover:bg-gray-700">Estoque</Link>
          </li>
          <li className="mb-2">
            <Link to="/usuarios" className="block py-2 px-4 rounded hover:bg-gray-700">Usuários</Link>
          </li>
          <li className="mb-2">
            <Link to="/fila" className="block py-2 px-4 rounded hover:bg-gray-700">Fila de Espera</Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
