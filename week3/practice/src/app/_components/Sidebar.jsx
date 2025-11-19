'use client'
import React from 'react'
import { AiOutlineDashboard } from "react-icons/ai";
import { FiLayout } from "react-icons/fi";
import { TbBrandPagekit } from "react-icons/tb";
import { FaChartSimple,FaTable } from "react-icons/fa6";



const Sidebar = ({handleSidebarClick}) => {

  return (
    <aside className='flex flex-col py-6 px-4 bg-[#363636] gap-8 w-64 h-full'>
      <section className='flex flex-col text-neutral-400'>
        <p className='text-xs font-semibold mb-2 tracking-wider'>CORE</p>
        <p className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors' onClick={()=>handleSidebarClick("dashboard")}>
          <AiOutlineDashboard className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Dashboard</span>
        </p>
      </section>

      <section className='flex flex-col text-neutral-400'>
        <p className='text-xs font-semibold mb-2 tracking-wider'>INTERFACE</p>
        <p className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'  onClick={()=>handleSidebarClick("layouts")}>
          <FiLayout className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Layouts</span>
        </p>
        <p className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'  onClick={()=>handleSidebarClick("pages")}>
          <TbBrandPagekit className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Pages</span>
        </p>
      </section>
      <section className='flex flex-col text-neutral-400'>
        <p className='text-xs font-semibold mb-2 tracking-wider'>ADDONS</p>
        <p className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'  onClick={()=>handleSidebarClick("charts")}>
          <FaChartSimple className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Charts</span>
        </p>
        <p className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'  onClick={()=>handleSidebarClick("tables")}>
          <FaTable className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Tables</span>
        </p>
      </section>
    </aside>
  )
}

export default Sidebar
