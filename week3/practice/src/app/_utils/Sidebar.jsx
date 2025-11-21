'use client'
import React, { useState } from 'react';
import Link from 'next/link'
import { AiOutlineDashboard } from "react-icons/ai";
import { FiLayout } from "react-icons/fi";
import { TbBrandPagekit } from "react-icons/tb";
import { FaChartSimple, FaTable, FaChevronDown, FaChevronRight, FaMarsAndVenus } from "react-icons/fa6";
import { TiThMenu } from "react-icons/ti";
import { FaChevronLeft } from 'react-icons/fa';

const Sidebar = () => {
  const [showPages, setShowPages] = useState(false);
  const [showLayouts, setShowLayouts] = useState(false);

  return (
    <aside className={`flex flex-col py-6 px-4 bg-[#363636] gap-8 w-64 h-[100vh] `}>
      {
        <>
          <section className='flex flex-col text-neutral-400'>
            <p className='text-xs font-semibold mb-2 tracking-wider'>CORE</p>
            <Link href="/dashboard"><p
              className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
            >
              <AiOutlineDashboard className="text-xl text-gray-300" />
              <span className='text-gray-200 font-medium'>Dashboard</span>
            </p></Link>
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
              <ul className='flex flex-col gap-1 pl-4 pt-1 '>
                <Link href="/layout/1"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'

                  >
                    <span className='text-gray-200 font-medium'>Layout 1</span>
                  </button>
                </li></Link>
                <Link href="/layout/2"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'

                  >
                    <span className='text-gray-200 font-medium'>Layout 2</span>
                  </button>
                </li></Link>
                <Link href="/layout/3"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                  >
                    <span className='text-gray-200 font-medium'>Layout 3</span>
                  </button>
                </li></Link>
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
              <ul className='flex flex-col gap-1 pl-4 pt-1'>
                <Link href="/page/our"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                  >
                    <span className='text-gray-200 font-medium'>Our Page</span>
                  </button>
                </li></Link>
                <Link href="/page/their"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                  >
                    <span className='text-gray-200 font-medium'>Their Page</span>
                  </button>
                </li></Link>
                <Link href="/page/your"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                  >
                    <span className='text-gray-200 font-medium'>Your Page</span>
                  </button>
                </li></Link>
                <Link href="/page/mine"><li>
                  <button
                    className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors w-full'
                  >
                    <span className='text-gray-200 font-medium'>My Page</span>
                  </button>
                </li></Link>
              </ul>
            )}
          </section>


          <section className='flex flex-col text-neutral-400'>
            <p className='text-xs font-semibold mb-2 tracking-wider'>ADDONS</p>
            <p
              className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
            >
              <FaChartSimple className="text-xl text-gray-300" />
              <span className='text-gray-200 font-medium'>Charts</span>
            </p>
            <p
              className='flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors'
            >
              <FaTable className="text-xl text-gray-300" />
              <span className='text-gray-200 font-medium'>Tables</span>
            </p>
          </section>
        </>}
    </aside>
  );
}

export default Sidebar;
