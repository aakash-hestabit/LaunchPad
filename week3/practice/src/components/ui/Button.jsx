import React from 'react'

const Button = ({title, handleClick,color="white", background = "gray", height="50px", width="200px", radius="rounded-lg"}) => {
  return (
    <button onClick={()=>handleClick()} style={{color,backgroundColor:background,height,width}} className={`${radius} flex gap-2 items-center justify-center font-semibold py-3 px-6 cursor-pointer border-zinc-500 border-1`}>
        {title}
    </button>
  )
}

export default Button