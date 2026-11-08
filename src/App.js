import './App.css';
import PlantTable from './plant-frontend/plantTable';
import PlantDetail from './plant-frontend/plantDetail';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<PlantTable/>}/>
            <Route path="/plants/:id" element={<PlantDetail />}/>
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
