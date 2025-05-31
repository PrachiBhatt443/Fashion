import React from 'react';

const PopularColors = () => {
  // Static Data (You can replace this with API data later)
  const popularColors = {
    week: [
      { color: 'rgb(5, 9, 7)', name: 'Dark Green'  },
      { color: 'rgb(212, 212, 215)', name: 'Light Gray' },
      { color: 'rgb(6, 159, 212)', name: 'Bright Cyan' },
    ],
    month: [
      { color: 'rgb(139, 184, 147)', name: 'Soft Sage Green' },
      { color: 'rgb(192, 167, 168)', name: 'Soft Dusty Pink' },
      { color: 'rgb(227, 220, 207)', name: 'Pale Beige' },
    ],
    day: [
      { color: 'rgb(207, 199, 198)', name: 'Light Grayish Beige'},
      { color: 'rgb(188, 143, 143)', name: 'Rosy Brown'},
      { color: 'rgb(101, 103, 144)', name: 'dimgrey' },
    ],
  };

  return (
    <div className="bg-cream min-h-screen py-16 px-6 sm:px-8 lg:px-12 mt-6">
      <h1 className="text-5xl font-extrabold text-center text-gray-900 mb-10 text-shadow-lg">
        Popular Colors <span className="text-[#C29B77]">Trending Now</span>
      </h1>

      <div className="space-y-24">
        {['month', 'week', 'day'].map((timePeriod, index) => (
          <div key={index} className="space-y-8">
            <h2
              className="text-4xl font-semibold text-center p-4 rounded-full shadow-lg"
              style={{
                background: 'linear-gradient(135deg, #C29B77, #E4D2A3)', // Gradient using your palette
                WebkitBackgroundClip: 'text',
                color: 'transparent',
                backgroundColor: '#F3E9D2', // Light cream background for headings
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              }}
            >
              This {timePeriod.charAt(0).toUpperCase() + timePeriod.slice(1)}'s Popular Colors
            </h2>

            <div className="flex justify-center space-x-8 flex-wrap animate__animated animate__fadeIn">
              {popularColors[timePeriod].map((colorItem, i) => (
                <div
                  key={i}
                  className="relative w-60 h-60 rounded-xl shadow-xl transform transition-all duration-300 hover:scale-105 hover:shadow-2xl"
                  style={{ backgroundColor: colorItem.color }}
                >
                  <div className="absolute inset-0 flex items-center justify-center">
                    <p className="text-white font-bold text-center text-lg text-shadow-md">{colorItem.name}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PopularColors;
