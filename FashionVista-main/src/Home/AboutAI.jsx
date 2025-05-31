import React from "react";
import { GoArrowRight } from "react-icons/go";
import {Link} from 'react-router-dom'


const AboutAI = () => {
  return (
    <div className="min-w-full my-[70px] bg-[#F7F3EA] p-10">
      <div className="container mx-auto text-center">
        <h1 className="text-4xl mb-6">
          UNLOCK <span className="">the power of AI</span>
        </h1>
        <p className="mb-6">
          At the core of T-Fashion is a robust AI engine that examines a
          wide-ranging digital landscape to forecast fashion trends with
          unparalleled accuracy. Leveraging a myriad of data points—from
          influencer posts on Instagram to search patterns on Google Trends—our
          algorithms decode the complexity of evolving fashion preferences and
          upcoming product trends. This allows us to offer data-backed insights
          through our platform, empowering you to make informed, proactive
          decisions for the seasons ahead.
        </p>
        <Link to="/about" className="pb-[70px] text-2xl">
            Read More <GoArrowRight className="inline"/>
        </Link>
      </div>
    </div>
  );
};

export default AboutAI;
