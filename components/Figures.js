"use client";

import { useCallback, useEffect, useState } from "react";

export default function Figures({ images }) {
  const [open, setOpen] = useState(null);

  const close = useCallback(() => setOpen(null), []);
  const prev = useCallback(
    () => setOpen((i) => (i === null ? i : (i - 1 + images.length) % images.length)),
    [images.length]
  );
  const next = useCallback(
    () => setOpen((i) => (i === null ? i : (i + 1) % images.length)),
    [images.length]
  );

  useEffect(() => {
    if (open === null) return;
    const onKey = (e) => {
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") prev();
      if (e.key === "ArrowRight") next();
    };
    window.addEventListener("keydown", onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [open, close, prev, next]);

  const im = open === null ? null : images[open];

  return (
    <>
      <div className="figures">
        {images.map((f, i) => (
          <figure
            key={f.src}
            className="fig-card"
            role="button"
            tabIndex={0}
            aria-label={`Ampliar: ${f.caption}`}
            onClick={() => setOpen(i)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                setOpen(i);
              }
            }}
          >
            <img src={f.src} alt={f.caption} />
            <figcaption>{f.caption}</figcaption>
            {f.desc && <p className="fig-desc">{f.desc}</p>}
          </figure>
        ))}
      </div>

      {im && (
        <div className="lightbox" role="dialog" aria-modal="true" aria-label={im.caption} onClick={close}>
          <button className="lightbox-close" aria-label="Cerrar" onClick={close}>
            <span className="mi">close</span>
          </button>
          <div className="lightbox-body" onClick={(e) => e.stopPropagation()}>
            <div className="lightbox-stage">
              <img src={im.src} alt={im.caption} />
            </div>
            <div className="lightbox-meta">
              <div className="lightbox-text">
                <h3>{im.caption}</h3>
                {im.desc && <p>{im.desc}</p>}
              </div>
              <div className="lightbox-nav">
                <button aria-label="Anterior" onClick={prev}>
                  <span className="mi">arrow_back</span>
                </button>
                <span>
                  {open + 1} / {images.length}
                </span>
                <button aria-label="Siguiente" onClick={next}>
                  <span className="mi">arrow_forward</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
