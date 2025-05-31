import React from "react";
import { FaGithub } from "react-icons/fa";
import { BsYoutube } from "react-icons/bs";
import { FaLinkedin } from "react-icons/fa";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <div className=" text-white ">
      <footer className="border bg-gradient-to-t from-black to-gray-800 py-10  text-white p-4">
        <div className="container mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className=" text-center md:text-start">
            <h2 className="text-lg font-semibold mb-4">FashionVista</h2>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                With FashionVista’s AI-powered trend forecasting platform, grasp trend dynamics through billions of interactions taking place online.
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                  Solution & Tech
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                  Events
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                  Sample Reports
                </a>
              </li>
            </ul>
          </div>
          <div className=" text-center md:text-start">
            <h2 className="text-lg font-semibold mb-4">Location</h2>
            <ul className="space-y-2">
              <li>
                <p className="text-gray-400 hover:text-white">
                  GBPIET
                </p>
              </li>
              <li>
                <p className="text-gray-400 hover:text-white">
                  Pauri Garhwal
                </p>
              </li>
              <li>
                <p className="text-gray-400 hover:text-white">
                  Uttarakhand
                </p>
              </li>
              <li>
                <p className="text-gray-400 hover:text-white">
                  India
                </p>
              </li>
            </ul>
          </div>

          <div className=" text-center md:text-start">
            <h2 className="text-lg font-semibold mb-4">Company</h2>
            <ul className="space-y-2">
              <li>
                <Link to="/about" className="text-gray-400 hover:text-white">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-400 hover:text-white">
                  Contact Us
                </Link>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                  Career
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>
        </div>
      </footer>
      <div className=" container mx-auto  flex flex-col md:flex-row justify-between items-center py-7">
        <div className="text-xl font-semibold hidden md:flex">
            FashionVista
        </div>
        <div className="text-gray-400 text-sm hidden md:flex">
          <p>&copy; 2024 All rights reserved</p>
        </div>
        <div className="mt-4 md:mt-0 flex space-x-4">
          <a href="#">
            <FaGithub className="h-6" />
          </a>
          <a href="#">
            <BsYoutube className="h-6" />
          </a>

          <a href="#">
            <FaLinkedin className="h-6" />
          </a>
        </div>
      </div>
    </div>
  );
};

export default Footer;
