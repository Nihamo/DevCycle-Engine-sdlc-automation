import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import SDLC from "./pages/SDLC";
import { Toaster } from "sonner";

function App() {
  return (
    <Router>
       <Toaster position="top-right" richColors />
      <div className="min-h-screen bg-gray-950">
        {/* <Navbar /> */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/sdlc" element={<SDLC />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
