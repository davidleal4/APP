import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(({ className, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn('w-full rounded-md border bg-background px-3 py-2 text-sm', className)}
    {...props}
  />
));
Textarea.displayName = 'Textarea';
