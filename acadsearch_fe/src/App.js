
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './components/searchpage';
import Signin from './components/signin';
import Signup from './components/signup';
import Profile from './components/profile';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/Search" element={<SearchPage />} />
        <Route path="/" element={<SearchPage />} />
        <Route path='/signin' element={<Signin />} />
        <Route path='/signup' element={<Signup />} />
        <Route path='/profile' element={<Profile />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
