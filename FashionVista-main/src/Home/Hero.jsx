import React from "react";
// import { useAuth } from "../context/AuthProvider";
import { Link } from "react-router-dom";

function Hero() {
  // const { blogs } = useAuth();
  // console.log(blogs);
  return (
    <div>
      <h1 className="container mx-auto text-4xl mt-3 font-semibold p-6">Latest Fashion</h1>
      <div className=" container mx-auto my-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 px-6">
        <div
          to=""
          key=""
          className="bg-white rounded-lg hover:shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300"
        >
          <div className="group relative">
            <img src="" alt="fashion image" className="w-full h-56 object-cover" />
            <div className=" absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-75 group-hover:opacity-100 transition-transform duration-300"></div>
            <h1 className=" absolute bottom-4 left-4 text-white text-xl font-bold group-hover:text-yellow-500 transition-colors duration-300">
              
            </h1>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Hero;
