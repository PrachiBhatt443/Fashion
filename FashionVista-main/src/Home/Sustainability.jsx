import React from "react";
import image from "../assets/intelligence-of-sustainability.png";
import { GoArrowRight } from "react-icons/go";

const Sustainability = () => {
  return (
    <div className="relative min-w-screen min-h-[500px]">
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center z-0"
        style={{ backgroundImage: `url(${image})` }}
      ></div>

      {/* Overlapping Text */}
      <div className="absolute top-[100px] left-[100px] text-xl z-10">
        <div className="text-4xl">
          <div className="text-5xl mb-2">T-Fashion</div> 
          <div className="text-[#3CA780] italic mb-9">intelligence of sustainability</div>
        </div>
        <p className="text-sm mb-6">
          At T-Fashion, we're not just forecasting trends; we're <br /> shaping the
          future of sustainable fashion. Our deep <br /> learning algorithms don't just
          forecast what's next—<br />they help you streamline your inventory to cut
          waste<br /> and reduce carbon emissions. Plus, we guide you<br /> toward
          eco-conscious materials and production <br /> methods, so you can be both
          stylish and sustainable.
        </p>
        <button >Read More <GoArrowRight className="inline"/></button>
      </div>
    </div>
  );
};

export default Sustainability;
