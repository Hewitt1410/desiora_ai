'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAdmin?: boolean;
}

export default function AuthGuard({ children, requireAdmin = false }: AuthGuardProps) {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, fetchUser } = useAuthStore();

  useEffect(() => {
    const checkAuth = async () => {
      if (!isAuthenticated && !isLoading) {
        const token = localStorage.getItem('access_token');
        if (token) {
          await fetchUser();
        } else {
          router.push('/login');
        }
      } else if (isAuthenticated && requireAdmin) {
        if (user && user.role !== 'admin' && user.role !== 'super_admin') {
          router.push('/');
        }
      }
    };

    checkAuth();
  }, [isAuthenticated, isLoading, requireAdmin, user, router, fetchUser]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  if (requireAdmin && user && user.role !== 'admin' && user.role !== 'super_admin') {
    return null;
  }

  return <>{children}</>;
}




