
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './components/searchpage';
import Signin from './components/signin';
import Signup from './components/signup';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/Search" element={<SearchPage />} />
        <Route path="/" element={<SearchPage />} />
        <Route path='/signin' element={<Signin />} />
        <Route path='/signup' element={<Signup />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
