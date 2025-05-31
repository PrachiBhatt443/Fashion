import React from "react";
import blog1 from "../assets/blog1.webp";
import blog2 from "../assets/blog2.webp";
import blog3 from "../assets/blog3.webp";
import blog4 from "../assets/blog4.webp";
import blog5 from "../assets/blog5.webp";
import blog6 from "../assets/blog6.webp";
import blog7 from "../assets/blog7.webp";
import image from "../assets/image.webp"
import Card from "../Blogs/Card";

const Blogs = () => {
  // style="background-image: url(&quot;/_next/image?url=/images/blog-hero-bg.png&amp;w=3840&amp;q=75&quot;); background-color: rgba(0, 0, 0, 0.7);"
  // style="background-color: rgba(0, 0, 0, 0.7);"
 
  return (
    <div className="mt-[70px] mb-8">

      <div class="relative flex w-screen flex-col items-center justify-center bg-cover bg-center" style={{backgroundImage: `url(${image})`}}>
        <div
          class="absolute inset-0 z-0 bg-black opacity-70"
        ></div>
        <div class="container z-20 pb-[4rem] mx-auto">
          <h1 class="mt-[0.625rem] py-[0.75rem] font-medium text-white text-[4rem] sm:text-[5rem] md:text-[6rem] max-w-full md:max-w-[85%] drop-shadow-md leading-[1.25]">
            Blog
          </h1>
          <p class="mt-[0.9375rem] w-[90%] text-[2rem] font-medium leading-[2.59rem] text-white sm:w-[60%] sm:text-[2.25rem]">
            Keep up with the latest news and trends <br />
            in the fashion industry
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3 container mx-auto">
        <Card image={blog1} heading="Beauty and Grooming"/>
        <Card image={blog2} heading="Color"/>
        <Card image={blog3} heading="Fashion"/>
        <Card image={blog4} heading="Fashion Weeks"/>
        <Card image={blog5} heading="Fashion AI"/>
        <Card image={blog6} heading="Fashion Tech And Innovation"/>
        <Card image={blog7} heading="Market Insights"/>
      </div>
    </div>
  );
};

export default Blogs;
