"use client";
import { signIn } from 'next-auth/react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';

export default function SignInPage() {
  const [email, setEmail] = useState('owner@enai.local');
  const [password, setPassword] = useState('password');

  return (
    <div className="min-h-screen grid place-items-center p-6">
      <div className="w-full max-w-md space-y-4 rounded-lg border bg-card p-6">
        <h1 className="text-xl font-semibold">Sign in to en-AI</h1>
        <div className="space-y-2">
          <input className="w-full rounded-md border bg-background px-3 py-2" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <input className="w-full rounded-md border bg-background px-3 py-2" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
          <Button className="w-full" onClick={() => signIn('credentials', { email, password, callbackUrl: '/' })}>Sign in</Button>
          <Button variant="secondary" className="w-full" onClick={() => signIn('email', { email, callbackUrl: '/' })}>Send magic link (console)</Button>
        </div>
      </div>
    </div>
  );
}
