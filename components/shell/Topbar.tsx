"use client";
import { Search, Bell, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { CommandPalette } from './command-palette/CommandPalette';

export function Topbar() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-2 border-b bg-background/70 backdrop-blur px-3">
      <div className="flex-1 flex items-center gap-2">
        <button
          className="flex items-center gap-2 rounded-md border bg-card px-2 py-1 text-sm text-muted-foreground w-full max-w-xl"
          onClick={() => setOpen(true)}
        >
          <Search className="h-4 w-4" />
          <span>Search or jump to…</span>
          <kbd className="ml-auto text-xs">⌘K</kbd>
        </button>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" aria-label="Notifications">
          <Bell className="h-5 w-5" />
        </Button>
        <Button variant="secondary">
          <User className="h-4 w-4 mr-2" />
          Account
        </Button>
      </div>
      <CommandPalette open={open} onOpenChange={setOpen} />
    </header>
  );
}
