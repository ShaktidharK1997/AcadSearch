
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './components/searchpage';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/Search" element={<SearchPage />} />
        <Route path="/" element={<SearchPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
