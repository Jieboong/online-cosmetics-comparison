import React from "react";
import { Link } from "react-router-dom";

const Products = (props) => {
    const products  = props.products
    return (

        <div className="mt-8 grid grid-cols-1 gap-y-6 gap-x-6 sm:grid-cols-2 lg:grid-cols-5 xl:gap-x-4">
          {products && products.map((product) => (
            <div key={product._id} className="group relative bg-white shadow-sm rounded-md">
                <div className="w-full min-h-52 aspect-w-1 aspect-h-1 rounded-md overflow-hidden group-hover:opacity-60 lg:h-52 lg:aspect-none">
                    <img
                    src={product.image}
                    alt="product"
                    className="w-full h-32 object-center object-cover lg:w-full lg:h-full"
                    />


                </div>
                <div className="mt-2 flex px-2">
                    <p className="text-md   font-semibold text-gray-900">{product.discount_price}<span className="text-xs">₩</span>{product.sale !== 0 ? <span className=" text-xs   font-normal line-through text-gray-600 ml-1">{product.original_price}₩</span>: ""}</p> 
                </div>
                <div className="flex px-2 pb-2">
                    <div>
                        <Link to={`/product/${product.id}`}>
                    <h3 className="text-sm font-medium text-gray-800">
                        
                        <span aria-hidden="true" className="absolute inset-0" />
                        {product.product_name}
                        
                    </h3>
                    </Link>
                    </div>
                </div>
            </div>
          ))}
        </div>
    );
}
 
export default Products;