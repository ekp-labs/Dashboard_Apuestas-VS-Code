import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Inicio from './pages/Inicio';
import Apuestas from './pages/Apuestas';
import Competiciones from './pages/Competiciones';
import Equipos from './pages/Equipos';
import Partidos from './pages/Partidos';
import Jugadores from './pages/Jugadores';
import Inteligencia from './pages/Inteligencia';
import Estadisticas from './pages/Estadisticas';
import Placeholder from './pages/Placeholder';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Inicio />} />
          <Route path="/competiciones" element={<Competiciones />} />
          <Route path="/equipos" element={<Equipos />} />
          <Route path="/jugadores" element={<Jugadores />} />
          <Route path="/partidos" element={<Partidos />} />
          <Route path="/apuestas" element={<Apuestas />} />
          <Route path="/inteligencia" element={<Inteligencia />} />
          <Route path="/estadisticas" element={<Estadisticas />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}



