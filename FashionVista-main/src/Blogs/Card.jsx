import React from "react";
import { Link } from "react-router-dom";

const Card = (props) => {
  return (
    <div className="p-6 hover:scale-105 duration-200">
      <Link className="h-[300px] w-[300px] p-6 hover:scale-105 duration-200 mt-5">
        <img src={props.image} alt="" className="object-cover" />
      </Link>
      <p className="">{props.heading}</p>

    </div>
  );
};

export default Card;
