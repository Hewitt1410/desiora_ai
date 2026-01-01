'use client';

import { useState, useEffect } from 'react';
import { plansApi, Plan } from '@/lib/api/plans';
import Link from 'next/link';
import Navigation from '@/components/Navigation';
import { Check, AlertCircle, RefreshCw } from 'lucide-react';

export default function PlansPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlans = async () => {
      setIsLoading(true);
      setError(null);
      try {
        // Fetch only active plans for public display (use public endpoint)
        const data = await plansApi.getAllPublic(true);
        // Sort by sort_order
        const sortedPlans = data.plans.sort((a, b) => a.sort_order - b.sort_order);
        setPlans(sortedPlans);
      } catch (err: any) {
        console.error('Failed to fetch plans:', err);
        setError(err.response?.data?.detail || err.message || 'Failed to load plans');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPlans();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
        <div className="bg-red-100 dark:bg-red-900/20 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-200 rounded-lg p-6 max-w-md text-center">
          <AlertCircle className="h-12 w-12 mx-auto mb-4 text-red-500" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Plans</h2>
          <p className="mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100 mb-3 sm:mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Select the perfect plan for your AI design needs
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 ${
                plan.is_default
                  ? 'border-2 border-primary-600 dark:border-primary-400'
                  : 'border border-gray-200 dark:border-gray-700'
              }`}
            >
              {plan.is_default && (
                <div className="text-center mb-4">
                  <span className="inline-block px-3 py-1 text-xs font-semibold text-primary-600 dark:text-primary-400 bg-primary-100 dark:bg-primary-900/30 rounded-full">
                    Default Plan
                  </span>
                </div>
              )}
              
              <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                {plan.display_name}
              </h3>
              
              {plan.description && (
                <p className="text-gray-600 dark:text-gray-400 mb-6 text-sm">
                  {plan.description}
                </p>
              )}

              <div className="mb-6">
                <div className="flex items-baseline">
                  <span className="text-4xl font-bold text-gray-900 dark:text-gray-100">
                    ${parseFloat(plan.price).toFixed(2)}
                  </span>
                  <span className="text-gray-600 dark:text-gray-400 ml-2">
                    / {plan.period_days === 7 ? 'week' : plan.period_days === 30 ? 'month' : plan.period_days === 365 ? 'year' : `${plan.period_days} days`}
                  </span>
                </div>
              </div>

              <div className="mb-6">
                <div className="flex items-center text-gray-900 dark:text-gray-100 mb-2">
                  <Check className="h-5 w-5 text-primary-600 dark:text-primary-400 mr-2" />
                  <span className="font-semibold">{plan.ai_job_quota} AI Jobs</span>
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Per {plan.period_days === 7 ? 'week' : plan.period_days === 30 ? 'month' : plan.period_days === 365 ? 'year' : `${plan.period_days} days`}
                </div>
              </div>

              <Link
                href={plan.is_default ? '/register' : '/register'}
                className={`block w-full text-center py-3 px-4 rounded-lg font-semibold transition ${
                  plan.is_default
                    ? 'bg-primary-600 text-white hover:bg-primary-700'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600'
                }`}
              >
                {plan.price === '0' || parseFloat(plan.price) === 0 ? 'Get Started' : 'Subscribe'}
              </Link>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Already have an account?{' '}
            <Link href="/login" className="text-primary-600 dark:text-primary-400 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}

