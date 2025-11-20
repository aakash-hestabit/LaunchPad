import React from 'react'

const Page =  async({params}) => {
  const params1 = await params;
  const layout_no = params1.slug;
  
  return (
    <div>this is layout number  no {layout_no}</div>

  )
}


export default Page