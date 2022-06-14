import React, {useState, useEffect} from "react";
import Navbar from "./Navbar";
import { useParams } from "react-router-dom";

const DetailPage = () => {
    const [products, setProducts] = useState(null)
    const [price, setPrice] = useState([])
    const { name } = useParams()


    useEffect(()=>{
        fetch(`http://172.30.1.51:3000/api/detail/${name}`).then(response => {
            return response.json()}).then((data)=> {
                
                setProducts(data)}
            )
    },[name])

    useEffect(()=>{
        fetch(`http://172.30.1.51:3000/api/price/${name}`).then(response => {
            return response.json()}).then((data)=> {
                
                setPrice(data)}
            )
    },[name])
    
    return (
    <div>
        <Navbar searchItem={false} homepage={false}/>
        {products &&  <div className="w-full p-20  bg-zinc-100">
            <div className="w-full flex mt-10 pl-20 pr-20 rounded-md bg-white h-[600px] shadow-lg">
            <div className="w-[200px] min-h-52 aspect-w-1 aspect-h-1 rounded-md overflow-hidden group-hover:opacity-60 lg:h-52 lg:aspect-none">
                    <img
                    src={products.image}
                    alt="product"
                    className="w-full h-32 object-center object-cover lg:w-full lg:h-full"
                    />
                </div>
                <div className="w-full pl-10 pt-10 mr-10">
                    <h1>product name</h1>
                    <h1>product price</h1>
                    <h1>product saleprice</h1>
                    <h1>product brand</h1>
                    <h1>store</h1>
                    <h1>product link</h1>
                </div>
            </div>

        </div>}
        
    </div>);
}
 
export default DetailPage;