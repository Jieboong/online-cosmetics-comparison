import React from "react";
import SearchProduct from "./Search";



const Hero = (props) => {
    return (
        <div className="w-full h-[450px] rounded-md justify-center">
            <div className="flex items-center bg-cover bg-bottom p-10 h-full rounded-xl bg-[url('https://cached-api.voxmarkets.co.uk/img/resize?nocrop=true&type=webp&width=1024&url=https://s3-eu-west-1.amazonaws.com/vox.store.images/cms/b4e0abfb-db2f-4ed8-8a57-f1e8fcdde2a6.jpeg')]">

<form className="w-full">
  
  

  
    <div className="w-full  px-3   flex">
    <SearchProduct handleSearch = {props.handleSearch}/>
    </div>
  

</form>

</div>
        </div>
    );
}
 
export default Hero;