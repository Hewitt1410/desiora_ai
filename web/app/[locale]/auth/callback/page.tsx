'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { authApi } from '@/lib/api/auth';
import { useAuthStore } from '@/lib/store/auth';

export default function AuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setUser } = useAuthStore();
  const [error, setError] = useState('');

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const provider = searchParams.get('provider') || 'google';

      if (!code) {
        setError('No authorization code received');
        return;
      }

      try {
        const redirectUri = `${window.location.origin}/auth/callback?provider=${provider}`;
        
        if (provider === 'google') {
          await authApi.googleOAuth({
            code,
            provider: 'google',
            redirect_uri: redirectUri,
          });
        } else if (provider === 'apple') {
          await authApi.appleOAuth({
            code,
            provider: 'apple',
            redirect_uri: redirectUri,
          });
        }

        const user = await authApi.getMe();
        setUser(user);
        router.push('/dashboard');
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Authentication failed');
      }
    };

    handleCallback();
  }, [searchParams, router, setUser]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Authentication Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.push('/login')}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Completing authentication...</p>
      </div>
    </div>
  );
}



