import { cn } from "@/lib/utils";

interface PreviewCardProps {
  title: string;
  badge?: string;
  src?: string | null;
  placeholder?: string;
  className?: string;
}

export const PreviewCard = ({
  title,
  badge,
  src,
  placeholder = "Awaiting image",
  className,
}: PreviewCardProps) => (
  <div
    className={cn(
      "flex flex-col rounded-2xl border border-border bg-card shadow-[var(--shadow-soft)] overflow-hidden animate-fade-in-up",
      className,
    )}
  >
    <div className="flex items-center justify-between border-b border-border px-5 py-3">
      <h3 className="font-display text-sm font-semibold text-foreground">{title}</h3>
      {badge && (
        <span className="rounded-full bg-accent px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-accent-foreground">
          {badge}
        </span>
      )}
    </div>
    <div className="flex flex-1 items-center justify-center bg-[image:var(--gradient-subtle)] p-4 min-h-[280px]">
      {src ? (
        <img
          src={src}
          alt={title}
          className="max-h-[420px] w-auto rounded-lg object-contain shadow-[var(--shadow-soft)] animate-scale-in"
        />
      ) : (
        <div className="flex flex-col items-center gap-2 text-muted-foreground">
          <div className="h-14 w-10 rounded-md border-2 border-dashed border-border" />
          <p className="text-xs">{placeholder}</p>
        </div>
      )}
    </div>
  </div>
);
