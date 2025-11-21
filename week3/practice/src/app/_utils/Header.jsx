'use client'
import { CgProfile } from "react-icons/cg";
import {  FaSearch } from "react-icons/fa";
import { GoTriangleDown } from "react-icons/go";
const Header = () => {
    

    return (
        <header className='flex py-3 px-6 items-center justify-between flex-wrap bg-[#4e4d4d] gap-y-2'>
            <span>
                <h1 className='font-bold text-2xl min-w-[177px] text-[#ddd8d8]'>Start Bootstrap</h1>
            </span>
            
            
            <nav className='flex gap-5'>
                <form className='flex border-2 rounded-2xl items-center content-center px-3 py-0.5 overflow-hidden gap-2 border-[gray] text-white'>
                    <label htmlFor="search" className="sr-only"></label>
                    <input type="text" id='search' placeholder='Search for...' className='decoration- outline-0 placeholder:text-[#d3cece] py-0.5'/>
                    <button className='cursor-pointer' onClick={(e)=>e.preventDefault()}><FaSearch /></button>
                </form>

                <button 
                    className="flex items-center gap-2 px-3 py-1 bg-gray-400 hover:bg-gray-200 rounded-full border border-gray-300">
                    <CgProfile className="text-xl text-gray-600" />
                    <GoTriangleDown className={`text-gray-500 text-sm`} />
                </button>
            </nav>
        </header>
    )
}

export default Header
