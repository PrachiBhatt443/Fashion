import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AiOutlineMenu } from "react-icons/ai";
import { IoCloseSharp } from "react-icons/io5";
import axios from "axios";
import toast from "react-hot-toast";

function Navbar() {
  const [show, setShow] = useState(false);

  const navigateTo = useNavigate();

  // const handleLogout = async (e) => {
  //   e.preventDefault();
  //   try {
  //     const { data } = await axios.get(
  //       "http://localhost:4001/api/users/logout",
  //       { withCredentials: true }
  //     );
  //     console.log(data);
  //     localStorage.removeItem("jwt"); // deleting token in localStorage so that if user logged out it will goes to login page
  //     toast.success(data.message);
  //     setIsAuthenticated(false);
  //     navigateTo("/login");
  //   } catch (error) {
  //     console.log(error);
  //     toast.error("Failed to logout");
  //   }
  // };

  return (
    <>
      <nav className=" shadow-lg px-4 py-4 fixed top-0 left-0 right-0 z-50 mx-auto block bg-white">
        <div className="flex items-center justify-between w-full ">
          <div className="font-semibold text-2xl">
            FashionVista
          </div>
          {/* Desktop */}
          <div className=" mx-6">
            <ul className="hidden md:flex space-x-6">
              <Link to="/" className="hover:bg-[#C29B77] duration-200 px-3 py-2 hover:text-white">
                Home
              </Link>
              <Link to="/about" className="hover:bg-[#C29B77] duration-200 px-3 py-2 hover:text-white">
                About
              </Link>
              <Link to="/resources" className="hover:bg-[#C29B77] duration-200 px-3 py-2 hover:text-white">
                Resources
              </Link>
              <Link to="/blog" className="hover:bg-[#C29B77] duration-200 px-3 py-2 hover:text-white">
                Blog
              </Link>
            </ul>
            <div className="md:hidden" onClick={() => setShow(!show)}>
              {show ? <IoCloseSharp size={24} /> : <AiOutlineMenu size={24} />}
            </div>
          </div>
          <div className="hidden md:flex space-x-2">
              <Link
                to="/Login"
                className="px-4 py-2 border-[1px] border-black"
              >
                LOGIN
              </Link>
          </div>
        </div>
        {/* mobile navbar */}
        {show && (
          <div className="bg-white">
            <ul className="flex flex-col h-screen items-center justify-center space-y-3 md:hidden text-xl">
              <Link
                to="/"
                onClick={() => setShow(!show)}
                smooth="true"
                duration={500}
                offset={-70}
                activeClass="active"
                className="hover:text-blue-500"
              >
                HOME
              </Link>
              <Link
                to="/blogs"
                onClick={() => setShow(!show)}
                smooth="true"
                duration={500}
                offset={-70}
                activeClass="active"
                className="hover:text-blue-500"
              >
                BLOGS
              </Link>
              <Link
                to="/creators"
                onClick={() => setShow(!show)}
                smooth="true"
                duration={500}
                offset={-70}
                activeClass="active"
                className="hover:text-blue-500"
              >
                CREATORS
              </Link>
              <Link
                to="/about"
                onClick={() => setShow(!show)}
                smooth="true"
                duration={500}
                offset={-70}
                activeClass="active"
                className="hover:text-blue-500"
              >
                ABOUT
              </Link>
              <Link
                to="/contact"
                onClick={() => setShow(!show)}
                smooth="true"
                duration={500}
                offset={-70}
                activeClass="active"
                className="hover:text-blue-500"
              >
                CONTACT
              </Link>
            </ul>
          </div>
        )}
      </nav>
    </>
  );
}

export default Navbar;
