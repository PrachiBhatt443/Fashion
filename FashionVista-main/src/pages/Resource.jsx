import React from "react";
import image from "../assets/sample-reports-hero.png";
import image2 from "../assets/T-Fashion-x-Pantone.webp";
import image3 from "../assets/Slide-Cover-Final-High-Resoluation.webp";

import ResourceComponent from "../Resource/ResourceComponent";

const Resource = () => {
  return (
    <div className="mt-20 mb-10 overflow-x-hidden">
      <div
        className="relative flex w-screen flex-col items-center justify-end bg-cover bg-center transition min-h-screen"
        style={{ backgroundImage: `url(${image})` }}
      >
        <div className="mb-[4rem] flex w-full flex-col justify-start gap-y-[1.6875rem] text-white">
          <div className="container mx-auto">
            <h2 className=" text-[5rem] leading-[7rem] flex flex-col">
              <i className="font-semibold">sample</i>
              <span>Reports</span>
            </h2>
          </div>
        </div>
      </div>

      <div className="flex container mx-auto">
        <div className="w-1/2 px-3">
            <ResourceComponent
                image={image2}
                heading="Discover the Most Effective Spring 2024 Color Trends with FashionVista and Pantone"
                paragraph="Get your hands on the Spring 2021 Most Effective Color Trends report, jointly organized by T-Fashion and Pantone. Use the report to validate your collections and shape your communication sales campaigns for the spring season."
            />
        </div>
        <div className="w-1/2 px-3">
            <ResourceComponent
                image={image3}
                heading="Top Trends from Mercedes Benz Fashion Week India 2024"
                paragraph="Get ready for the latest fashion trends to hit the Russian market. T-Fashion, with its expert team and state-of-the-art AI technology, has analyzed the top styles and colors emerging from the Mercedes Benz Fashion Week Russia. From the analysis of over 2750 different looks and millions of Instagram images, T-Fashion presents a comprehensive report on the trends to watch out for this fall/winter season."
            />
        </div>
      </div>

    </div>
  );
};

export default Resource;
