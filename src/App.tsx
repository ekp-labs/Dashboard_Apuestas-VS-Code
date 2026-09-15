import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Inicio from './pages/Inicio';
import Apuestas from './pages/Apuestas';
import Placeholder from './pages/Placeholder';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Inicio />} />
          <Route path="/competiciones" element={<Placeholder title="Competiciones" />} />
          <Route path="/equipos" element={<Placeholder title="Equipos" />} />
          <Route path="/jugadores" element={<Placeholder title="Jugadores" />} />
          <Route path="/partidos" element={<Placeholder title="Partidos" />} />
          <Route path="/apuestas" element={<Apuestas />} />
          <Route path="/inteligencia" element={<Placeholder title="Inteligencia" />} />
          <Route path="/estadisticas" element={<Placeholder title="Estadísticas" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}



