interface Props {
  children: React.ReactNode
}

export default function SpeechBubble({ children }: Props) {
  return (
    <div className="ds-speech-row">
      <div className="ds-mascot-wrap">
        <img
          className="ds-mascot"
          src="/assets/space-beaver.png"
          alt="Space Beaver mascot"
          onError={(e) => {
            // fallback emoji if asset missing
            const t = e.currentTarget
            t.style.display = 'none'
            t.parentElement!.textContent = '🤖'
          }}
        />
      </div>
      <div className="ds-bubble">{children}</div>
    </div>
  )
}
