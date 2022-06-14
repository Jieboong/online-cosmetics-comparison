import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import Home from "./Home";
import React, {useEffect, useState} from "react";
import Footer from "./Footer";





function MainPage() {
  const [category, setCategory] = useState(null)
  const [products, setProducts] = useState([])
  const [searchproduct, setSearchProduct] = useState([])
  const [searchItem, setSearchItem] = useState(false)

  
  const handleSearch = (item) => {
    console.log(item)
    if(item !== ""){
      const newprods = products.filter(prod => prod.product_name.toLowerCase().includes(item.toLowerCase()))
      setSearchProduct(newprods)
      setSearchItem(true)
    }
    else{
      setSearchItem(false)
    }
    
  }
    
    useEffect(()=>{
        fetch("http://172.30.1.51:3000/api/category").then(response => {
            return response.json()}).then((data)=> {setCategory(data)})
    },[])

    useEffect(()=>{
      fetch("http://172.30.1.51:3000/api/products").then(response => {
          return response.json()}).then((data)=> {setProducts(data)})
  },[])

  return (
    <>
    <Navbar handleSearch = {handleSearch} searchItem={searchItem} homepage={true}/>
    <Sidebar category={category}/>
    <Home products={products} searchproduct = {searchproduct} searchItem={searchItem} handleSearch = {handleSearch}/>
    <Footer></Footer>
    </>

  );
}

export default MainPage;