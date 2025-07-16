import React, { useEffect, useState } from 'react';

function PacienteList() {
  const [pacientes, setPacientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/pacientes/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setPacientes(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="text-center text-gray-600">Carregando pacientes...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">Erro: {error.message}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Lista de Pacientes (React)</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {pacientes.map(paciente => (
          <div key={paciente.paciente_id} className="bg-white shadow-md rounded-lg p-4">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">{paciente.nome} {paciente.sobrenome}</h2>
            <p className="text-gray-600 text-sm mb-2">CPF: {paciente.cpf || 'N/A'}</p>
            <p className="text-gray-600 text-sm mb-4">Email: {paciente.email || 'N/A'}</p>
            {/* Adicione mais detalhes ou links aqui */}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PacienteList;
