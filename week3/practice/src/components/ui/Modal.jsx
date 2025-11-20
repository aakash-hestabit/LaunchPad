import React from 'react'
import { RxCross2 } from "react-icons/rx";

const Modal = ({handleModalClose,modalDetails}) => {
  return (
    <section className='fixed inset-0 w-full h-full bg-[#b6abab63] backdrop-blur-sm flex items-center justify-center'  onClick={(e)=>{
        if(e.target === e.currentTarget){
            handleModalClose();
        }
    }}>
        <article className='w-[90%] md:w-[60%] min-h-[40%] max-h-[70%] bg-gray-500 rounded-lg p-4 relative'>
            <p className='w-full text-xl p-7 pr-8 text-white overflow-y-auto scrollbar-hide max-h-[600px] font-mono'>
                {modalDetails}
            </p>
            <button className=' absolute p-4 right-1 top-1 bg-gray-700 font-bold rounded-full cursor-pointer' onClick={()=>handleModalClose()}><RxCross2/></button>
        </article>
    </section>
  )
}

export default Modal