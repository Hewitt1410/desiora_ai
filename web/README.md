# Desiora AI - Next.js Web App

Next.js web application for Desiora AI room design platform.

## Features

- ✅ Google OAuth login
- ✅ Room image upload with S3 presigned URLs
- ✅ Design style selection
- ✅ AI design job submission
- ✅ Real-time job status tracking
- ✅ Results gallery
- ✅ Subscription management UI
- ✅ Admin dashboard UI
- ✅ TypeScript
- ✅ Clean, modern UI with Tailwind CSS
- ✅ Auth guard for protected routes

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **React Query** - Data fetching
- **Axios** - HTTP client
- **React Hook Form** - Form handling
- **React Dropzone** - File uploads

## Setup

### 1. Install Dependencies

```bash
cd web
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Project Structure

```
web/
├── app/                    # Next.js app directory
│   ├── admin/             # Admin pages
│   ├── auth/              # Auth pages
│   ├── design/            # Design job pages
│   ├── dashboard/         # User dashboard
│   ├── subscription/      # Subscription management
│   └── login/             # Login page
├── components/            # React components
│   └── AuthGuard.tsx     # Route protection
├── lib/                   # Utilities
│   ├── api/              # API client
│   └── store/            # State management
└── public/                # Static assets
```

## Pages

- `/` - Landing page
- `/login` - Login page with Google OAuth
- `/dashboard` - User dashboard with job list
- `/design/new` - Create new design job
- `/design/[id]` - View design job status and results
- `/subscription` - Subscription management
- `/admin` - Admin dashboard (admin only)
- `/auth/callback` - OAuth callback handler

## API Integration

The app integrates with the FastAPI backend:

- Authentication endpoints
- Image upload endpoints
- Design job endpoints
- Subscription endpoints
- Admin endpoints

## Features

### Authentication
- Email/password login
- Google OAuth
- Token management with refresh
- Protected routes

### Design Jobs
- Image upload with drag & drop
- Style selection
- Job creation
- Real-time status polling
- Results gallery

### Subscription
- View current plan
- Usage quota display
- Plan comparison
- Cancel subscription

### Admin Dashboard
- User statistics
- Subscription statistics
- Job statistics
- Usage metrics
- Top users

## Development

```bash
# Development
npm run dev

# Build
npm run build

# Start production server
npm start

# Lint
npm run lint
```

## License

MIT


