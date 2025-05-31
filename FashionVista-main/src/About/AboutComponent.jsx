import React from 'react'

const AboutComponent = ({heading, photo, paragraph}) => {
  return (
    <div className='w-full bg-[#FAF7F2] p-8 mb-14 pt-14'>
        <div className='container mx-auto flex'>
            <div className='w-1/2'>
                <h1 className='text-5xl mb-5'>{heading}</h1>
                <p>
                    {paragraph}
                </p>
            </div>
            <div className='w-1/2 ml-6'>
                <img src={photo} alt="trend photo" />
            </div>
        </div>
    </div>
  )
}

export default AboutComponent