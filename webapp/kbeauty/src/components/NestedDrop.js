const NestedDrop = (props) => {
    return (
        props.cat.categories.map((item)=>(
            <li key={item._id} onClick={props.handleProducts(item.name_en)}>
              <div  className="flex justify-between" >
        <div className="flex">
            <img src={item.image} className="w-10 pr-2 justify-center" alt="" />
        <p className="font-medium text-zinc-600 mt-1 hover:text-black hover:font-semibold">{item.name_en}</p>
        </div>
        
    </div>      
            </li>
        ))
    );
}
 
export default NestedDrop;