'use client';

import { useState, useEffect } from 'react';
import AuthGuard from '@/components/AuthGuard';
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

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await adminApi.getStats();
        setStats(data);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
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

  if (!stats) {
    return <div>Failed to load statistics</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href="/" className="text-2xl font-bold text-primary-600">
                Desiora AI
              </Link>
              <Link href="/dashboard" className="text-gray-700 hover:text-primary-600">
                Dashboard
              </Link>
              <Link href="/admin" className="text-primary-600 font-semibold">
                Admin
              </Link>
            </div>
            <div className="flex items-center">
              <span className="text-sm text-gray-600 mr-4">{user?.email}</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-sm text-gray-600 mb-2">Total Users</div>
            <div className="text-3xl font-bold text-gray-900">{stats.users.total}</div>
            <div className="text-sm text-gray-500 mt-1">
              {stats.users.active} active
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-sm text-gray-600 mb-2">Total Subscriptions</div>
            <div className="text-3xl font-bold text-gray-900">{stats.subscriptions.total}</div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-sm text-gray-600 mb-2">Total Jobs</div>
            <div className="text-3xl font-bold text-gray-900">{stats.jobs.total}</div>
            <div className="text-sm text-gray-500 mt-1">
              Avg: {stats.jobs.average_per_user.toFixed(1)} per user
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-sm text-gray-600 mb-2">AI Usage</div>
            <div className="text-3xl font-bold text-gray-900">
              {stats.usage.usage_percentage.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-500 mt-1">
              {stats.usage.ai_jobs_used} / {stats.usage.ai_jobs_quota}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Subscriptions by Plan</h2>
            <div className="space-y-2">
              {Object.entries(stats.subscriptions.by_plan).map(([plan, count]) => (
                <div key={plan} className="flex justify-between">
                  <span className="text-gray-600 capitalize">{plan}</span>
                  <span className="font-semibold">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Jobs by Status</h2>
            <div className="space-y-2">
              {Object.entries(stats.jobs.by_status).map(([status, count]) => (
                <div key={status} className="flex justify-between">
                  <span className="text-gray-600 capitalize">{status}</span>
                  <span className="font-semibold">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Users by Jobs</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 text-gray-600">User</th>
                  <th className="text-right py-2 text-gray-600">Jobs</th>
                </tr>
              </thead>
              <tbody>
                {stats.usage.top_users.map((topUser) => (
                  <tr key={topUser.user_id} className="border-b">
                    <td className="py-2">
                      <div className="text-gray-900">{topUser.email}</div>
                      {topUser.username && (
                        <div className="text-sm text-gray-500">{topUser.username}</div>
                      )}
                    </td>
                    <td className="text-right py-2 font-semibold">{topUser.job_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 flex space-x-4">
          <Link
            href="/admin/users"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition"
          >
            View Users
          </Link>
          <Link
            href="/admin/jobs"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition"
          >
            View Jobs
          </Link>
        </div>
      </main>
    </div>
  );
}


