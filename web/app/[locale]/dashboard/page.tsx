'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import AuthGuard from '@/components/AuthGuard';
import Navigation from '@/components/Navigation';
import { designsApi, DesignJobResponse } from '@/lib/api/designs';
import { useAuthStore } from '@/lib/store/auth';
import Link from 'next/link';
import { format } from 'date-fns';

export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}

function DashboardContent() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [jobs, setJobs] = useState<DesignJobResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await designsApi.listJobs({ page_size: 10 });
        setJobs(response.jobs);
      } catch (error) {
        console.error('Failed to fetch jobs:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">My Design Jobs</h1>
          <Link
            href="/design/new"
            className="w-full sm:w-auto px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition text-center text-sm sm:text-base"
          >
            Create New Design
          </Link>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 mb-4 text-base sm:text-lg">No design jobs yet</p>
            <Link
              href="/design/new"
              className="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition text-sm sm:text-base"
            >
              Create Your First Design
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {jobs.map((job) => (
              <Link
                key={job.id}
                href={`/design/${job.id}`}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-md dark:shadow-gray-700/50 p-4 sm:p-6 hover:shadow-lg transition"
              >
                <div className="flex justify-between items-start mb-3 sm:mb-4">
                  <span
                    className={`px-2 sm:px-3 py-1 rounded-full text-xs font-semibold ${
                      job.status === 'completed'
                        ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200'
                        : job.status === 'processing'
                        ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200'
                        : job.status === 'failed'
                        ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                    }`}
                  >
                    {job.status}
                  </span>
                  <span className="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                    {format(new Date(job.created_at), 'MMM d, yyyy')}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2 text-sm sm:text-base">{job.job_type}</h3>
                <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 line-clamp-2">{job.prompt}</p>
                {job.result_urls && job.result_urls.length > 0 && (
                  <div className="mt-3 sm:mt-4">
                    <span className="text-xs sm:text-sm text-primary-600 dark:text-primary-400 font-semibold">
                      {job.result_urls.length} result{job.result_urls.length > 1 ? 's' : ''}
                    </span>
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}


