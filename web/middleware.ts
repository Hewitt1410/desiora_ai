import createMiddleware from 'next-intl/middleware';
import { locales, defaultLocale } from './i18n';

export default createMiddleware({
  locales,
  defaultLocale,
  localePrefix: 'never' // Disable locale prefix in URL, use Accept-Language header or cookie
});

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)']
};


