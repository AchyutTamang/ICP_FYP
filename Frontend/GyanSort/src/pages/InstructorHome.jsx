import React from "react";
import Navbar from "../components/stick/Navbar";
import instructorImg from "../assets/Teacher.png";
import { useNavigate } from "react-router-dom";

function InstructorHome() {
  const navigate = useNavigate();

  // Function to handle creating a new course
  const handleCreateCourse = () => {
    // You can add navigation to a course creation page here
    // navigate('/instructor/create-course');
    console.log("Create course clicked");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 text-white relative overflow-hidden">
      {/* Background pattern */}
      <div
        className="absolute inset-0 opacity-10 bg-repeat z-0"
        style={{
          backgroundImage: "url('/pattern-education.png')",
          backgroundSize: "300px",
        }}
      ></div>

      <Navbar />

      {/* Hero Section */}
      <div className="container mx-auto px-4 pt-24 pb-16 relative z-10">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <h1 className="text-4xl font-bold mb-4">
              <span className="text-[#00FF40]">START</span>
              <br />
              Uploading Content
            </h1>
            <p className="text-gray-300 mb-8 max-w-lg">
              Create and manage your courses, upload content, and engage with
              your students.
            </p>
            <button
              onClick={handleCreateCourse}
              className="bg-[#00FF40] hover:bg-[#00DD30] text-black font-bold py-3 px-8 rounded-full transition duration-300 transform hover:-translate-y-1"
            >
              Right Now
            </button>
          </div>
          <div className="md:w-1/2 flex justify-center">
            <img
              src={instructorImg}
              alt="Instructor dashboard"
              className="max-w-full md:max-w-md h-auto"
            />
          </div>
        </div>
      </div>

      <button
        onClick={() => navigate("/instructor/courses")}
        className="bg-[#00FF40] hover:bg-[#00DD30] text-black font-bold py-2 px-4 rounded-md"
      >
        Manage My Courses
      </button>
      
      {/* Your Courses Section */}
      <div className="container mx-auto px-4 py-16 relative z-10">
        <h2 className="text-3xl font-bold mb-8">Your Courses</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Create New Course card */}
          <div
            className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer hover:bg-gray-700 transition duration-300"
            onClick={handleCreateCourse}
          >
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-2">Create New Course</h3>
              <p className="text-gray-400">Start building your next course</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 py-8 mt-16 relative z-10">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>© 2023 GyanSort. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default InstructorHome;
