import { useCallback, useRef, useState } from "react";
import { Upload, Camera } from "lucide-react";
import { cn } from "@/lib/utils";

interface DropzoneProps {
  onFile: (file: File) => void;
}

export const Dropzone = ({ onFile }: DropzoneProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const cameraRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback(
    (files: FileList | null) => {
      if (!files || files.length === 0) return;
      const file = files[0];
      if (!file.type.startsWith("image/")) return;
      onFile(file);
    },
    [onFile],
  );

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFiles(e.dataTransfer.files);
      }}
      onClick={() => inputRef.current?.click()}
      className={cn(
        "group relative flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed bg-card p-10 text-center cursor-pointer transition-all duration-300",
        "hover:border-primary hover:bg-accent/40 hover:shadow-[var(--shadow-soft)]",
        isDragging
          ? "border-primary bg-accent/60 scale-[1.01]"
          : "border-border",
      )}
    >
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-[image:var(--gradient-hero)] text-primary-foreground shadow-[var(--shadow-elegant)] transition-transform duration-300 group-hover:scale-110">
        <Upload className="h-7 w-7" />
      </div>
      <div className="space-y-1">
        <p className="font-display text-lg font-semibold text-foreground">
          Drop your document here
        </p>
        <p className="text-sm text-muted-foreground">
          or <span className="text-primary font-medium">browse</span> to upload — JPG, PNG up to 10MB
        </p>
      </div>

      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          cameraRef.current?.click();
        }}
        className="mt-2 inline-flex items-center gap-2 rounded-full border border-border bg-background px-4 py-2 text-xs font-medium text-foreground hover:bg-accent transition-colors md:hidden"
      >
        <Camera className="h-4 w-4" />
        Use camera
      </button>

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <input
        ref={cameraRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  );
};
