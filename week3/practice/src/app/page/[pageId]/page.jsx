import React from 'react'
import { notFound } from 'next/navigation';
const page = async({params}) => {
    const params1 = await params;
    const pageId = params1.pageId;
    console.log(pageId);
    
    const validPageIds = ['your','mine','their','our'];
    if(!validPageIds.includes(pageId)){
        return notFound();
    }
  return (
    <div>this is {pageId} page</div>
  )
}

export default page