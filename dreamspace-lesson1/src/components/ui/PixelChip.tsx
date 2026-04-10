interface Props {
  children: React.ReactNode
}

export default function PixelChip({ children }: Props) {
  return <span className="ds-pixel-chip">{children}</span>
}
