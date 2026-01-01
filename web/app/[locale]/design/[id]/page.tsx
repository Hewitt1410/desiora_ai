'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import AuthGuard from '@/components/AuthGuard';
import { designsApi, DesignJobResponse } from '@/lib/api/designs';
// Using img tag instead of Next.js Image for external URLs
import { format } from 'date-fns';

export default function DesignJobPage() {
  return (
    <AuthGuard>
      <DesignJobContent />
    </AuthGuard>
  );
}

function DesignJobContent() {
  const params = useParams();
  const router = useRouter();
  const jobId = parseInt(params.id as string);
  const [job, setJob] = useState<DesignJobResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [polling, setPolling] = useState(false);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const jobData = await designsApi.getJob(jobId);
        setJob(jobData);
        
        // Poll for updates if job is still processing
        if (jobData.status === 'pending' || jobData.status === 'processing') {
          setPolling(true);
        }
      } catch (error) {
        console.error('Failed to fetch job:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchJob();
  }, [jobId]);

  useEffect(() => {
    if (!polling) return;

    const interval = setInterval(async () => {
      try {
        const jobData = await designsApi.getJob(jobId);
        setJob(jobData);
        
        if (jobData.status === 'completed' || jobData.status === 'failed') {
          setPolling(false);
        }
      } catch (error) {
        console.error('Failed to poll job:', error);
        setPolling(false);
      }
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, [polling, jobId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Job not found</h2>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <button
                onClick={() => router.push('/dashboard')}
                className="text-primary-600 hover:text-primary-700"
              >
                ← Back to Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.job_type}</h1>
              <p className="text-gray-600">{job.prompt}</p>
            </div>
            <span
              className={`px-4 py-2 rounded-full text-sm font-semibold ${
                job.status === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : job.status === 'processing'
                  ? 'bg-blue-100 text-blue-800'
                  : job.status === 'failed'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              {job.status}
              {polling && (
                <span className="ml-2 inline-block animate-spin">⟳</span>
              )}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 text-sm text-gray-600">
            <div>
              <span className="font-semibold">Created:</span>{' '}
              {format(new Date(job.created_at), 'MMM d, yyyy HH:mm')}
            </div>
            {job.completed_at && (
              <div>
                <span className="font-semibold">Completed:</span>{' '}
                {format(new Date(job.completed_at), 'MMM d, yyyy HH:mm')}
              </div>
            )}
            {job.processing_time_seconds && (
              <div>
                <span className="font-semibold">Processing Time:</span>{' '}
                {job.processing_time_seconds}s
              </div>
            )}
            {job.retry_count > 0 && (
              <div>
                <span className="font-semibold">Retries:</span> {job.retry_count}/{job.max_retries}
              </div>
            )}
          </div>

          {job.error_message && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 font-semibold mb-1">Error:</p>
              <p className="text-red-700">{job.error_message}</p>
            </div>
          )}

          {job.result_urls && job.result_urls.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Results</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {job.result_urls.map((url, index) => (
                  <div key={index} className="relative aspect-square rounded-lg overflow-hidden shadow-md">
                    <img
                      src={url}
                      alt={`Result ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {job.status === 'pending' || job.status === 'processing' ? (
            <div className="mt-8 text-center">
              <p className="text-gray-600 mb-4">Your design is being processed...</p>
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : null}
        </div>
      </main>
    </div>
  );
}

