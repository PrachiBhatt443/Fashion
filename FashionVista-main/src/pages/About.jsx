import React from "react";
import AboutComponent from "../About/AboutComponent";
import image1 from "../assets/solution-and-technology-hero (1).webp";
import image2 from "../assets/solution-and-technology-three.webp";
import image3 from "../assets/analysis-of-data.webp";
import image4 from "../assets/ai-market-analysis-two.webp";
import image5 from "../assets/fashion-analytics-and-insights.webp";
import image6 from "../assets/fashion-analytics-and-insights-four.webp";
import image7 from "../assets/fashion-analytics-and-insights-five.webp";
import InverseAboutComponent from "../About/InverseAboutComponent";

const About = () => {
  return (
    <div className="mt-20">
      <AboutComponent
        heading={"Solution and Technology"}
        photo={image1}
        paragraph={
          "T-Fashion is an AI-powered trend forecasting and generative design platform that provides customized fashion analytics and AI-generated product recommendations to fashion companies."
        }
      />

      <div className="w-full bg-[#C29B77] mb-14 p-8">
        <div className="container mx-auto text-white">
          <h1 className="text-3xl mb-5">
            Innovative Technology, Backed by Expert Research
          </h1>
          <p>
            Our solutions are the product of over 8 years of dedicated AI
            research, conducted by a team of experts including PhDs in the
            field. The technologies powering T-Fashion have not only been honed
            over years of development but have also been recognized in
            high-level academic circles, including prestigious conferences like
            CVPR. This rigorous academic foundation ensures that our platform is
            at the forefront of AI innovation.
          </p>
        </div>
      </div>

      <InverseAboutComponent
        heading={
          "Audience Intelligence: Understanding Your Customer Base with Precision"
        }
        photo={image2}
        paragraph={
          "Defining and understanding your unique target audience is key. Our Audience Intelligence Tool collects millions of data points across various online channels, including social media platforms like Instagram, analytical tools like Google Trends, images from fashion weeks and lookbooks, and so on. This provides you with a comprehensive understanding of your customer base and trendsetters in your area. This extensive data collection allows us to forecast upcoming trends with unparalleled accuracy."
        }
      />

      <AboutComponent
        heading={"Data Analysis: Transforming Data into Insights"}
        photo={image3}
        paragraph={
          "We worked with fashion experts and AI experts to create innovative algorithms capable of pinpointing demographic and fashion information out of images. Our sophisticated deep learning algorithms delve into the collected data, extracting crucial information such as age, gender, location, clothing types, style preferences, and Pantone colors. This detailed analysis forms the backbone of our trend predictions and product recommendations."
        }
      />

      <InverseAboutComponent
        heading={"Trend Forecasts and Analytics: Anticipating the Future"}
        photo={image4}
        paragraph={
          "Equipped with hundreds of millions of data points, our system not only understands current market trends but also predicts how these trends will evolve. We provide you with forward-looking fashion trend forecasts, giving you a competitive edge in product development and market timing. We transform complex data into visually accessible and actionable insights. You will gain a comprehensive understanding of emerging product trends and their potential market impact, enabling informed decision-making that can significantly boost your sales and uncover new market opportunities"
        }
      />

      <AboutComponent
        heading={"Fashion Analytics & Insights"}
        photo={image5}
        paragraph={
          "We visualize the resulting trend data to help you grasp trend dynamics and find the winning products. In the end, you will have an in-depth understanding of what product trends are on the way to the market and how they will behave for next seasons. This will help you make better decisions, boost your sales and find new market opportunities."
        }
      />

      <InverseAboutComponent
        heading={"Collections: Collaborate and Innovate"}
        photo={image6}
        paragraph={
          "More than a moodboard, Collections is your collaborative workspace. Gather and share insights, designs, and data within your team, fostering a creative and cohesive environment. It's where research meets innovation, helping you and your team stay inspired and aligned."
        }
      />

      <AboutComponent
        heading={"Join the Fashion Revolution with T-Fashion"}
        photo={image7}
        paragraph={
          "Step into the future of fashion with T-Fashion. Our AI-powered platform is your guide to navigating the complexities of the fashion industry, from trend forecasting to product design. Discover how we can transform your approach to fashion, making your brand not just a participant but a trendsetter in the industry."
        }
      />

    </div>
  );
};

export default About;
