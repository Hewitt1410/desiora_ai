'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth';
import Navigation from '@/components/Navigation';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, isLoading, fetchUser } = useAuthStore();

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem('access_token');
      if (token && !isAuthenticated) {
        await fetchUser();
      }
    };
    init();
  }, [isAuthenticated, fetchUser]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16">
        <div className="text-center">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-gray-100 mb-4 sm:mb-6">
            Transform Your Rooms with AI
          </h1>
          <p className="text-base sm:text-lg lg:text-xl text-gray-600 dark:text-gray-400 mb-6 sm:mb-8 max-w-2xl mx-auto px-4">
            Upload a photo and let AI redesign your space in any style you want
          </p>
          {isAuthenticated ? (
            <Link
              href="/dashboard"
              className="inline-block px-6 sm:px-8 py-3 sm:py-4 bg-primary-600 text-white rounded-lg text-base sm:text-lg font-semibold hover:bg-primary-700 transition shadow-lg hover:shadow-xl"
            >
              Go to Dashboard
            </Link>
          ) : (
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                href="/login"
                className="w-full sm:w-auto inline-block px-6 sm:px-8 py-3 sm:py-4 bg-primary-600 text-white rounded-lg text-base sm:text-lg font-semibold hover:bg-primary-700 transition shadow-lg hover:shadow-xl text-center"
              >
                Get Started
              </Link>
              <Link
                href="/plans"
                className="w-full sm:w-auto inline-block px-6 sm:px-8 py-3 sm:py-4 bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 border-2 border-primary-600 dark:border-primary-400 rounded-lg text-base sm:text-lg font-semibold hover:bg-primary-50 dark:hover:bg-gray-700 transition text-center"
              >
                View Plans
              </Link>
            </div>
          )}
        </div>

        {/* Features section */}
        <div className="mt-12 sm:mt-16 lg:mt-20 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 sm:p-8">
            <div className="text-3xl mb-4">🎨</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Multiple Styles
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base">
              Choose from modern, minimalist, rustic, and more design styles
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 sm:p-8">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Fast Processing
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base">
              Get your redesigned room in minutes with AI-powered processing
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 sm:p-8 sm:col-span-2 lg:col-span-1">
            <div className="text-3xl mb-4">📱</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Easy to Use
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base">
              Simply upload a photo and let AI do the rest
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}


