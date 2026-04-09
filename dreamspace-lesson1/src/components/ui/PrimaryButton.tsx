interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  alt?: boolean
}

export default function PrimaryButton({ alt, className = '', children, ...rest }: Props) {
  return (
    <button className={`ds-btn-primary${alt ? ' alt' : ''} ${className}`} {...rest}>
      {children}
    </button>
  )
}
