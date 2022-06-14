import React, {useState} from "react";
import Hero from "./Hero";
import Products from "./Products";


const Home = (props) => {
    const [showItem, setShowItem] = useState(15);
    const products = props.products
    const handleShowMore = () => setShowItem(showItem+15)

    return (
        <div className="md:ml-80 md:pt-[150px] pt-10 px-8 h-full bg-zinc-100">
            <Hero handleSearch = {props.handleSearch}/>
            {!props.searchItem ? products && <Products products={products.slice(0,showItem)}/> : products && <Products products={props.searchproduct}/>}
            
            {!props.searchItem ? <div className="h-32 text-center items-center w-full">
                <button className="mt-12 rounded-md bg-zinc-400 px-8 py-3 text-white hover:bg-purple-800" onClick={handleShowMore}>Load More</button>
            </div>  : <div className="h-32"></div>}
            
        </div>
    );
}
 
export default Home;