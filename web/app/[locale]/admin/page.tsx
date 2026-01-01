'use client';

import { useState, useEffect } from 'react';
import AuthGuard from '@/components/AuthGuard';
import Navigation from '@/components/Navigation';
import { adminApi, AdminStatsResponse } from '@/lib/api/admin';
import { useAuthStore } from '@/lib/store/auth';
import Link from 'next/link';

export default function AdminPage() {
  return (
    <AuthGuard requireAdmin>
      <AdminContent />
    </AuthGuard>
  );
}

function AdminContent() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<AdminStatsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setError(null);
        const data = await adminApi.getStats();
        setStats(data);
      } catch (err: any) {
        console.error('Failed to fetch stats:', err);
        const errorMessage = err.response?.data?.detail || 
                            err.message || 
                            'Failed to load statistics. Please try again.';
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md">
          <h2 className="text-xl font-semibold text-red-600 mb-4">Error Loading Statistics</h2>
          <p className="text-gray-700 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">No statistics available</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href="/" className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                Desiora AI
              </Link>
              <Link href="/dashboard" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400">
                Dashboard
              </Link>
              <Link href="/admin" className="text-primary-600 dark:text-primary-400 font-semibold">
                Admin
              </Link>
              <Link href="/admin/plans" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400">
                Plans
              </Link>
            </div>
            <div className="flex items-center">
              <span className="text-sm text-gray-600 dark:text-gray-400 mr-4">{user?.email}</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">Admin Dashboard</h1>

        {/* Default Admin Account Info */}
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-yellow-900 dark:text-yellow-200 mb-4">
            🔐 Default Admin Account
          </h2>
          <div className="space-y-2 text-sm">
            <div className="flex items-center space-x-2">
              <span className="font-medium text-yellow-800 dark:text-yellow-300">Email:</span>
              <code className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/50 rounded text-yellow-900 dark:text-yellow-200">
                admin@desiora.ai
              </code>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-medium text-yellow-800 dark:text-yellow-300">Password:</span>
              <code className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/50 rounded text-yellow-900 dark:text-yellow-200">
                admin123
              </code>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-medium text-yellow-800 dark:text-yellow-300">Role:</span>
              <span className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/50 rounded text-yellow-900 dark:text-yellow-200">
                super_admin
              </span>
            </div>
            <div className="mt-4 pt-4 border-t border-yellow-200 dark:border-yellow-800">
              <p className="text-yellow-800 dark:text-yellow-300 text-xs">
                ⚠️ <strong>Security Notice:</strong> This is the default admin account. 
                Please change the password after first login for security purposes.
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-6 sm:mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6">
            <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 mb-2">Total Users</div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">{stats.users.total}</div>
            <div className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1">
              {stats.users.active} active
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6">
            <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 mb-2">Total Subscriptions</div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">{stats.subscriptions.total}</div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6">
            <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 mb-2">Total Jobs</div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">{stats.jobs.total}</div>
            <div className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1">
              Avg: {stats.jobs.average_per_user.toFixed(1)} per user
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6">
            <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 mb-2">AI Usage</div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">
              {stats.usage.usage_percentage.toFixed(1)}%
            </div>
            <div className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1">
              {stats.usage.ai_jobs_used} / {stats.usage.ai_jobs_quota}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-gray-100 mb-3 sm:mb-4">Subscriptions by Plan</h2>
            <div className="space-y-2">
              {Object.entries(stats.subscriptions.by_plan).map(([plan, count]) => (
                <div key={plan} className="flex justify-between text-sm sm:text-base">
                  <span className="text-gray-600 dark:text-gray-400 capitalize">{plan}</span>
                  <span className="font-semibold text-gray-900 dark:text-gray-100">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-gray-100 mb-3 sm:mb-4">Jobs by Status</h2>
            <div className="space-y-2">
              {Object.entries(stats.jobs.by_status).map(([status, count]) => (
                <div key={status} className="flex justify-between text-sm sm:text-base">
                  <span className="text-gray-600 dark:text-gray-400 capitalize">{status}</span>
                  <span className="font-semibold text-gray-900 dark:text-gray-100">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6 mb-6 sm:mb-8">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-gray-100 mb-3 sm:mb-4">Top Users by Jobs</h2>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[300px]">
              <thead>
                <tr className="border-b dark:border-gray-700">
                  <th className="text-left py-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400">User</th>
                  <th className="text-right py-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400">Jobs</th>
                </tr>
              </thead>
              <tbody>
                {stats.usage.top_users.map((topUser) => (
                  <tr key={topUser.user_id} className="border-b dark:border-gray-700">
                    <td className="py-2">
                      <div className="text-sm sm:text-base text-gray-900 dark:text-gray-100 break-all">{topUser.email}</div>
                      {topUser.username && (
                        <div className="text-xs sm:text-sm text-gray-500 dark:text-gray-400">{topUser.username}</div>
                      )}
                    </td>
                    <td className="text-right py-2 font-semibold text-sm sm:text-base text-gray-900 dark:text-gray-100">{topUser.job_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Link
              href="/admin/plans"
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition-shadow border-2 border-primary-200 dark:border-primary-800 hover:border-primary-400 dark:hover:border-primary-600"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-gray-100">Manage Plans</h3>
                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
              <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">
                Create, edit, and manage subscription plans
              </p>
            </Link>
            
            <Link
              href="/admin/users"
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-gray-100">Manage Users</h3>
                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">
                View and manage user accounts
              </p>
            </Link>
            
            <Link
              href="/admin/jobs"
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-gray-100">View Jobs</h3>
                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">
                Monitor and manage design jobs
              </p>
            </Link>
            
            <Link
              href="/admin/subscriptions"
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-gray-100">Subscriptions</h3>
                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
              </div>
              <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">
                View all user subscriptions
              </p>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}



