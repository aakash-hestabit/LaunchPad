'use client'
import React, { useState } from 'react';
import { AiOutlineDashboard } from "react-icons/ai";
import { FiLayout } from "react-icons/fi";
import { TbBrandPagekit } from "react-icons/tb";
import { FaChartSimple, FaTable, FaChevronDown, FaChevronRight } from "react-icons/fa6";

const Sidebar = ({ handleSidebarClick, setPageNumber, handleLayoutClick}) => {
  const [showPages, setShowPages] = useState(false);
  const [showLayouts, setShowLayouts] = useState(false);

  return (
    <aside className='flex flex-col py-6 px-4 bg-[#363636] gap-8 w-64 h-full'>
     
      <section className='flex flex-col text-neutral-400'>
        <p className='text-xs font-semibold mb-2 tracking-wider'>CORE</p>
        <p
          className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
          onClick={() => handleSidebarClick("dashboard")}
        >
          <AiOutlineDashboard className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Dashboard</span>
        </p>
      </section>

   
      <section className='flex flex-col text-neutral-400'>
        <p className='text-xs font-semibold mb-2 tracking-wider'>INTERFACE</p>

        
        <p
          className='flex items-center justify-between gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
          onClick={() => setShowLayouts(!showLayouts)}
        >
          <span className='flex gap-2'>
            <FiLayout className="text-xl text-gray-300" />
            <span className='text-gray-200 font-medium'>Layouts</span>
          </span>
          {showLayouts ? <FaChevronDown /> : <FaChevronRight />}
        </p>

   
        {showLayouts && (
          <ul className='flex flex-col gap-1 pl-4 pt-2 '>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() => handleLayoutClick(1)}
              >
                <span className='text-gray-200 font-medium'>Layout 1</span>
              </button>
            </li>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() => handleLayoutClick(2)}
              >
                <span className='text-gray-200 font-medium'>Layout 2</span>
              </button>
            </li>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() =>handleLayoutClick(3)}
              >
                <span className='text-gray-200 font-medium'>Layout 3</span>
              </button>
            </li>
          </ul>
        )}

 
        <p
          className='flex items-center justify-between gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
          onClick={() => setShowPages(!showPages)}
        >
          <span className='flex gap-2'>
            <TbBrandPagekit className="text-xl text-gray-300" />
            <span className='text-gray-200 font-medium'>Pages</span>
          </span>
          {showPages ? <FaChevronDown /> : <FaChevronRight />}
        </p>

    
        {showPages && (
          <ul className='flex flex-col gap-1 pl-4 pt-2'>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() => setPageNumber(1)}
              >
                <span className='text-gray-200 font-medium'>Page 1</span>
              </button>
            </li>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() => setPageNumber(2)}
              >
                <span className='text-gray-200 font-medium'>Page 2</span>
              </button>
            </li>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() => setPageNumber(3)}
              >
                <span className='text-gray-200 font-medium'>Page 3</span>
              </button>
            </li>
            <li>
              <button
                className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                onClick={() => setPageNumber(4)}
              >
                <span className='text-gray-200 font-medium'>Page 4</span>
              </button>
            </li>
          </ul>
        )}
      </section>


      <section className='flex flex-col text-neutral-400'>
        <p className='text-xs font-semibold mb-2 tracking-wider'>ADDONS</p>
        <p
          className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
          onClick={() => handleSidebarClick("charts")}
        >
          <FaChartSimple className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Charts</span>
        </p>
        <p
          className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
          onClick={() => handleSidebarClick("tables")}
        >
          <FaTable className="text-xl text-gray-300" />
          <span className='text-gray-200 font-medium'>Tables</span>
        </p>
      </section>
    </aside>
  );
}

export default Sidebar;
