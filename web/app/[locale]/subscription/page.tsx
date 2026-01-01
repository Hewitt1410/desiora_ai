'use client';

import { useState, useEffect } from 'react';
import AuthGuard from '@/components/AuthGuard';
import { subscriptionsApi, SubscriptionStatusResponse } from '@/lib/api/subscriptions';
import { useAuthStore } from '@/lib/store/auth';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SubscriptionPage() {
  return (
    <AuthGuard>
      <SubscriptionContent />
    </AuthGuard>
  );
}

function SubscriptionContent() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [subscription, setSubscription] = useState<SubscriptionStatusResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCanceling, setIsCanceling] = useState(false);

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const data = await subscriptionsApi.getStatus();
        setSubscription(data);
      } catch (error) {
        console.error('Failed to fetch subscription:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSubscription();
  }, []);

  const handleCancel = async () => {
    if (!confirm('Are you sure you want to cancel your subscription?')) return;

    setIsCanceling(true);
    try {
      await subscriptionsApi.cancel();
      // Refresh subscription status
      const data = await subscriptionsApi.getStatus();
      setSubscription(data);
    } catch (error) {
      console.error('Failed to cancel subscription:', error);
    } finally {
      setIsCanceling(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!subscription) {
    return <div>Failed to load subscription</div>;
  }

  const { subscription: sub, quota_info } = subscription;

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
              <Link href="/subscription" className="text-primary-600 font-semibold">
                Subscription
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Subscription</h1>

          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Current Plan</h2>
              <span
                className={`px-4 py-2 rounded-full text-sm font-semibold ${
                  sub.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : sub.status === 'canceled'
                    ? 'bg-gray-100 text-gray-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                {sub.status}
              </span>
            </div>
            <div className="bg-primary-50 rounded-lg p-6">
              <div className="text-3xl font-bold text-primary-600 mb-2 capitalize">
                {sub.plan} Plan
              </div>
              <div className="text-gray-600">
                {sub.current_period_end
                  ? `Renews on ${new Date(sub.current_period_end).toLocaleDateString()}`
                  : 'No active subscription'}
              </div>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Usage Quota</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>AI Jobs Used</span>
                  <span>
                    {quota_info.used} / {quota_info.quota}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-primary-600 h-3 rounded-full transition-all"
                    style={{ width: `${quota_info.percentage_used}%` }}
                  ></div>
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  {quota_info.remaining} jobs remaining
                </div>
              </div>
              {!subscription.can_use_ai_job && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-yellow-800">
                    You've reached your quota limit. Please upgrade your plan to continue.
                  </p>
                </div>
              )}
            </div>
          </div>

          {sub.status === 'active' && (
            <div className="mb-8">
              <button
                onClick={handleCancel}
                disabled={isCanceling}
                className="px-6 py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 disabled:opacity-50 transition"
              >
                {isCanceling ? 'Canceling...' : 'Cancel Subscription'}
              </button>
            </div>
          )}

          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Available Plans</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { plan: 'weekly', price: '$9.99', quota: '100 jobs/week' },
                { plan: 'monthly', price: '$29.99', quota: '500 jobs/month' },
                { plan: 'yearly', price: '$299.99', quota: '6000 jobs/year' },
              ].map((p) => (
                <div
                  key={p.plan}
                  className={`border-2 rounded-lg p-6 ${
                    sub.plan === p.plan
                      ? 'border-primary-600 bg-primary-50'
                      : 'border-gray-200'
                  }`}
                >
                  <div className="text-2xl font-bold text-gray-900 capitalize mb-2">
                    {p.plan}
                  </div>
                  <div className="text-3xl font-bold text-primary-600 mb-2">{p.price}</div>
                  <div className="text-sm text-gray-600 mb-4">{p.quota}</div>
                  {sub.plan === p.plan ? (
                    <div className="text-sm font-semibold text-primary-600">Current Plan</div>
                  ) : (
                    <button className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
                      Upgrade
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}



