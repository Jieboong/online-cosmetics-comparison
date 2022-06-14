import {SearchIcon} from '@heroicons/react/outline'

const SearchProduct = (props) => {
    const getInputValue = (i)=>{
        props.handleSearch(i.target.value)
    };
    return (  
        <div className="2xl:hidden w-full items-center px-3 flex">
                <label className="relative text-gray-400 w-full focus-within:text-gray-600 block ">
                    <SearchIcon className="pointer-events-none w-6 h-6 absolute top-1/2 transform -translate-y-1/2 left-3"/>
                    <input className="appearance-none block w-full bg-grey-lighter text-grey-darker border-2 border-zinc-800 rounded-md py-4 px-4 pl-14 leading-tight focus:outline-none focus:bg-white focus:border-2 focus:border-purple-800" id="grid-password" type="search" placeholder="Sea view, infinity pool, spa bath" onChange={getInputValue}/>
                </label>
              </div>
    );
}
 
export default SearchProduct;