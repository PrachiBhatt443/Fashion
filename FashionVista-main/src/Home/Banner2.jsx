import React from "react";
import { GoArrowRight } from "react-icons/go";

const Banner2 = () => {
  return (
    <div className="container mx-auto mt-[100px] mb-[70px]">
      <h1 className="text-5xl">
        FASHION <span className="font-bold">TREND</span>{" "}
        <i className="italic text-[#C29B77]">forecasting</i>{" "}
      </h1>
      <p className="mt-[50px]">
        Welcome to the next wave of fashion intelligence, where AI-driven
        insights elegantly blend with your creative spirit. T-Fashion reshapes
        the traditional design cycle, turning data into your next stunning
        collection. Customized analytics and AI-generated recommendations await
        you. Are you ready to lead the fashion curve?
      </p>
      <button className="mt-5 px-2 py-3 border-[1px] border-black tracking-tighter">Book a meeting <GoArrowRight className="inline ml-2"/></button>
    </div>
  );
};

export default Banner2;
