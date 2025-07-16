import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import PacienteList from './components/PacienteList';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<h1 className="text-3xl font-bold text-gray-800">Bem-vindo ao Dashboard!</h1>} />
          <Route path="/pacientes" element={<PacienteList />} />
          {/* Adicione mais rotas aqui para outros módulos */}
          <Route path="*" element={<h1 className="text-3xl font-bold text-gray-800">Página Não Encontrada</h1>} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;