import React from "react";
import fashionOne from "../assets/fashion-trend-one.webp";
import fashiontwo from "../assets/fashion-trend-two.webp";

import { GoArrowRight } from "react-icons/go";

const Banner3 = () => {
  return (
    <div className="container mx-auto">
      <div className="flex w-full">
        <div className="w-1/2">
          <img src={fashionOne} alt="model photo" />
        </div>
        <div className="w-1/2 bg-[#F7F3EA]">
          <div className="p-8">
            <h1 className="text-5xl ">
              UPCOMING <br /> <span>PRODUCT</span> <br />{" "}
              <i className="">trends</i>
            </h1>
            <div>
              <p className="mt-4">
                Bridging the gap between <br /> catwalk inspiration and <br />{" "}
                algorithmic precision, T-Fashion <br /> offers a vanguard
                platform that <br /> foresees fashion cycles, enriching <br />{" "}
                your designs with data-driven <br /> foresight. We interpret the{" "}
                <br /> language of the market, <br /> converting it into your
                next <br /> phenomenal design.
              </p>
            </div>
            <button className="mt-4 text-xl">
              {" "}
              Read More <GoArrowRight className="inline" />
            </button>
          </div>
        </div>
      </div>

      <div className="flex w-full">
        <div className="w-1/2 bg-[#FAF7F2]">
          <div className="p-8">
            <h1 className="text-5xl ">
              INSPIRING & <br /> ACCURATE DESIGN <br /> DIRECTION <br />{" "}
              <i className="">for creatives</i>
            </h1>
            <div>
              <p className="mt-4">
                With T-Fashion, knowing what's going to be popular is more
                science than guesswork. We analyze upcoming product trends and
                how they're likely to perform in the market. This helps you make
                smarter choices, so you don't end up with unnecessary stocks.
                T-Fashion will guide you to your winning products.
              </p>
            </div>
            <button className="mt-4 text-xl">
              {" "}
              Read More <GoArrowRight className="inline" />
            </button>
          </div>
        </div>
        <div className="w-1/2">
          <img src={fashiontwo} alt="model photo" />
        </div>
      </div>
    </div>
  );
};

export default Banner3;
