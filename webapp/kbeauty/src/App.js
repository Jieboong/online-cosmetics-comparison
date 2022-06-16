
import Footer from "./components/Footer";
import MainPage from "./components/Main";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Category from "./components/category/Category";
import DetailPage from "./components/DetailPage";


function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
       <Route exact path="/" element={<MainPage/>}></Route> 
       <Route path="/product/:name" element={<DetailPage/>}></Route> 
       <Route path="/category/:id" element={<Category/>}></Route> 
      </Routes>
      </BrowserRouter>
    </div>

  );
}

export default App;
