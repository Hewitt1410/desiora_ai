'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useDropzone } from 'react-dropzone';
import AuthGuard from '@/components/AuthGuard';
import { imagesApi } from '@/lib/api/images';
import { designsApi } from '@/lib/api/designs';
import axios from 'axios';

const DESIGN_STYLES = [
  { value: 'modern', label: 'Modern', description: 'Clean lines, contemporary design' },
  { value: 'minimalist', label: 'Minimalist', description: 'Sparse, uncluttered space' },
  { value: 'rustic', label: 'Rustic', description: 'Wooden, vintage, cozy' },
  { value: 'scandinavian', label: 'Scandinavian', description: 'Light colors, hygge atmosphere' },
  { value: 'industrial', label: 'Industrial', description: 'Exposed brick, metal fixtures' },
  { value: 'bohemian', label: 'Bohemian', description: 'Eclectic, vibrant, artistic' },
  { value: 'traditional', label: 'Traditional', description: 'Classic, elegant, formal' },
  { value: 'contemporary', label: 'Contemporary', description: 'Current trends, mixed styles' },
];

const ROOM_TYPES = [
  { value: 'living_room', label: 'Living Room' },
  { value: 'bedroom', label: 'Bedroom' },
  { value: 'kitchen', label: 'Kitchen' },
  { value: 'bathroom', label: 'Bathroom' },
  { value: 'dining_room', label: 'Dining Room' },
  { value: 'office', label: 'Home Office' },
];

export default function NewDesignPage() {
  return (
    <AuthGuard>
      <NewDesignContent />
    </AuthGuard>
  );
}

function NewDesignContent() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('modern');
  const [selectedRoomType, setSelectedRoomType] = useState<string>('living_room');
  const [prompt, setPrompt] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.heic'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0]);
        setError('');
      }
    },
    onDropRejected: () => {
      setError('File must be an image (JPG, PNG, HEIC) and under 10MB');
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError('');

    try {
      // Step 1: Get presigned URL
      const presignResponse = await imagesApi.presignUpload({
        filename: selectedFile.name,
        content_type: selectedFile.type,
        file_size: selectedFile.size,
      });

      // Step 2: Upload to S3
      await axios.put(presignResponse.upload_url, selectedFile, {
        headers: {
          'Content-Type': selectedFile.type,
        },
      });

      // Step 3: Confirm upload
      await imagesApi.confirmUpload(presignResponse.s3_key);

      setUploadedImageUrl(presignResponse.s3_key);
      setStep(2);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSubmit = async () => {
    if (!uploadedImageUrl) return;

    setIsSubmitting(true);
    setError('');

    try {
      const finalPrompt = prompt || `Redesign this ${selectedRoomType} in ${selectedStyle} style`;
      
      const job = await designsApi.createJob({
        job_type: 'room_design',
        prompt: finalPrompt,
        parameters: {
          image_url: uploadedImageUrl,
          style: selectedStyle,
          room_type: selectedRoomType,
        },
      });

      router.push(`/design/${job.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create design job');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">Desiora AI</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={() => router.push('/dashboard')}
                className="px-4 py-2 text-gray-600 hover:text-gray-900"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900">Create New Design</h2>
              <div className="flex space-x-2">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 1 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-600'}`}>
                  1
                </div>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 2 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-600'}`}>
                  2
                </div>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 3 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-600'}`}>
                  3
                </div>
              </div>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          {step === 1 && (
            <div>
              <h3 className="text-xl font-semibold mb-4">Upload Room Image</h3>
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
                  isDragActive
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-400'
                }`}
              >
                <input {...getInputProps()} />
                {selectedFile ? (
                  <div>
                    <p className="text-gray-700 mb-2">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-gray-600 mb-2">
                      Drag and drop an image here, or click to select
                    </p>
                    <p className="text-sm text-gray-500">
                      JPG, PNG, or HEIC up to 10MB
                    </p>
                  </div>
                )}
              </div>
              {selectedFile && (
                <button
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="mt-4 w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 transition"
                >
                  {isUploading ? 'Uploading...' : 'Upload Image'}
                </button>
              )}
            </div>
          )}

          {step === 2 && (
            <div>
              <h3 className="text-xl font-semibold mb-4">Select Design Style</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {DESIGN_STYLES.map((style) => (
                  <button
                    key={style.value}
                    onClick={() => setSelectedStyle(style.value)}
                    className={`p-4 rounded-lg border-2 transition ${
                      selectedStyle === style.value
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-primary-300'
                    }`}
                  >
                    <div className="font-semibold text-gray-900">{style.label}</div>
                    <div className="text-xs text-gray-600 mt-1">{style.description}</div>
                  </button>
                ))}
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room Type
                </label>
                <select
                  value={selectedRoomType}
                  onChange={(e) => setSelectedRoomType(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  {ROOM_TYPES.map((room) => (
                    <option key={room.value} value={room.value}>
                      {room.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Prompt (Optional)
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Add any specific requirements or preferences..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  rows={4}
                />
              </div>

              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 transition"
              >
                {isSubmitting ? 'Creating Design Job...' : 'Create Design Job'}
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}


