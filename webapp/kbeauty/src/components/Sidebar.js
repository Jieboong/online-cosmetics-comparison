import React, {useState} from "react";
import { Link } from "react-router-dom";




const Sidebar = (props) => {
    const category = props.category

    

    console.log(category)
    return (
        <aside className="md:w-80 md:fixed md:mt-[100px] md:overflow-scroll md:shadow-md" aria-label="Sidebar">
   <div className="w-full  px-3 h-screen overflow-y-auto bg-white">
      <ul className="space-y-2">
          {category && category.map((item,i)=>(
              
              <a href="#">
               <li key={item.name}>
                                    <Link to={`/category/${item.name}`}>
                                    <div  className="flex justify-between">
                                        <div className="flex">
                                        <p className="font-medium text-zinc-600 mt-1 hover:text-black hover:font-semibold">{item.name}</p>
                                        </div>
                                    </div>  
                                    </Link>
                                </li>
               </a>
          
          ))}
        <li>
            <div className="h-32"></div>
        </li>
      </ul>
   </div>
</aside> 

    );
}
 
export default Sidebar;