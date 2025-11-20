'use client'
import React, {useState} from 'react'
import { FaChevronRight } from 'react-icons/fa6'

const Card = ({height='120px',width='310px',label='Default Label',details='This is the default text for details',color ='red', handleModalOpen}) => {

  return (
    <article style={{height,backgroundColor:color}} className='flex-col box-border text-white rounded-md w-full overflow-hidden md:w-[48%] lg:w-[32%] xl:w-[24%]'>
        <p className=' border border-gray-500 px-5 py-3 h-[60%] flex items-center rounded-t-md font-bold tracking-wide'>{label}</p>
        
        <button className='flex items-center justify-between border border-gray-500 h-[40%] rounded-b-md w-full px-5 text-sm font-semibold cursor-pointer' 
            onClick={()=>{handleModalOpen(details)}}>
            <span>View Details</span> <FaChevronRight/> 
        </button>
    </article>
  )
}

export default Card 