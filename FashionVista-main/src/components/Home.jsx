import React from "react";
import Banner from "../Home/Banner";
import Banner2 from "../Home/Banner2";
import Banner3 from "../Home/Banner3";
import Sustainability from "../Home/Sustainability";
import AboutAI from "../Home/AboutAI";
// import Creator from "../Home/Creator";

function Home() {
  return (
    <div>
      <Banner/>
      <Banner2/>
      <Banner3/>
      <AboutAI/>
      <Sustainability/>
    </div>
  );
}

export default Home;
