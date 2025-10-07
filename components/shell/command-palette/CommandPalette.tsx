"use client";
import * as React from 'react';
import { Command } from 'cmdk';
import { useRouter } from 'next/navigation';

export function CommandPalette({ open, onOpenChange }: { open: boolean; onOpenChange: (v: boolean) => void }) {
  const router = useRouter();
  const [search, setSearch] = React.useState('');

  React.useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        onOpenChange(true);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [onOpenChange]);

  const navigate = (path: string) => {
    router.push(path);
    onOpenChange(false);
  };

  return (
    <div className={`fixed inset-0 z-50 ${open ? '' : 'pointer-events-none'}`} onClick={() => onOpenChange(false)}>
      <div className={`mx-auto mt-24 max-w-2xl rounded-lg border bg-background shadow-xl ${open ? '' : 'hidden'}`} onClick={(e) => e.stopPropagation()}>
        <Command value={search} onValueChange={setSearch} label="Global search">
          <Command.Input placeholder="Search projects, pipelines, prompts…" />
          <Command.List>
            <Command.Empty>No results.</Command.Empty>
            <Command.Group heading="Navigate">
              {[
                ['/', 'Home'],
                ['/dashboard', 'Dashboard'],
                ['/projects', 'Projects'],
                ['/pipelines', 'Pipelines'],
                ['/runs', 'Runs'],
                ['/prompts', 'Prompts'],
                ['/datasets', 'Datasets'],
                ['/templates', 'Templates'],
                ['/billing', 'Billing'],
                ['/settings', 'Settings'],
                ['/org/settings', 'Org Settings'],
                ['/admin', 'Admin'],
                ['/docs', 'Docs']
              ].map(([path, label]) => (
                <Command.Item key={path} onSelect={() => navigate(path)}>
                  {label}
                </Command.Item>
              ))}
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </div>
  );
}
