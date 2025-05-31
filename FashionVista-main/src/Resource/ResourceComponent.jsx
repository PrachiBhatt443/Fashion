import React from 'react'
import { GoArrowRight } from "react-icons/go";

const ResourceComponent = ({image, heading, paragraph}) => {
  return (
    <div className='p-5'>
        <div className='flex flex-col'>
            <img src={image} alt="" />
            <h1 className='text-4xl text-gray-700 font-bold mt-8'>{heading}</h1>
            <p className='mt-4'>{paragraph}</p>
            <button className='mt-4 text-xl'>Learn More <GoArrowRight className='inline'/></button>
        </div>
    </div>
  )
}

export default ResourceComponent