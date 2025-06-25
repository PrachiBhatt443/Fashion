import React from "react";
import Navbar from "../src/components/Navbar";
import Home from "../src/components/Home";
import Footer from "../src/components/Footer";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import Login from "../src/pages/Login";
import Register from "../src/pages/Register";
import { Toaster } from "react-hot-toast";
import Blogs from "./pages/Blogs";
import About from "./pages/About";
import Resource from "./pages/Resource";
import Contact from "./pages/Contact";
import Trend from "../src/components/Trend";
import FashionAnalyzer from "./components/FashionAnalyzer";
function App() {
  const location = useLocation();
  const hideNavbarFooter = ["/login", "/register"].includes(location.pathname);

  return (
    <div className="p-16">
      {!hideNavbarFooter && <Navbar />}
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/login" element={<Login />} />
        <Route exact path="/register" element={<Register />} />
        <Route exact path="/blog" element={<Blogs />} />
        <Route exact path="/about" element={<About />} />
        <Route exact path="/resources" element={<Resource />} />
        <Route exact path="/contact" element={<Contact />} />
        <Route exact path="/trend" element={<Trend />} />
        <Route exact path="/prediction" element={<FashionAnalyzer />} />
      </Routes>
      <Toaster />
      {!hideNavbarFooter && <Footer />}
    </div>
  );
}

export default App;
