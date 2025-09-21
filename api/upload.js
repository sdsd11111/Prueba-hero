// api/upload.js
import { put } from '@vercel/blob';
import { NextResponse } from 'next/server';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function upload(request) {
  if (request.method !== 'POST') {
    return new NextResponse('Método no permitido', { status: 405 });
  }

  try {
    const formData = await request.formData();
    const file = formData.get('file');
    
    if (!file) {
      return NextResponse.json(
        { error: 'No se proporcionó ningún archivo' }, 
        { status: 400 }
      );
    }

    // Subir a Vercel Blob Storage
    const blob = await put(file.name, file, { 
      access: 'public',
      token: process.env.BLOB_READ_WRITE_TOKEN
    });

    return NextResponse.json(blob);
    
  } catch (error) {
    console.error('Error al subir el archivo:', error);
    return NextResponse.json(
      { error: 'Error al subir el archivo: ' + error.message }, 
      { status: 500 }
    );
  }
}
