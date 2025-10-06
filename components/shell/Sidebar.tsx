"use client";
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils/cn';
import { Home, LineChart, Boxes, Workflow, PlayCircle, Library, Database, Store, CreditCard, Settings, ShieldCheck, BookOpen } from 'lucide-react';

const items = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/dashboard', label: 'Dashboard', icon: LineChart },
  { href: '/projects', label: 'Projects', icon: Boxes },
  { href: '/pipelines', label: 'Pipelines', icon: Workflow },
  { href: '/runs', label: 'Runs', icon: PlayCircle },
  { href: '/prompts', label: 'Prompts', icon: Library },
  { href: '/datasets', label: 'Datasets', icon: Database },
  { href: '/templates', label: 'Templates', icon: Store },
  { href: '/billing', label: 'Billing', icon: CreditCard },
  { href: '/settings', label: 'Settings', icon: Settings },
  { href: '/org/settings', label: 'Org', icon: ShieldCheck },
  { href: '/admin', label: 'Admin', icon: ShieldCheck },
  { href: '/docs', label: 'Docs', icon: BookOpen },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="hidden md:flex w-64 shrink-0 flex-col gap-2 border-r bg-card/40 p-3">
      <div className="text-lg font-semibold px-2">en-AI</div>
      <nav className="flex-1 space-y-1">
        {items.map(({ href, label, icon: Icon }) => (
          <Link key={href} href={href} className={cn(
            'flex items-center gap-2 rounded-md px-3 py-2 text-sm hover:bg-accent/60',
            pathname === href && 'bg-accent/80'
          )}>
            <Icon className="h-4 w-4" />
            <span>{label}</span>
          </Link>
        ))}
      </nav>
      <div className="px-2 text-xs text-muted-foreground">© {new Date().getFullYear()} en-AI</div>
    </aside>
  );
}
