interface Props {
  children: React.ReactNode
  className?: string
  variant?: 'blue' | 'line'
  style?: React.CSSProperties
}

export default function Card({ children, className = '', variant = 'blue', style }: Props) {
  return (
    <div className={`${variant === 'line' ? 'ds-card-line' : 'ds-card'} ${className}`} style={style}>
      {children}
    </div>
  )
}
