import React, {useEffect, useState} from "react";
import Navbar from "../Navbar";
import Sidebar from "../Sidebar";
import Products from "../Products";
import Footer from "../Footer";
import { useParams } from "react-router-dom";


const Category = () => {
    const [category, setCategory] = useState(null)
    const [products, setProducts] = useState([])
    const { id } = useParams()


    useEffect(()=>{
        fetch(`http://172.30.1.51:3000/api/category/${id}`).then(response => {
            return response.json()}).then((data)=> {
                console.log(data)
                setProducts(data)}
            )
    },[id])

    useEffect(()=>{
        fetch("http://172.30.1.51:3000/api/category").then(response => {
            return response.json()}).then((data)=> {setCategory(data)})
    },[])

    return (
        <div>
            <Navbar searchItem={false} homepage={false}/>
            <Sidebar category={category}/>
            <div className="md:ml-80 md:pt-[110px] pt-8 px-8 h-full  bg-gray-50 ">
            {!products && <div className="w-full h-screen bg-zinc-100 text-center">Loading...</div> }
                {products && <Products products={products}/>}
                

                <div className="h-32"></div>
            </div>

            <Footer></Footer>
        </div>
    );
}
 
export default Category;