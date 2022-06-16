import React, {useState, useEffect} from "react";
import Navbar from "./Navbar";
import { useParams } from "react-router-dom";
import { Bar } from "react-chartjs-2";
import {Chart as ChartJS} from 'chart.js/auto'


const DetailPage = () => {
    const [products, setProducts] = useState(null)
    const [prod, setProd] = useState(null)
    const [price, setPrice] = useState([])
    const { name } = useParams()
    const [tags, setTags] = useState(null)
    const [isLoading, setLoading] = useState(false)
    

    useEffect(()=>{
        fetch(`http://3.34.179.67:3000/api/detail/${name}`).then(response => {
            return response.json()}).then((data)=> {
                setProducts(data)
                setLoading(true)
            })
    },[name])


    useEffect(()=>{
        fetch(`http://3.34.179.67:3000/api/price/${name}`).then(response => {
            return response.json()}).then((data)=> {
                setPrice(data)
            })
    },[name])

    useEffect(()=>{
        fetch(`http://3.34.179.67:3000/api/comments/${name}`).then(response => {
            return response.json()}).then((data)=> {
                setTags(data)
            })
    },[name])

    

    
    return (
    <div>
        <Navbar searchItem={false} homepage={false}/>
        {products === null && 
        <div className="w-full  pt-48 h-screen items-center text-center">
            <div class="flex items-center justify-center">
  <div class="spinner-border animate-spin inline-block w-10 h-10 border-4 rounded-full" role="status">
    <span class="v visually-hidden">...</span>
  </div>
</div>
        </div> }
        {products  &&  <div className="w-full p-20  bg-white">
            <div className={`relative  w-full p-10 items-center flex mt-20 overflow-x-auto shadow-md sm:rounded-lg`}>
                <div className="col">
                    <div className=" w-52 h-52">
                        <img src={products[0].image} alt="" />
                    </div>
                    {tags && <div className="grid grid-rows-5    grid-flow-col ">
                            {tags.token.map((t)=> <div className="w-[100px]  bg-pink-400 text-white m-2 rounded-md shadow-sm text-center">#{t}</div>)}            

                        </div>}
                    
                </div>
                
                <div className="mt-4 ml-6 col">
                    <div className=" font-bold">
                    {products[0].product_name}
                    </div>
                    <div className="text-md">
                    {products[0].big_category}
                    </div>                    
                    <div className="text-md">
                    {products[0].brand}
                    </div>             
                    <div className="text-md">
                    {products[0].store}
                    </div>             
                    <div className="text-md font-bold">
                    {products[0].discount_price} ₩
                    </div>
                    <div className="text-md mt-2 font-bold">
                     <a href={products[0].link} className='bg-pink-600 p-2 text-sm rounded-md text-white mt-6'>See product</a> 
                    </div> 
                </div>
                <div className="ml-10 w-full" >
        <Bar
          data={{
            labels: price.map((x)=> x.date),
            datasets: [
              {
                // Label for bars
                label: "date/price",
                // Data or value of your each variable
                data: price.map((x)=> x.discount_price),
                // Color of each bar
                backgroundColor: ["rgba(255, 8, 142, 0.2)",],
                // Border color of each bar
                borderColor: ["purple"],
                borderWidth: 0.5,
              },
            ],
          }}
          // Height of graph
          height={400}
          options={{
            maintainAspectRatio: false,
            scales: {
              yAxes: [
                {
                  ticks: {
                    // The y-axis value will start from zero
                    beginAtZero: true,
                  },
                },
              ],
            },
            legend: {
              labels: {
                fontSize: 15,
              },
            },
          }}
        />
      </div>
            </div>
        <div className="relative mt-20 overflow-x-auto shadow-md sm:rounded-lg">
            <h5 className="font-bold text-xl m-2">Related Products</h5>
    <table className="w-full text-sm text-left text-white dark:text-white">
        <thead className="text-xs text-white uppercase bg-pink-400 dark:bg-pink-400 dark:text-white">
            <tr>
            <th scope="col" className="px-6 py-3">
                    Image
                </th>
                <th scope="col" className="px-6 py-3">
                    Product name
                </th>
                {products.big_category !== "" ? <th scope="col" className="px-6 py-3">
                    Category
                </th>: ""}
                <th scope="col" className="px-6 py-3">
                    Brand
                </th> 
                <th scope="col" className="px-6 py-3">
                    Price
                </th>
                <th scope="col" className="px-6 py-3">
                    Store
                </th>
                <th scope="col" className="px-6 py-3">
                    Link
                </th>
            </tr>
        </thead>
        <tbody>
        {products && products.map((product) => (
            <tr className="bg-white border-b dark:bg-white dark:border-bg-white">
            <th scope="row" className="px-6 py-4 font-medium text-black dark:text-black whitespace-nowrap">
                <img src={product.image} className=" w-40 h-40" alt="" />
            </th>
            <th scope="row" className="px-6 py-4 font-medium text-black dark:text-black whitespace-nowrap">
                
                {product.product_name}   
            </th>
            {product.big_category !== "" ? <td className="px-6 py-4 text-black">
                {product.big_category}   
            </td>: ""}
            
            <td className="px-6 py-4 text-black">
                {product.brand}
            </td>
            
            <td className="px-6 py-4 text-black">
                {product.discount_price} ₩    
            </td>
            <td className="px-6 py-4 text-black">
                {product.store}     
            </td>
            <td className="px-6 py-4 text-left">
                <a href={product.link} target="_blank" className="font-medium text-left  text-pink-600 dark:text-pink-600 hover:underline">Open</a>
            </td>
        </tr>
        ))}
            
        </tbody>
    </table>
    
</div></div>}
        
    </div>);
}
 
export default DetailPage;