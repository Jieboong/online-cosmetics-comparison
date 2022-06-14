import React, {useState, useEffect} from "react";
import { MenuAlt1Icon, ShoppingBagIcon} from '@heroicons/react/outline'
import { Link } from "react-router-dom";

import SearchProduct from "./Search";


const Navbar = (props) => {
  const [nav, setNav] = useState(false)
  const handleClick = ()=> setNav(!nav)
  const [scrollY, setScrollY] = useState(0);

  function logit() {
    setScrollY(window.pageYOffset);
  }

  useEffect(() => {
    function watchScroll() {
      window.addEventListener("scroll", logit);
    }
    watchScroll();
    // Remove listener (like componentWillUnmount)
    return () => {
      window.removeEventListener("scroll", logit);
    };
  }, []);

    return (
    <div className="w-screen h-[100px] z-10 bg-white fixed drop-shadow-lg">
        <div className="px-2 flex justify-between items-center w-full h-full">
            <div className="flex items-center">
                <button className="md:px-8 px-4" onClick={handleClick}><MenuAlt1Icon className="w-8"></MenuAlt1Icon></button>
                <Link to="/"><h1 className="text-2xl font-bold mr-4 sm:text-4xl">K-Beauty</h1></Link>
            </div>
            {(scrollY > 330 && props.homepage) || props.searchItem ?
            <div className="hidden md:block w-[700px]">
              <SearchProduct handleSearch = {props.handleSearch}/>
            </div>

             : ""}            
            <div className="flex px-4">
                <button><h6 className="font-medium mt-1 px-4 text-black hover:text-gray-700">My Account</h6></button>
                
            </div>
        </div>
        
    </div>);
}
 
export default Navbar;