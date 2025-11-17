import React from 'react';
import { Brain } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full bg-gray-900 border-b border-gray-800 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Brain className="w-8 h-8 text-blue-500" />
          </div>
        </div>
      </div>
    </nav>
  );
}